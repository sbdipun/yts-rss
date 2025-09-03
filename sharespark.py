# sharespark.py

import logging
import xml.etree.ElementTree as ET
import re
from config import SHARESPARK_RSS_URL
from rss_fetcher import fetch_rss_feed  # Reuse cloudscraper logic from rss_fetcher.py

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def extract_sharespark_items(rss_content):
    """
    Extracts items from SHARESPARK RSS feed.
    Returns list of dicts with title, size, link, category
    """
    try:
        root = ET.fromstring(rss_content)
        items = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            category_elem = item.find('category')
            link_elem = item.find('link')

            if title_elem is None or category_elem is None or link_elem is None:
                logger.warning("Skipping item: missing required fields")
                continue

            title = title_elem.text.strip()
            category = category_elem.text.strip()

            torrent_link = link_elem.text.strip()  # This is usually a magnet link or details page

            items.append({
                'title': title,
                'torrent_link': torrent_link,
                'category': category,
                'source': 'sharespark'
            })

        logger.info(f"Extracted {len(items)} items from sharespark feed")
        return items

    except ET.ParseError as e:
        logger.error(f"Error parsing sharespark feed XML: {e}")
        return []
