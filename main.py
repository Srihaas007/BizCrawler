import logging

from modules.api_requests import create_session, query_osm_tags_in_area
from modules.scraping import scrape_emails_and_phone
from modules.data_processing import save_to_csv

def main():
    """
    Main function to query restaurants, pizza shops, burger shops, and other food establishments.
    """
    # 1. Create an HTTP session with retries
    session = create_session()

    # 2. Define your array of tags for food establishments
    food_establishments_tags = [
        {"amenity": "restaurant"},        # Restaurants
        {"amenity": "fast_food"},         # Fast Food Chains
        {"cuisine": "pizza"},             # Pizza Shops
        {"cuisine": "burger"},            # Burger Shops
        {"cuisine": "chinese"},           # Chinese Restaurants
        {"cuisine": "indian"},            # Indian Restaurants
        {"cuisine": "mexican"},           # Mexican Restaurants
        {"cuisine": "japanese"},          # Japanese Restaurants
        {"cuisine": "kebab"},             # Kebab Shops
        {"cuisine": "italian"},           # Italian Restaurants
    ]

    # 3. Query Overpass (all of England for these tags)
    logging.info("Querying Overpass for food establishments in England...")
    results = query_osm_tags_in_area(session, area_name="England", tag_list=food_establishments_tags, timeout=300)

    # 4. Process and scrape websites
    businesses = []
    unique_ids = set()

    for element in results:
        elem_id = element.get("id")
        if elem_id in unique_ids:
            continue
        unique_ids.add(elem_id)

        tags = element.get("tags", {})
        name = tags.get("name", "N/A")
        website = tags.get("website", "")
        street = tags.get("addr:street", "")
        city = tags.get("addr:city", "")
        postcode = tags.get("addr:postcode", "")
        address = ", ".join([street, city, postcode]).strip(", ")

        phone = tags.get("phone", "N/A")
        email = tags.get("email", "N/A")

        # Scrape the website for additional contact info if available
        additional_emails, additional_phones = [], []
        if website.startswith("http"):
            scraped_emails, scraped_phones = scrape_emails_and_phone(website)
            additional_emails = scraped_emails
            additional_phones = scraped_phones

        # Only add rows with meaningful data
        if name != "N/A" or address != "N/A" or phone != "N/A" or email != "N/A" or website != "N/A":
            businesses.append({
                "id": elem_id,
                "name": name,
                "address": address if address else "N/A",
                "phone": phone,
                "email": email,
                "website": website if website else "N/A",
                "additional_emails": ", ".join(additional_emails) if additional_emails else "N/A",
                "additional_phones": ", ".join(additional_phones) if additional_phones else "N/A"
            })

    # 5. Save results to CSV
    save_to_csv(businesses, filename="food_establishments_in_england.csv")
    logging.info("Data saved. Done!")

if __name__ == "__main__":
    main()
