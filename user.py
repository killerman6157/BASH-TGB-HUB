from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from scheduler import is_within_time
from config import ADMIN_ID
from utils import database

router = Router()

class BuyerState(StatesGroup):
    jira_lamba = State()
    jira_otp = State()
    jira_bank = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if not is_within_time():
        return await message.answer("🚫 An rufe karɓar Telegram accounts. Za a bude gobe 8:00 na safe (WAT).")

    await state.set_state(BuyerState.jira_lamba)
    await message.answer("📥 Turo lambar waya da kake son siyarwa. Ka cire 2FA kafin turo.")

@router.message(BuyerState.jira_lamba)
async def karba_lamba(message: Message, state: FSMContext):
    lamba = message.text.strip()
    if database.phone_exists(lamba):
        return await message.answer(f"⚠️ An riga an karɓi wannan lambar: {lamba}.
⏳ Sake turawa bayan mako ɗaya.")

    database.save_account(message.from_user.id, lamba)
    await state.update_data(phone=lamba)
    await state.set_state(BuyerState.jira_otp)
    await message.answer(f"✅ An tura OTP zuwa {lamba}.
📩 Turo OTP a nan.")

@router.message(BuyerState.jira_otp)
async def karba_otp(message: Message, state: FSMContext):
    data = await state.get_data()
    lamba = data.get("phone")
    await state.clear()
    await message.answer(f"✅ An shiga account ɗin {lamba}.
💵 Za a biya daga 8:00PM WAT. Yi amfani da /withdraw don tura info.")

@router.message(Command("withdraw"))
async def withdraw(message: Message, state: FSMContext):
    if not is_within_time():
        return await message.answer("🚫 An rufe biyan kuɗi. Za a bude gobe 8:00AM (WAT).")

    await state.set_state(BuyerState.jira_bank)
    await message.answer("💳 Turo lambar asusun ka da sunan mai asusun. Misali: 9131085651 OPay Bashir Rabiu")

@router.message(BuyerState.jira_bank)
async def karba_bank(message: Message, state: FSMContext):
    info = message.text.strip()
    database.save_withdrawal(message.from_user.id, info)
    await state.clear()
    await message.answer("✅ Bukatar cire kuɗi ta karɓu. Ana jira admin.")

    accounts = database.get_user_accounts(message.from_user.id)
    await message.bot.send_message(
        ADMIN_ID,
        f"💰 BUKATAR BIYA!
👤 User: {message.from_user.id} (@{message.from_user.username})
"
        f"📱 Accounts: {', '.join(accounts)}
🏦 Banki: {info}
"
        f"/mark_paid {message.from_user.id} {len(accounts)}"
    )
