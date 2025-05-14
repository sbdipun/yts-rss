import os

# Environment-based Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")     # ← This is correct
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")   # ← This is correct

# Optional values
RSS_URL = os.getenv("RSS_URL", "https://yts.mx/rss/0/all/all/0/all ")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "2"))
