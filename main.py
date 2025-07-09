import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

# Local imports
from rss_fetcher import fetch_rss_feed, extract_items
from hdencode_rss import fetch_hdencode_feed, parse_hdencode_feed
from telegram_bot import post_to_telegram
from tbl import scrape_links  # 👈 Newly added import
from tmv import tmv_scrape_links
from bwt import extract_bwt_items
import config

# === Logging Setup ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Confirm app started and show environment
logger.info("App started")
logger.info(f"Environment: {dict(os.environ)}")

# === Flask App ===
app = Flask(__name__)

@app.route('/')
def index():
    return "RSS Telegram Poster is running!"

# === Scheduled Job ===
def scheduled_job():
    logging.info("Fetching and processing RSS feeds...")

    all_items = []

    # --- Process YTS Feed ---
    try:
        yts_url = config.YTS_RSS_URL
        logging.info(f"Fetching YTS feed from {yts_url}")
        rss_content = fetch_rss_feed(yts_url)
        yts_items = extract_items(rss_content)
        all_items.extend(yts_items)
    except Exception as e:
        logging.error(f"Error processing YTS feed: {e}")

    # --- Process HD Encode Feed ---
    try:
        hde_url = config.HDENCODE_RSS_URL
        logging.info(f"Fetching HD Encode feed from {hde_url}")
        hde_content = fetch_hdencode_feed(hde_url)
        hde_items = parse_hdencode_feed(hde_content)
        all_items.extend(hde_items)
    except Exception as e:
        logging.error(f"Error processing HD Encode feed: {e}")

     # --- Process TBL Feed (Custom Scraped Site) ---
    try:
        logging.info("Fetching TBL torrents...")
        tbl_items = scrape_links()  # From tbl.py
        all_items.extend(tbl_items)
    except Exception as e:
        logging.error(f"Error processing TBL feed: {e}")

    # --- Process TMV Feed (Custom Scraped Site) ---
    try:
        logging.info("Fetching TMV torrents...")
        tmv_items = tmv_scrape_links()  # From tbl.py
        all_items.extend(tmv_items)
    except Exception as e:
        logging.error(f"Error processing TMV feed: {e}")

     # --- Process BW Torrents Feed ---
    try:
        logger.info("Fetching BW Torrents feed...")
        bwt_url = config.BWTORRENTS_RSS_URL
        bwt_content = fetch_rss_feed(bwt_url)
        bwt_items = extract_bwt_items(bwt_content)
        all_items.extend(bwt_items)
    except Exception as e:
        logger.error(f"Error fetching BW Torrents feed: {e}")

    # --- Post Results ---
    if all_items:
        try:
            post_to_telegram(
                bot_token=config.TELEGRAM_BOT_TOKEN,
                chat_id=config.TELEGRAM_CHANNEL_ID,
                items=all_items
            )
        except Exception as e:
            logging.error(f"Error during telegram posting: {e}")
    else:
        logging.info("No items found across any feeds.")

# === Initialize Scheduler ===
try:
    scheduler = BackgroundScheduler()

    # Only add job if not already added
    if not scheduler.get_jobs():
        scheduler.add_job(
            scheduled_job,
            'interval',
            minutes=config.CHECK_INTERVAL_MINUTES,
            max_instances=3
        )
        scheduler.start()
        logging.info(f"Scheduler started. Checking every {config.CHECK_INTERVAL_MINUTES} minute(s).")
    else:
        logging.warning("Scheduler job already exists.")
except Exception as e:
    logging.error(f"Failed to initialize scheduler: {e}")
