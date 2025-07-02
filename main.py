import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import user, admin
from utils.scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Routers
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Start scheduler for opening/closing
    await start_scheduler(bot)

    # Bot commands (optional)
    await bot.set_my_commands([
        BotCommand(command="start", description="Fara amfani da bot"),
        BotCommand(command="withdraw", description="Nemi biyan kuɗi"),
        BotCommand(command="myaccounts", description="Duba lambobin da ka tura"),
    ])

    print("✅ Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
