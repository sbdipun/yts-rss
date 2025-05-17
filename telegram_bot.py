import logging
import requests
import time
from deduplicator import add_and_check_item

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def post_to_telegram(bot_token, chat_id, items):
    logger.info(f"Using bot token: {'*' * len(bot_token)}")
    logger.info(f"Sending to chat_id: {chat_id}")
    logger.info(f"Found {len(items)} items to process")

    new_items_posted = 0

    for item in items:
        item_id = item['title']

        if not add_and_check_item(item_id):
            logger.info(f"Skipping duplicate: {item['title']}")
            continue

        # Determine source and set formatting
        source = item.get('source', 'yts').lower()

        if source == 'yts':
            message = (
                f"🎬<b>{item['title']}</b>\n"
                f"📦<b>Size:</b> {item['size']}\n\n"
                f"🧲<b>Torrent:</b>\n"
                f"<code>{item['torrent_link']}</code>"
            )
        elif source == 'hdencode':
            message = (
                f"📺<b>{item['title']}</b>\n\n"
                f"<b>Link:</b>\n"
                f"<code>{item['torrent_link']}</code>"
            )
        else:  # tbl or unknown
            message = (
                f"📀 <b>{item['title']}</b>\n\n"
                f"🧲 <b>Magnet:</b>\n"
                f"<code>{item['torrent_link']}</code>"
            )

        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }

        attempt = 0
        max_retries = 3

        while attempt <= max_retries:
            try:
                response = requests.post(send_url, data=payload)
                if response.status_code == 200:
                    logger.info(f"Posted: {item['title']} ({source.upper()})")
                    new_items_posted += 1
                    break  # Exit loop on success
                elif response.status_code == 429:
                    retry_after = int(response.json().get("parameters", {}).get("retry_after", 5))
                    logger.warning(f"Flood limit hit. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    attempt += 1
                else:
                    logger.error(f"Failed to post {item['title']}: {response.status_code} - {response.text}")
                    break  # Not retryable
            except Exception as e:
                logger.exception(f"Exception posting {item['title']}: {e}")
                break  # Skip on general exception

        time.sleep(1)  # Prevent hitting Telegram rate limits

    if new_items_posted == 0:
        logger.info("No new items to post.")
