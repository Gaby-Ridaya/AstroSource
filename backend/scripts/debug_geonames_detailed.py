#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=== DEBUG GEONAMES DÉTAILLÉ ===")

GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")
print(f"GEONAMES_USERNAME: {GEONAMES_USERNAME}")


def get_lat_lon_debug(city, country=None):
    url = "http://api.geonames.org/searchJSON"
    params = {"q": city, "maxRows": 1, "username": GEONAMES_USERNAME}
    if country:
        params["country"] = country

    print(f"URL: {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text[:500]}...")

        data = response.json()
        print(f"JSON data: {data}")

        if data["totalResultsCount"] == 0:
            print("No results found")
            return None

        geo = data["geonames"][0]
        lat, lng = geo["lat"], geo["lng"]
        print(f"Found coordinates: {lat}, {lng}")
        return lat, lng

    except Exception as e:
        print(f"Exception: {e}")
        import traceback

        traceback.print_exc()
        return None


# Test
result = get_lat_lon_debug("Paris", "France")
print(f"Final result: {result}")
