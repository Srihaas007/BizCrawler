# config/settings.py

import os
import logging
from fake_useragent import UserAgent

# Directory to store outputs (CSV, logs, etc.)
OUTPUT_DIR = "data/output/"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Log file configuration
LOG_FILE = "process_log.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# User Agent headers for HTTP requests
HEADERS = {"User-Agent": UserAgent().random}

# Overpass API endpoints
API_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]
