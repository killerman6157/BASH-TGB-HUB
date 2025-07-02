import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import user, admin, scheduler
from database.db import create_tables
from utils.scheduler import start_scheduler

load_dotenv()  # Load environment variables

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    await create_tables()  # Create DB tables if not exist

    dp.include_router(user.router)
    dp.include_router(admin.router)

    await start_scheduler(bot)  # Start the daily open/close scheduler

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🤖 Bot stopped.")
