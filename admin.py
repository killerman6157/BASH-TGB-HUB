from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID, CHANNEL_ID
from utils import database

router = Router()

@router.message(Command("user_accounts"))
async def user_accounts(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) != 2:
        return await message.answer("🛠 Amfani: /user_accounts [UserID]")

    user_id = int(args[1])
    count = database.count_user_accounts(user_id)
    await message.answer(f"👤 User ID: {user_id} yana da accounts {count} masu jiran biya.")

@router.message(Command("mark_paid"))
async def mark_paid(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) != 3:
        return await message.answer("🛠 Amfani: /mark_paid [UserID] [Adadi]")

    user_id = int(args[1])
    amount = int(args[2])
    database.mark_accounts_paid(user_id, amount)
    await message.answer(f"✅ An biya User ID {user_id} don accounts {amount}.")

@router.message(Command("completed_today_payment"))
async def completed_today(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.bot.send_message(
        CHANNEL_ID,
        "📢 SANARWA: An kammala biyan kuɗi na yau! Sai gobe 8:00AM."
    )
    await message.answer("📬 An sanar da channel.")
