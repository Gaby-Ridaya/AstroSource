#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

import sys

print("=== DEBUG GEONAMES ===")
print("Current dir:", os.getcwd())

try:
    from astro_calcule import get_lat_lon

    print("✓ get_lat_lon imported successfully")

    geonames_user = os.getenv("GEONAMES_USERNAME")
    print(f"GEONAMES_USERNAME: {geonames_user}")

    print("Testing get_lat_lon for Paris...")
    coords = get_lat_lon("Paris", "France")
    print(f"Result: {coords}")

    if coords:
        lat, lon = coords
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("No coordinates returned")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback

    traceback.print_exc()
