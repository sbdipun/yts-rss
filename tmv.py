# tmv.py

import logging
import requests
from bs4 import BeautifulSoup
import html
import os
from config import TMV_BASE_URL

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Base URL of the site
TMV_BASE_URL = "https://www.1tamilmv.fi/"  # Replace with real URL

def scrape_with_scraperapi(url):
    """
    Fetches HTML content from a given URL using standard requests.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
        }
        logger.info(f"Fetching TMV base page via requests: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


def tmv_scrape_links():
    """
    Scrapes latest torrents from TMV site.
    Returns list of items like:
    {
        'title': file_name,
        'torrent_link': torrent_link,
        'source': 'tmv'
    }
    """
    try:
        logger.info(f"Fetching TMV feed from {TMV_BASE_URL}")
        base_page_html = scrape_with_scraperapi(TMV_BASE_URL)
        if not base_page_html:
            logger.error("Failed to fetch base page.")
            return []

        soup = BeautifulSoup(base_page_html, 'html.parser')
        divs = soup.find_all('div', class_='ipsType_break ipsContained')

        if not divs:
            logger.warning("No torrents found on TMV site.")
            return []

        links = [div.find('a')['href'] for div in divs[:10] if div.find('a')]

        results = []
        for link in links:
            try:
                logger.debug(f"Fetching subpage: {link}")
                sub_page_html = scrape_with_scraperapi(link)
                if not sub_page_html:
                    logger.warning(f"Failed to fetch subpage: {link}")
                    continue

                sub_soup = BeautifulSoup(sub_page_html, 'html.parser')
                torrent_tags = sub_soup.find_all('a', attrs={'data-fileext': 'torrent'})

                for tag in torrent_tags:
                    if 'href' in tag.attrs:
                        torrent_link = tag['href']
                        file_name = tag.get_text(strip=True)

                        results.append({
                            'title': file_name,
                            'torrent_link': torrent_link,
                            'source': 'tmv'
                        })

                logger.info(f"Found {len(results)} items from TMV")
                return results

            except Exception as e:
                logger.exception(f"Error processing {link}: {e}")

    except Exception as e:
        logger.exception(f"Unexpected error during TMV scraping: {e}")
        return []
