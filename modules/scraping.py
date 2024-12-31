# modules/scraping.py

import re
import logging
import requests
from bs4 import BeautifulSoup
from config.settings import HEADERS

def scrape_emails_and_phone(url):
    """
    Scrape emails and phone numbers from a website URL.

    Args:
        url (str): The website URL to scrape.

    Returns:
        (emails, phone_numbers) (tuple of lists): 
            - emails: List of found email addresses.
            - phone_numbers: List of found phone numbers.
    """
    emails, phone_numbers = [], []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Regex for emails
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text)

        # Regex for phone numbers (basic, adjust if needed)
        phone_numbers = re.findall(r"(\+?\d[\d\s-]{7,}\d)", response.text)

        # Convert to sets to remove duplicates
        emails = list(set(emails))
        phone_numbers = list(set(phone_numbers))
    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")

    return emails, phone_numbers
