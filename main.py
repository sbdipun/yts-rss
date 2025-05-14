import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import time

# Local imports
from rss_fetcher import fetch_rss_feed, extract_items
from telegram_bot import post_to_telegram
import config

# === Logging Setup ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Flask App ===
app = Flask(__name__)

@app.route('/')
def index():
    return "RSS Telegram Poster is running!"

# === Scheduler Job ===
def scheduled_job():
    logging.info("Fetching RSS feed...")
    try:
        rss_content = fetch_rss_feed(config.RSS_URL)
        items = extract_items(rss_content)
        post_to_telegram(
            bot_token=config.TELEGRAM_BOT_TOKEN,
            chat_id=config.TELEGRAM_CHANNEL_ID,
            items=items
        )
    except Exception as e:
        logging.error(f"Error during job execution: {e}")

# === Start Scheduler ===
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
    scheduled_job,
    'interval',
    minutes=config.CHECK_INTERVAL_MINUTES,
    max_instances=1
)
    scheduler.start()
    logging.info(f"Scheduler started. Checking every {config.CHECK_INTERVAL_MINUTES} minute(s).")

# === Run App ===
if __name__ == '__main__':
    start_scheduler()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000)
