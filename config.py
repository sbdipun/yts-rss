import os
from dotenv import load_dotenv

# Load environment variables from .env file (only in local dev)
load_dotenv()

# Environment-based Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Feed/source values (set in .env / Render env vars)
YTS_RSS_URL = os.getenv("YTS_RSS_URL", "")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "2"))
HDENCODE_RSS_URL = os.getenv("HDENCODE_RSS_URL", "")
TBL_BASE_URL = os.getenv("TBL_BASE_URL", "")
TMV_BASE_URL = os.getenv("TMV_BASE_URL", "")
BWTORRENTS_RSS_URL = os.getenv("BWTORRENTS_RSS_URL", "")
TORRENTING_RSS_URL = os.getenv("TORRENTING_RSS_URL", "")
SHARESPARK_RSS_URL = os.getenv("SHARESPARK_RSS_URL", "")
FILELIST_RSS_URL = os.getenv("FILELIST_RSS_URL", "")
