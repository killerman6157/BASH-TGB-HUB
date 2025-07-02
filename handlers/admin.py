from aiogram import Router, types, F
from config import ADMIN_ID, CHANNEL_ID, DB_NAME
import aiosqlite
from datetime import datetime

router = Router()

@router.message(F.text.startswith("/user_accounts"))
async def user_accounts(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()
    if len(parts) != 2:
        return await message.answer("❌ Amfani: /user_accounts [User ID]")

    user_id = parts[1]

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM user_accounts WHERE user_id = ? AND status = 'accepted'",
            (user_id,)
        )
        count = (await cursor.fetchone())[0]

    await message.answer(f"👤 User ID {user_id} yana da accounts guda {count} da aka karba, kuma a shirye suke don biya.")

@router.message(F.text.startswith("/mark_paid"))
async def mark_paid(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer("❌ Amfani: /mark_paid [User ID] [Adadin Accounts]")

    user_id = int(parts[1])
    num_paid = int(parts[2])

    async with aiosqlite.connect(DB_NAME) as db:
        # Get accounts
        cursor = await db.execute(
            "SELECT phone_number FROM user_accounts WHERE user_id = ? AND status = 'accepted' LIMIT ?",
            (user_id, num_paid)
        )
        rows = await cursor.fetchall()

        # Update to paid
        for row in rows:
            phone = row[0]
            await db.execute(
                "UPDATE user_accounts SET status = 'paid' WHERE phone_number = ?", (phone,)
            )
            await db.execute(
                "INSERT INTO paid_accounts (user_id, phone_number) VALUES (?, ?)", (user_id, phone)
            )

        # Mark payment request
        await db.execute(
            "UPDATE payment_requests SET status = 'paid', paid_at = CURRENT_TIMESTAMP WHERE user_id = ? AND status = 'pending'",
            (user_id,)
        )

        await db.commit()

    await message.answer(f"✅ An yiwa User ID {user_id} alamar biya don accounts guda {num_paid}.")

@router.message(F.text == "/completed_today_payment")
async def completed_today_payment(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.bot.send_message(
        CHANNEL_ID,
        "📢 *SANARWA:*\nAn biya duk wanda ya nemi biya yau! Muna maku fatan alheri, sai gobe karfe 8:00 na safe.",
        parse_mode="Markdown"
    )
    await message.answer("✅ An sanar da channel cewa an kammala biya.")

@router.message(F.text == "/stats")
async def show_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT status, COUNT(*) FROM user_accounts GROUP BY status"
        )
        stats = await cursor.fetchall()

    response = "📊 *Statistics:*\n"
    for status, count in stats:
        response += f"• {status}: {count}\n"

    await message.answer(response, parse_mode="Markdown")
