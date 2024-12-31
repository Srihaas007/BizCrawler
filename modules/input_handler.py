# modules/input_handler.py

def get_user_inputs():
    """
    Prompt the user for the necessary input parameters.

    Returns:
        sector (str): The business sector or category to search (e.g., 'lawyer').
        lat (float): Center latitude for the search.
        lon (float): Center longitude for the search.
        radius_km (int): Search radius in kilometers.
    """
    sector = input("Enter the business sector (e.g., 'lawyer'): ").strip()
    lat = float(input("Enter the latitude (e.g., 51.509865 for London): ").strip())
    lon = float(input("Enter the longitude (e.g., -0.118092 for London): ").strip())
    radius = int(input("Enter the search radius in kilometers (e.g., 5): ").strip())
    return sector, lat, lon, radius
