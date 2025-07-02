from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import DB_NAME
from utils.states import AccountSubmission, WithdrawRequest
from utils.validators import is_valid_phone_number
from utils.session_login import secure_account
from datetime import datetime
import aiosqlite

router = Router()

# Open/Close time control
def is_within_open_hours():
    now = datetime.now()
    return 8 <= now.hour < 22  # WAT time

@router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    if not is_within_open_hours():
        return await message.answer(
            "⛔ An rufe karɓar Telegram accounts na yau.\n"
            "Za a bude gobe da karfe 8:00 na safe."
        )

    await message.answer(
        "Barka da zuwa cibiyar karɓar Telegram accounts!\n\n"
        "Don farawa, turo lambar wayar account ɗin da kake son sayarwa (misali: +2348167757987).\n"
        "Tabbatar ka cire Two-Factor Authentication (2FA) kafin ka tura."
    )
    await state.set_state(AccountSubmission.waiting_for_phone)

@router.message(AccountSubmission.waiting_for_phone)
async def receive_phone(message: Message, state: FSMContext):
    phone = message.text.strip()

    if not is_valid_phone_number(phone):
        return await message.answer("❌ Lambar ba daidai ba ce.")

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT 1 FROM user_accounts WHERE phone_number = ?", (phone,)
        )
        exists = await cursor.fetchone()

    if exists:
        return await message.answer(
            f"⚠️ Kuskure! An riga an yi rajistar wannan lambar!\n\n📞 {phone}"
        )

    await state.update_data(phone=phone)
    await message.answer(
        f"📨 Ana sarrafawa... Don Allah a jira.\n\n🇳🇬 An tura OTP zuwa lambar: {phone}\n"
        "Ka turo lambar OTP a nan."
    )
    await state.set_state(AccountSubmission.waiting_for_otp)

@router.message(AccountSubmission.waiting_for_otp)
async def receive_otp(message: Message, state: FSMContext):
    otp = message.text.strip()
    data = await state.get_data()
    phone = data.get("phone")

    result = await secure_account(phone, otp, buyer_id=message.from_user.id, bot=message.bot)

    if result == "2FA required":
        return
    elif result != "success":
        return await message.answer("❌ Kuskure wajen login. Ka tabbatar OTP ɗin ya dace.")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO user_accounts (user_id, phone_number, status) VALUES (?, ?, ?)",
            (message.from_user.id, phone, "accepted")
        )
        await db.commit()

    await message.answer(
        "✅ An shiga account ɗin ku cikin nasara. Ku cire shi daga na'urar ku.\n"
        "Za a biya ku daga karfe 8:00 na dare (WAT)."
    )
    await state.clear()

@router.message(F.text == "/withdraw")
async def withdraw_request(message: Message, state: FSMContext):
    now = datetime.now()
    if not (8 <= now.hour < 22):
        return await message.answer(
            "⛔ An rufe biyan kuɗi na yau. Za a sake bude gobe da karfe 8:00 AM (WAT)."
        )

    await message.answer("✍ Maza turo lambar account ɗin banki da sunan mai account:\n\nMisali:\n`9131085651 OPay Bashir Rabiu`")
    await state.set_state(WithdrawRequest.waiting_for_bank_info)

@router.message(WithdrawRequest.waiting_for_bank_info)
async def receive_bank_info(message: Message, state: FSMContext):
    bank_info = message.text.strip()

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO payment_requests (user_id, bank_info, status) VALUES (?, ?, ?)",
            (message.from_user.id, bank_info, "pending")
        )
        await db.commit()

    await message.answer("✅ An karɓi bukatar cire kuɗi. Za a biya daga karfe 8:00 PM.")
    await message.bot.send_message(
        message.bot.admin_id if hasattr(message.bot, 'admin_id') else  ADMIN_ID,
        f"💵 *BUKATAR BIYA!*\n\n"
        f"User ID: `{message.from_user.id}` (@{message.from_user.username})\n"
        f"Bayanan Banki: `{bank_info}`",
        parse_mode="Markdown"
    )
    await state.clear()

@router.message(F.text == "/myaccounts")
async def my_accounts(message: Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT phone_number, status FROM user_accounts WHERE user_id = ?",
            (message.from_user.id,)
        )
        rows = await cursor.fetchall()

    if not rows:
        return await message.answer("❌ Ba ka da wata lamba da ka tura tukuna.")

    response = "📋 Lambar da ka tura:\n\n"
    for phone, status in rows:
        response += f"📞 `{phone}` — `{status}`\n"

    await message.answer(response, parse_mode="Markdown")
