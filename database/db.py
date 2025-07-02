import aiosqlite

DB_NAME = "data.db"

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phone_number TEXT UNIQUE,
                status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payment_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                bank_info TEXT,
                status TEXT DEFAULT 'pending',
                requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                paid_at DATETIME
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS delivered_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                buyer_id INTEGER,
                delivered_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS paid_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phone_number TEXT,
                paid_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
