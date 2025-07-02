import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

DB_NAME = "data.db"

# Lokutan aiki (WAT timezone)
OPEN_HOUR = 8   # 8:00 AM
CLOSE_HOUR = 22 # 10:00 PM

# Default 2FA password
DEFAULT_2FA_PASSWORD = "Bashir@111#"
