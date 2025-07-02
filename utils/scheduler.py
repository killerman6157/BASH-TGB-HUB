from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time, timedelta
import pytz
from config import OPEN_HOUR, CLOSE_HOUR

# Nigeria timezone (WAT)
TZ = pytz.timezone("Africa/Lagos")

# Global flag
account_receiving_open = False

def get_current_time_wat():
    return datetime.now(TZ)

async def open_account_receiving():
    global account_receiving_open
    account_receiving_open = True
    print("✅ An buɗe karɓar accounts –", get_current_time_wat().strftime("%H:%M"))

async def close_account_receiving():
    global account_receiving_open
    account_receiving_open = False
    print("⛔ An rufe karɓar accounts –", get_current_time_wat().strftime("%H:%M"))

def is_account_receiving_open():
    return account_receiving_open

async def start_scheduler(bot=None):
    scheduler = AsyncIOScheduler(timezone=TZ)

    scheduler.add_job(open_account_receiving, 'cron', hour=OPEN_HOUR, minute=0)
    scheduler.add_job(close_account_receiving, 'cron', hour=CLOSE_HOUR, minute=0)

    # Start scheduler
    scheduler.start()

    # Yanzu lokaci nawa ne? Domin kunna initial flag
    now = get_current_time_wat().time()
    if time(OPEN_HOUR) <= now < time(CLOSE_HOUR):
        await open_account_receiving()
    else:
        await close_account_receiving()
