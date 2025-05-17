# tbl.py

import logging
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
from config import TBL_BASE_URL

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Base URL of the site you're scraping
TBL_BASE_URL = "https://www.1tamilblasters.earth/"  # Replace with real URL

def scrape_links():
    """
    Scrapes the latest torrents from a non-RSS torrent site.
    Returns list of items like:
    {
        'title': title,
        'torrent_link': magnet_link,
        'source': 'tbl'
    }
    """
    try:
        logger.info(f"Fetching base page: {TBL_BASE_URL}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
        }
        response = requests.get(TBL_BASE_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='ipsType_break ipsContained')

        if not divs:
            logger.warning("No divs found with class 'ipsType_break ipsContained'.")
            return []

        logger.info(f"Found {len(divs)} torrents on the page")

        results = []
        for div in divs[:10]:  # Limit to 10 items
            link_tag = div.find('a')
            if not link_tag or not link_tag.has_attr('href'):
                logger.warning("Skipping item: missing link tag or href attribute")
                continue

            link = link_tag['href']
            logger.debug(f"Fetching subpage: {link}")

            try:
                sub_response = requests.get(link, headers=headers)
                sub_response.raise_for_status()
                sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                magnet_tag = sub_soup.find('a', class_='magnet-plugin')

                if magnet_tag and magnet_tag.has_attr('href'):
                    magnet_link = magnet_tag['href']

                    # Extract title from magnet link
                    query_params = re.search(r'dn=([^&]+)', magnet_link)
                    title = query_params.group(1) if query_params else 'Unknown Title'
                    decoded_title = urllib.parse.unquote(title)

                    results.append({
                        'title': decoded_title,
                        'torrent_link': magnet_link,
                        'source': 'tbl'
                    })
                else:
                    logger.warning(f"No magnet link found on subpage: {link}")

            except requests.RequestException as e:
                logger.error(f"Failed to fetch subpage {link}: {e}")
            except Exception as e:
                logger.exception(f"Error parsing subpage {link}: {e}")

        logger.info(f"Scraped {len(results)} items from TBL")
        return results

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error during scraping: {e}")
        return []
