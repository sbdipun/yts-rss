# bwt.py

import logging
import xml.etree.ElementTree as ET
import re
from config import BWTORRENTS_RSS_URL
from rss_fetcher import fetch_rss_feed  # Reuse cloudscraper logic from rss_fetcher.py

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def extract_bwt_items(rss_content):
    """
    Extracts items from BW Torrents RSS feed.
    Returns list of dicts with title, size, torrent_link, source
    """
    try:
        root = ET.fromstring(rss_content)
        items = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            description_elem = item.find('description')
            link_elem = item.find('link')

            if title_elem is None or description_elem is None or link_elem is None:
                logger.warning("Skipping item: missing required fields")
                continue

            title = title_elem.text.strip()
            description = description_elem.text.strip()

            # Extract size using regex
            size_match = re.search(r'Size:\s*([\d.]+\s*[GMK]B|[\d]+\s*[GMK]iB)', description, re.IGNORECASE)
            size = size_match.group(1) if size_match else "N/A"

            torrent_link = link_elem.text.strip()  # This is usually a magnet link or details page

            items.append({
                'title': title,
                'size': size,
                'torrent_link': torrent_link,
                'source': 'bwt'
            })

        logger.info(f"Extracted {len(items)} items from BW Torrents feed")
        return items

    except ET.ParseError as e:
        logger.error(f"Error parsing BW Torrents feed XML: {e}")
        return []
