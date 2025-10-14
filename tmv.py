# tmv.py

import logging
import cloudscraper
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
TMV_BASE_URL = "https://www.1tamilmv.mba/"  # Replace with real URL

def scrape_with_scraperapi(url):
    """
    Fetches HTML content from a given URL using cloudscraper.
    """
    try:
        logger.info(f"Fetching via cloudscraper: {url}")

        # Create a cloudscraper instance
        scraper = cloudscraper.create_scraper()

        # Optional: Add proxy if needed
        use_proxy = True
        proxies = {
            "https": "https": "https://x6DzSR6XnGeLnBLk32UPvjWg:CFcqTXQDxKybUf6qAHTmSxpW@in-mum.prod.surfshark.com:443"
        }

        # Fetch with or without proxy
        if use_proxy:
            response = scraper.get(url, proxies=proxies)
        else:
            response = scraper.get(url)

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

        # Limit to 10 links to prevent timeout
        links = [div.find('a')['href'] for div in divs if div.find('a')]

        logger.debug(f"Found {len(links)} valid links on base page")

        results = []
        for link in links:
            try:
                logger.debug(f"Fetching subpage: {link}")
                sub_page_html = scrape_with_scraperapi(link)

                if not sub_page_html:
                    logger.warning(f"Failed to fetch subpage: {link}")
                    continue

                sub_soup = BeautifulSoup(sub_page_html, 'html.parser')
                torrent_link_tags = sub_soup.find_all('a', attrs={'data-fileext': 'torrent'})

                logger.debug(f"Found {len(torrent_link_tags)} torrent links on {link}")

                for torrent_link_tag in torrent_link_tags:
                    if 'href' in torrent_link_tag.attrs:
                        torrent_link = torrent_link_tag['href']
                        file_name = torrent_link_tag.get_text(strip=True)

                        results.append({
                            "title": file_name,
                            "torrent_link": torrent_link,
                            "description": html.escape("."),
                            "source": "tmv"
                        })

            except Exception as e:
                logger.exception(f"Error processing subpage {link}: {e}")

        logger.info(f"Scraped {len(results)} items from TMV")
        return results

    except Exception as e:
        logger.exception(f"Unexpected error during TMV scraping: {e}")
        return []
