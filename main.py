import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

# Local imports
from rss_fetcher import fetch_rss_feed, extract_items
from telegram_bot import post_to_telegram
import config

# === Logging Setup ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Log environment for debugging
logging.info("App started")
logging.info(f"Environment: {dict(os.environ)}")

# === Flask App ===
app = Flask(__name__)

@app.route('/')
def index():
    return "RSS is running!"

# === Scheduled Job ===
def scheduled_job():
    logging.info("Fetching RSS feeds...")
    all_items = []

    for rss_url in config.RSS_URLS:
        try:
            logging.info(f"Fetching from: {rss_url}")
            rss_content = fetch_rss_feed(rss_url)
            items = extract_items(rss_content)
            all_items.extend(items)
        except Exception as e:
            logging.error(f"Error fetching {rss_url}: {e}")

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
        logging.info("No new items found in any feed.")

# === Initialize Scheduler ===
try:
    scheduler = BackgroundScheduler()

    # Only add job if not already added
    if not scheduler.get_jobs():
        scheduler.add_job(
            scheduled_job,
            'interval',
            minutes=config.CHECK_INTERVAL_MINUTES,
            max_instances=1
        )
        scheduler.start()
        logging.info(f"Scheduler started. Checking every {config.CHECK_INTERVAL_MINUTES} minute(s).")
    else:
        logging.warning("Scheduler job already exists.")
except Exception as e:
    logging.error(f"Failed to initialize scheduler: {e}")
