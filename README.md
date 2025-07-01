# 🤖 BASH TGB HUB - Hausa Version

Wannan bot ne da aka rubuta da Aiogram 3 domin sauƙaƙe karɓar Telegram accounts daga masu siyarwa, da kuma sarrafa bukatun cire kuɗi daga admin. Wannan version ɗin yana amfani da yaren Hausa kawai (za a iya faɗaɗa zuwa Turanci daga baya).

## ✅ Fasalulluka
- Karɓar accounts daga 8:00AM zuwa 10:00PM (Nigeria time)
- Karɓar lambar waya da OTP daga mai siyarwa
- Karɓar bayanin banki don biya
- Admin yana duba accounts da biyan kuɗi
- Auto open/close system na karɓar accounts
- SQLite database domin tracking

## 📁 Tsarin Fayil

. ├── main.py ├── config.py ├── .env ├── scheduler.py ├── utils/ │   └── database.py ├── handlers/ │   ├── user.py │   └── admin.py ├── requirements.txt

## ⚙️ Saita .env File

BOT_TOKEN=SAKA_TOKEN_DINKA ADMIN_ID=7958281142 CHANNEL_ID=-1002839743918 TIMEZONE=Africa/Lagos

## ▶️ Gudanar da Bot
```bash
pip install -r requirements.txt
python main.py
```bash

## 🧾 Admin Commands

/user_accounts [user_id]

/mark_paid [user_id] [adadin]

/completed_today_payment


---
