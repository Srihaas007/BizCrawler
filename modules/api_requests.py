# modules/api_requests.py

import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config.settings import HEADERS, API_URLS


def create_session():
    """
    Create a requests session with retry logic to handle transient network issues.

    Returns:
        session (requests.Session): A configured session object.
    """
    session = requests.Session()
    retries = Retry(
        total=5,                # Retry up to 5 times
        backoff_factor=1,       # Wait 1s, 2s, 4s, etc., between retries
        status_forcelist=[500, 502, 503, 504],  # Retry on specific server errors
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def query_osm_businesses(session, lat, lon, radius_km, business_type):
    """
    Query OpenStreetMap via Overpass for nodes, ways, and relations of a certain business type
    within a certain radius (in meters).

    Args:
        session (requests.Session): The session to use for HTTP requests.
        lat (float): Center latitude.
        lon (float): Center longitude.
        radius_km (int): Search radius in kilometers.
        business_type (str): Type of business (e.g. 'lawyer', 'accountant').

    Returns:
        list: A list of elements (nodes, ways, relations) returned by Overpass.
    """
    # Overpass Query
    # ( ... ) => Union of node, way, relation
    # (around:R, lat, lon) => Query objects around lat/lon within R meters
    # out center => For ways/relations, returns a center coordinate as well
    query = f"""
    [out:json][timeout:60];
    (
      node["office"="{business_type}"](around:{radius_km * 1000},{lat},{lon});
      way["office"="{business_type}"](around:{radius_km * 1000},{lat},{lon});
      relation["office"="{business_type}"](around:{radius_km * 1000},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """

    for url in API_URLS:
        try:
            response = session.get(url, params={"data": query}, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("elements", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Error querying {url}: {e}")
            continue

    logging.error("All Overpass API endpoints failed. Returning empty list.")
    return []
