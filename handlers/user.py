from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime
from config import ADMIN_ID, OPEN_HOUR, CLOSE_HOUR, DB_NAME
from utils.states import AccountSubmission, WithdrawRequest
from utils.validators import is_valid_phone_number, is_2fa_error
import aiosqlite

router = Router()

# ⏰ Check if account receiving is open
def is_within_open_hours() -> bool:
    now = datetime.now()
    return OPEN_HOUR <= now.hour < CLOSE_HOUR

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Barka da zuwa cibiyar karbar Telegram accounts!\n"
        "Don farawa, turo lambar wayar account din da kake son sayarwa (misali: +2348167757987).\n"
        "Tabbatar ka cire Two-Factor Authentication (2FA) kafin ka tura.\n\n"
        "Idan ka fasa, danna /cancel."
    )
    await state.set_state(AccountSubmission.waiting_for_phone)

@router.message(AccountSubmission.waiting_for_phone)
async def receive_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not is_valid_phone_number(phone):
        return await message.answer("❌ Lambar wayarka ba daidai ba ce. Ka sake gwadawa.")

    if not is_within_open_hours():
        return await message.answer(
            "⛔ An rufe karbar Telegram accounts na yau.\n"
            f"Za a sake buɗewa gobe da karfe {OPEN_HOUR}:00 na safe."
        )

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM user_accounts WHERE phone_number = ?", (phone,))
        exists = await cursor.fetchone()
        if exists:
            return await message.answer(f"⚠️ Kuskure! An riga an yi rajistar wannan lambar!\n{phone}\nBa za ka iya sake tura wannan lambar ba sai nan da mako ɗaya.")

        await db.execute(
            "INSERT INTO user_accounts (user_id, phone_number) VALUES (?, ?)",
            (message.from_user.id, phone)
        )
        await db.commit()

    await state.update_data(phone=phone)
    await message.answer(f"Ana sarrafawa... Don Allah a jira.\n🇳🇬 An tura OTP zuwa: {phone}\nTuro lambar sirrin a nan.")
    await state.set_state(AccountSubmission.waiting_for_otp)

@router.message(AccountSubmission.waiting_for_otp)
async def receive_otp(message: Message, state: FSMContext):
    otp = message.text.strip()
    data = await state.get_data()
    phone = data.get("phone")

    # Simulated login attempt — replace with real Telethon/Pyrogram login
    try:
        if "0000" in otp or "1234" in otp:
            raise Exception("Password required")  # 2FA mock error

        # login success
        await message.answer(
            "✅ An shiga account din ku cikin nasara. Ku cire shi daga na'urar ku.\n"
            "Za a biya ku daga karfe 8:00 na dare (WAT)."
        )
    except Exception as e:
        if is_2fa_error(e):
            await message.answer("⚠ Lambar tana da 2FA/password. Ka cire 2FA kafin ka sake tura.")
        else:
            await message.answer(f"❌ Kuskure wajen shiga account: {e}")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE user_accounts SET status = ? WHERE phone_number = ?",
            ("accepted", phone)
        )
        await db.commit()

    await state.clear()

@router.message(F.text == "/cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ An soke aikin cikin nasara.")

@router.message(F.text == "/withdraw")
async def cmd_withdraw(message: Message, state: FSMContext):
    if not is_within_open_hours():
        return await message.answer("⛔ An rufe biyan kuɗi na yau. Za a buɗe gobe da karfe 8:00 na safe.")

    await message.answer(
        "Maza turo lambar asusun bankinka da sunan mai asusun.\n"
        "Misali: 9131085651 OPay Bashir Rabiu."
    )
    await state.set_state(WithdrawRequest.waiting_for_bank_info)

@router.message(WithdrawRequest.waiting_for_bank_info)
async def receive_bank_info(message: Message, state: FSMContext):
    bank_info = message.text.strip()
    user_id = message.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO payment_requests (user_id, bank_info) VALUES (?, ?)",
            (user_id, bank_info)
        )
        await db.commit()

    await message.answer("✅ An karbi bukatar cire kuɗi. Za a tura maka kuɗin daga karfe 8:00 na dare (WAT).")

    text = (
        f"💰 BUKATAR BIYA!\n"
        f"User ID: {user_id} (Username: @{message.from_user.username})\n"
        f"Bayanan Banki: {bank_info}\n"
        f"Danna /user_accounts {user_id} don duba adadin accounts ɗinsa."
    )
    await message.bot.send_message(ADMIN_ID, text)
    await state.clear()

@router.message(F.text == "/myaccounts")
async def cmd_myaccounts(message: Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT phone_number, status FROM user_accounts WHERE user_id = ?",
            (message.from_user.id,)
        )
        rows = await cursor.fetchall()

    if not rows:
        await message.answer("❌ Ba ka da wata lamba da ka tura tukuna.")
    else:
        response = "📋 Lambobin da ka tura:\n\n"
        for phone, status in rows:
            response += f"📞 `{phone}` — `{status}`\n"
        await message.answer(response, parse_mode="Markdown")
