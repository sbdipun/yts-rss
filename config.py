import os

# Environment-based Config
TELEGRAM_BOT_TOKEN = os.getenv("7607848214:AAH-FURy_kD1Vybj5WvHb_hseWqnF8QE83k")
TELEGRAM_CHANNEL_ID = os.getenv("-1001651019056")

# Optional values
RSS_URL = os.getenv("RSS_URL", "https://yts.mx/rss/0/all/all/0/all ")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "2"))
