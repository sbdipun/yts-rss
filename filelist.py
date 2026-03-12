import logging
import re
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def extract_filelist_items(rss_content):
    """
    Parse Filelist RSS XML and return:
    [
      {
        "name": "<title>",
        "link": "<link>",
        "size": "<size or N/A>"
      }
    ]
    """
    try:
        root = ET.fromstring(rss_content)
        items = []

        for item in root.findall(".//item"):
            title_elem = item.find("title")
            link_elem = item.find("link")
            description_elem = item.find("description")

            if title_elem is None or link_elem is None:
                logger.warning("Skipping Filelist item: missing title or link")
                continue

            name = (title_elem.text or "").strip()
            link = (link_elem.text or "").strip()
            description = (description_elem.text or "").strip() if description_elem is not None else ""

            size_match = re.search(r"Size:\s*([\d.]+\s*[GMK]B(?:\s*i?B)?)", description, re.IGNORECASE)
            if not size_match:
                size_match = re.search(r"Size:\s*([^ ]+\s*[GMK]B)", description, re.IGNORECASE)
            size = size_match.group(1).strip() if size_match else "N/A"

            items.append({
                "name": name,
                "link": link,
                "size": size,
            })

        logger.info(f"Extracted {len(items)} items from Filelist feed")
        return items
    except ET.ParseError as e:
        logger.error(f"Error parsing Filelist RSS XML: {e}")
        return []
