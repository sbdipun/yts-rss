import cloudscraper
import xml.etree.ElementTree as ET
import re

def fetch_rss_feed(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    response.raise_for_status()
    return response.content


def extract_items(rss_content):
    root = ET.fromstring(rss_content)
    items = []

    for item in root.findall('.//item'):
        title_elem = item.find('title')
        link_elem = item.find('link')

        if title_elem is None or link_elem is None:
            logging.warning("Skipping invalid item (missing title or link)")
            continue

        title = title_elem.text.strip()
        link = link_elem.text.strip()

        items.append({
            'title': title,
            'torrent_link': link,
            'size': 'N/A',  # Not available in this feed
        })

    return items
