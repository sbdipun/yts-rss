import os
from dotenv import load_dotenv

# Load environment variables from .env file (only in local dev)
load_dotenv()

# Environment-based Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Optional values
# config.py
YTS_RSS_URL = os.getenv("RSS_URL", "https://yts.mx/rss/0/all/all/0/all")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "2"))
HDENCODE_RSS_URL = os.getenv("HDENCODE_RSS_URL", "https://hdencode.org/feed/?sfw=pass1747284999")
TBL_BASE_URL = os.getenv("TBL_BASE_URL", "https://www.1tamilblasters.earth/")
