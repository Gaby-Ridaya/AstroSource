import os
import requests
from dotenv import load_dotenv

# Charger la clé depuis le fichier .env
load_dotenv()
GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")

def get_lat_lon(city, country=None):
    url = "http://api.geonames.org/searchJSON"
    params = {
        "q": city,
        "maxRows": 1,
        "username": GEONAMES_USERNAME
    }
    if country:
        params["country"] = country
    response = requests.get(url, params=params)
    data = response.json()
    if data["totalResultsCount"] == 0:
        return None
    geo = data["geonames"][0]
    return geo["lat"], geo["lng"]

# Exemple d'utilisation
if __name__ == "__main__":
    ville = input("Nom de la ville : ")
    pays = input("Code pays (optionnel, ex: FR) : ").strip() or None
    result = get_lat_lon(ville, pays)
    if result:
        print(f"Latitude : {result[0]}, Longitude : {result[1]}")
    else:
        print("Ville non trouvée.")