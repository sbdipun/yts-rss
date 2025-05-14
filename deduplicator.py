import os
import logging

# File where we store already posted items
POSTED_ITEMS_FILE = "posted_items.txt"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
    """Check if item is new, and add it to the list if so."""
    posted_items = load_posted_items()
    if item_id in posted_items:
        return False  # Already posted
    save_posted_item(item_id)
    return True  # New item
