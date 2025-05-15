import logging
import xml.etree.ElementTree as ET
import requests

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def fetch_hdencode_feed(url):
    """
    Fetches the HD Encode RSS feed from the given URL.
    """
    try:
        logger.info(f"Fetching HD Encode feed from {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error(f"Error fetching HD Encode feed: {e}")
        return None


def parse_hdencode_feed(rss_content):
    """
    Parses HD Encode RSS feed and extracts title and link.
    Returns list of items with 'title' and 'torrent_link'
    """
    if rss_content is None:
        logger.warning("No RSS content to parse.")
        return []

    try:
        root = ET.fromstring(rss_content)
        items = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            link_elem = item.find('link')

            if title_elem is None or link_elem is None:
                logger.warning("Skipping item: missing title or link")
                continue

            title = title_elem.text.strip()
            torrent_link = link_elem.text.strip()

            items.append({
                'title': title,
                'torrent_link': torrent_link,
                'source': 'HDENCODE'
            })

        logger.info(f"Parsed {len(items)} items from HD Encode feed")
        return items

    except ET.ParseError as e:
        logger.error(f"Error parsing HD Encode feed XML: {e}")
        return []
