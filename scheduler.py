from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from config import TIMEZONE

IS_OPEN = {"status": True}

def start_scheduler():
    scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))
    scheduler.add_job(lambda: IS_OPEN.update({"status": False}), CronTrigger(hour=22, minute=0))
    scheduler.add_job(lambda: IS_OPEN.update({"status": True}), CronTrigger(hour=8, minute=0))
    scheduler.start()

def is_within_time() -> bool:
    return IS_OPEN["status"]
