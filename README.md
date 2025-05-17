# 🎬 RSS-to-Telegram Torrent Poster Bot

A modular Python bot that scrapes multiple torrent sites (including non-RSS ones), filters new content, and posts them to a Telegram channel with clean formatting.

Supports:
- ✅ YTS (via RSS)
- ✅ HD Encode (via RSS)
- ✅ TBL-style custom sites (via scraping)
- ✅ TMV-style custom sites (via scraping)

Built with:
- Flask (for health check)
- APScheduler (background job runner)
- BeautifulSoup & Requests (HTML parsing + scraping)
- python-telegram-bot / raw Telegram API
- Deduplication logic

---

## 🧠 Features

| Feature | Description |
|--------|-------------|
| 🔁 Multiple Sources | Supports RSS feeds + custom scraped sites |
| 📺 TV Shows & Movies | Different formatting by source |
| 🧹 Deduplication | Prevents reposting the same torrents |
| ⚙️ Configurable | Set everything via environment variables |
| 🌐 Deployable | Works on Render, Heroku, or local server |
| ⏱️ Scheduler | Posts at regular intervals using APScheduler |

---

## 📦 File Structure
