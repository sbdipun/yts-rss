# 🎬 RSS-to-Telegram Post Bot

A modular Python bot that scrapes multiple sites (including non-RSS ones), filters new content, and posts them to a Telegram channel with clean formatting.

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

## MongoDB deduplication

Set these environment variables to enable MongoDB-backed deduplication:

- `MONGODB_URI`
- `MONGODB_DB` (optional, default: `yts_rss`)
- `MONGODB_COLLECTION` (optional, default: `posted_items`)

The app creates a unique index on `item_hash` and uses duplicate-key handling to prevent reposts.
