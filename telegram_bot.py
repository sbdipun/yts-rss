from telegram import Bot
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def post_to_telegram(bot_token, chat_id, items):
    bot = Bot(token=bot_token)
    for item in items:
        message = (
            f"🎬 <b>{item['title']}</b>\n"
            f"📦 Size: {item['size']}\n"
            f"🔗 Torrent: <a href='{item['torrent_link']}'>Download</a>"
        )
        try:
            bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
            logging.info(f"Posted: {item['title']}")
        except Exception as e:
            logging.error(f"Failed to post {item['title']}: {e}")
