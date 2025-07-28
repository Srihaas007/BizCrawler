# modules/api_requests.py

import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from config.settings import HEADERS, API_URLS

def create_session():
    """
    Create a requests session with retry logic.
    """
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

def build_overpass_query(area_name, tag_list, timeout=120):
    """
    Build an Overpass query string for a list of OSM tags within a named area (e.g. "England").
    
    Args:
        area_name (str): Name of the area in OSM (e.g., "England").
        tag_list (list of dict): List of dictionaries, e.g. [{"amenity": "care_home"}, {"social_facility": "nursing_home"}].
        timeout (int): Overpass query timeout (seconds).
        
    Returns:
        str: A complete Overpass QL query string.
    """
    # Start with a standard Overpass header
    query = f'[out:json][timeout:{timeout}];\n'
    # Reference the area by name
    query += f'area["name"="{area_name}"]->.searchArea;\n'
    query += '(\n'

    # Build sub-queries for each key-value in the tag list
    for tag_dict in tag_list:
        for key, val in tag_dict.items():
            query += f'  node["{key}"="{val}"](area.searchArea);\n'
            query += f'  way["{key}"="{val}"](area.searchArea);\n'
            query += f'  relation["{key}"="{val}"](area.searchArea);\n'

    query += ');\n'
    query += 'out center;\n'
    query += '>;\n'
    query += 'out skel qt;'
    return query

def query_osm_tags_in_area(session, area_name, tag_list, timeout=120):
    """
    Query Overpass for multiple tag variations (from tag_list) in the specified OSM area.
    
    Args:
        session (requests.Session): A session with retry logic.
        area_name (str): For example, "England" or "Wales".
        tag_list (list of dict): E.g., [{"amenity":"care_home"}, {"social_facility":"nursing_home"}].
        timeout (int): Overpass query timeout in seconds.
        
    Returns:
        list: A list of OSM elements (nodes/ways/relations).
    """
    # Build the query
    query_str = build_overpass_query(area_name, tag_list, timeout=timeout)

    # Attempt to fetch data from each API URL in the list
    for url in API_URLS:
        try:
            response = session.get(url, params={"data": query_str}, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("elements", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Error querying {url}: {e}")
            continue

    logging.error("All Overpass API endpoints failed. Returning empty list.")
    return []
