# modules/data_processing.py

import pandas as pd
import os
import logging
from config.settings import OUTPUT_DIR

def save_to_csv(data, sector):
    """
    Save scraped data to a CSV file in the output directory.

    Args:
        data (list of dict): A list of dictionary items containing business info.
        sector (str): The business sector (used in the filename).
    """
    if not data:
        logging.warning("No data to save. The data list is empty.")
        return

    df = pd.DataFrame(data)
    output_csv = os.path.join(OUTPUT_DIR, f"{sector}_business_data.csv")
    df.to_csv(output_csv, index=False)
    logging.info(f"Data saved to {output_csv}")
