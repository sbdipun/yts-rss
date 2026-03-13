import os
import logging
import hashlib
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "yts_rss")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "posted_items")
POSTED_ITEMS_FILE = "posted_items.txt"

logger = logging.getLogger(__name__)
_index_initialized = False


def _hash_item_id(item_id):
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def _get_collection():
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI is not set")

    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGODB_DB]
    return db[MONGODB_COLLECTION]


def _ensure_index(collection):
    global _index_initialized
    if _index_initialized:
        return

    collection.create_index("item_hash", unique=True)
    _index_initialized = True


def _load_posted_items():
    if not os.path.exists(POSTED_ITEMS_FILE):
        return set()

    try:
        with open(POSTED_ITEMS_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        logger.error(f"Error loading local dedupe file: {e}")
        return set()


def _save_posted_item(item_id):
    try:
        with open(POSTED_ITEMS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item_id}\n")
        return True
    except Exception as e:
        logger.error(f"Error saving local dedupe file: {e}")
        return False


def _add_and_check_item_file(item_id):
    posted_items = _load_posted_items()
    if item_id in posted_items:
        return False
    _save_posted_item(item_id)
    return True


def add_and_check_item(item_id):
    """Check if item is new using MongoDB deduplication collection."""
    item_hash = _hash_item_id(item_id)

    try:
        collection = _get_collection()
        _ensure_index(collection)
        collection.insert_one(
            {
                "item_hash": item_hash,
                "item_id": item_id,
            }
        )
        return True
    except DuplicateKeyError:
        return False
    except Exception as e:
        logger.error(f"MongoDB dedupe failed for item '{item_id}': {e}")
        return _add_and_check_item_file(item_id)
