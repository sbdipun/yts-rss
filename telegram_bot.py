from telegram import Bot
import logging
from deduplicator import add_and_check_item

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def post_to_telegram(bot_token, chat_id, items):
    bot = Bot(token=bot_token)
    new_items_posted = 0

    for item in items:
        item_id = item['title']  # You can also use 'torrent_link' if you prefer

        if not add_and_check_item(item_id):
            logging.info(f"Skipping duplicate: {item['title']}")
            continue

        message = (
            f"🎬 <b>{item['title']}</b>\n"
            f"📦 Size: {item['size']}\n"
            f"🔗 Torrent: <a href='{item['torrent_link']}'>Download</a>"
        )
        try:
            bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
            logging.info(f"Posted: {item['title']}")
            new_items_posted += 1
        except Exception as e:
            logging.error(f"Failed to post {item['title']}: {e}")

    if new_items_posted == 0:
        logging.info("No new items to post.")
