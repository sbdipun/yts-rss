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

## Upstash Redis deduplication

Set these environment variables to enable Redis-backed deduplication:

- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`
- `DEDUP_PREFIX` (optional, default: `yts-rss:posted`)
- `DEDUP_TTL_SECONDS` (optional, default: `0` which means no expiry)

If Upstash variables are not set, the app falls back to local `posted_items.txt`.
