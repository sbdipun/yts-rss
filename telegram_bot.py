import logging
import requests
from deduplicator import add_and_check_item

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def post_to_telegram(bot_token, chat_id, items):
    logging.info(f"Using bot token: {bot_token}")
    logging.info(f"Sending to chat_id: {chat_id}")
    logging.info(f"Found {len(items)} items to process")
    new_items_posted = 0

    for item in items:
        item_id = item['title']  # Or use item['torrent_link']

        if not add_and_check_item(item_id):
            logging.info(f"Skipping duplicate: {item['title']}")
            continue

        message = (
            f"🎬 <b>{item['title']}</b>\n"
            f"📦 <b>Size: {item['size']}</b>\n\n"
            f"🔗 Torrent: <pre><code>{item['torrent_link']}</code></pre>"
        )

        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(send_url, data=payload)
            if response.status_code == 200:
                logging.info(f"Posted: {item['title']}")
                new_items_posted += 1
            else:
                 logging.error(f"Failed to post {item['title']}: {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"Exception posting {item['title']}: {e}")

    if new_items_posted == 0:
        logging.info("No new items to post.")
