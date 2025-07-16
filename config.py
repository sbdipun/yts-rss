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
TMV_BASE_URL = os.getenv("TMV_BASE_URL", "https://www.1tamilmv.onl/")
BWTORRENTS_RSS_URL = os.getenv(
    "BWTORRENTS_RSS_URL",
    " https://bwtorrents.cc/rss.php?cat=145,120,188,125,116,124,114,117,189,190,113,118,115,121,119,194,192,128,132,129,130,127,131,141,140&passkey=22e2c513c1f2f48b8e9c126f537c9903"
)
TORRENTING_RSS_URL = os.getenv("TORRENTING_RSS_URL", "https://torrenting.com/t.rss?49;47;38;11;3;40;1;18;u=1767736;tp=bnpjvcnhvnxqihbcxbokpcojzopxdgnt;DaddyCooL;private;do-not-share")
