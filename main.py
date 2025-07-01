import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import user, admin
from scheduler import start_scheduler

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(user.router, admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
