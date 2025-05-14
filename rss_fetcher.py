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
        title = item.find('title').text
        description = item.find('description').text

        size_match = re.search(r'Size:\s*([\d.]+ MB)', description)
        if not size_match:
            size_match = re.search(r'(\d+\.\d+\s*[MG]B)', description, re.IGNORECASE)

        size = size_match.group(1) if size_match else 'N/A'

        enclosure = item.find('enclosure')
        torrent_link = enclosure.get('url') if enclosure is not None else 'N/A'

        items.append({
            'title': title,
            'size': size,
            'torrent_link': torrent_link
        })

    return items
