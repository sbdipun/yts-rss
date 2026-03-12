import os
import logging
import hashlib
import requests

# File where we store already posted items
POSTED_ITEMS_FILE = "posted_items.txt"
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
DEDUP_PREFIX = os.getenv("DEDUP_PREFIX", "yts-rss:posted")
DEDUP_TTL_SECONDS = int(os.getenv("DEDUP_TTL_SECONDS", "0"))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def _hash_item_id(item_id):
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def _add_and_check_item_redis(item_id):
    if not UPSTASH_REDIS_REST_URL or not UPSTASH_REDIS_REST_TOKEN:
        return None

    hashed_id = _hash_item_id(item_id)
    redis_key = f"{DEDUP_PREFIX}:{hashed_id}"
    headers = {
        "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
        "Content-Type": "application/json",
    }

    command = ["SET", redis_key, "1", "NX"]
    if DEDUP_TTL_SECONDS > 0:
        command.extend(["EX", str(DEDUP_TTL_SECONDS)])

    try:
        response = requests.post(
            UPSTASH_REDIS_REST_URL.rstrip("/"),
            headers=headers,
            json=command,
            timeout=15,
        )
        response.raise_for_status()
        result = response.json().get("result")
        return result == "OK"
    except Exception as e:
        logger.error(f"Upstash dedupe failed, falling back to local file: {e}")
        return None


def load_posted_items():
    """Load previously posted item IDs from file."""
    if not os.path.exists(POSTED_ITEMS_FILE):
        return set()

    try:
        with open(POSTED_ITEMS_FILE, "r") as f:
            return set(line.strip() for line in f.readlines())
    except Exception as e:
        logging.error(f"Error loading posted items: {e}")
        return set()


def save_posted_item(item_id):
    """Save a new item ID to the file."""
    try:
        with open(POSTED_ITEMS_FILE, "a") as f:
            f.write(f"{item_id}\n")
        return True
    except Exception as e:
        logging.error(f"Error saving posted item: {e}")
        return False


def add_and_check_item(item_id):
    """Check if item is new, and add it using Upstash Redis or local file fallback."""
    redis_result = _add_and_check_item_redis(item_id)
    if redis_result is not None:
        return redis_result

    posted_items = load_posted_items()
    if item_id in posted_items:
        return False  # Already posted
    save_posted_item(item_id)
    return True  # New item
