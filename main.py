# main.py

import logging

# Local modules
from modules.input_handler import get_user_inputs
from modules.api_requests import create_session, query_osm_businesses
from modules.scraping import scrape_emails_and_phone
from modules.data_processing import save_to_csv

def main():
    """
    Main function that:
    1. Gets user input (sector, lat, lon, radius).
    2. Queries Overpass API with a single bounding search to minimize calls.
    3. Scrapes each found business website for additional emails/phones.
    4. Saves the results to a CSV file in the 'data/output' folder.
    """
    # 1. Prompt user for inputs
    sector, center_lat, center_lon, radius_km = get_user_inputs()

    # 2. Create an HTTP session with retries
    session = create_session()
    logging.info(f"Starting Overpass query for '{sector}' within {radius_km} km around ({center_lat}, {center_lon}).")

    # 3. Perform the Overpass query
    overpass_data = query_osm_businesses(session, center_lat, center_lon, radius_km, sector)

    # 4. Gather data and avoid duplicates by tracking element IDs
    businesses = []
    unique_ids = set()

    for element in overpass_data:
        element_id = element.get("id")
        if element_id in unique_ids:
            continue  # Skip duplicates
        unique_ids.add(element_id)

        tags = element.get("tags", {})
        name = tags.get("name", "N/A")
        website = tags.get("website", None)

        # Construct address from OSM tags
        street = tags.get("addr:street", "")
        city = tags.get("addr:city", "")
        postcode = tags.get("addr:postcode", "")
        address = ", ".join([street, city, postcode]).strip(", ")

        phone_number = tags.get("phone", "N/A")
        email = tags.get("email", "N/A")
        opening_hours = tags.get("opening_hours", "N/A")
        description = tags.get("description", "N/A")

        # If a website is available, scrape it for additional info
        additional_emails, additional_phones = [], []
        if website and website.startswith("http"):
            scraped_emails, scraped_phones = scrape_emails_and_phone(website)
            additional_emails = scraped_emails
            additional_phones = scraped_phones

        businesses.append({
            "name": name,
            "address": address if address else "N/A",
            "website": website if website else "N/A",
            "phone_number": phone_number,
            "email": email,
            "additional_emails": ", ".join(additional_emails) if additional_emails else "N/A",
            "additional_phone_numbers": ", ".join(additional_phones) if additional_phones else "N/A",
            "opening_hours": opening_hours,
            "description": description
        })

    # 5. Save results to CSV
    save_to_csv(businesses, sector)
    logging.info("Scraping complete.")

if __name__ == "__main__":
    main()
