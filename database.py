import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    lang TEXT DEFAULT 'ha'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    phone TEXT UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bank_info TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
)
""")

conn.commit()

def phone_exists(phone: str) -> bool:
    cursor.execute("SELECT 1 FROM accounts WHERE phone = ?", (phone,))
    return cursor.fetchone() is not None

def save_account(user_id: int, phone: str):
    cursor.execute("INSERT OR IGNORE INTO accounts (user_id, phone) VALUES (?, ?)", (user_id, phone))
    conn.commit()

def save_withdrawal(user_id: int, info: str):
    cursor.execute("INSERT INTO withdrawals (user_id, bank_info) VALUES (?, ?)", (user_id, info))
    conn.commit()

def get_user_accounts(user_id: int):
    cursor.execute("SELECT phone FROM accounts WHERE user_id = ? AND status = 'pending'", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def count_user_accounts(user_id: int) -> int:
    cursor.execute("SELECT COUNT(*) FROM accounts WHERE user_id = ? AND status = 'pending'", (user_id,))
    return cursor.fetchone()[0]

def mark_accounts_paid(user_id: int, count: int):
    cursor.execute("""
        UPDATE accounts SET status = 'paid'
        WHERE user_id = ? AND status = 'pending'
        LIMIT ?
    """, (user_id, count))
    conn.commit()
