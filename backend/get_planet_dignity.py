import json

# Exemple d'utilisation du fichier planetes_dignites.json dans un script

def get_planet_dignity(planet_name, dignities_json_path):
    with open(dignities_json_path, 'r', encoding='utf-8') as f:
        dignities = json.load(f)
    planet_info = dignities.get(planet_name, None)
    if planet_info:
        domicile = planet_info.get('domicile')
        exaltation = planet_info.get('exaltation')
        description = planet_info.get('description')
        return domicile, exaltation, description
    else:
        return None, None, None

# Exemple d'intégration dans le prompt final
# planet = 'Sun'
# domicile, exaltation, description = get_planet_dignity(planet, '/home/gaby/AstroSource/Prompt_art_json/planetes_dignites.json')
# print(f"{planet} — Domicile : {domicile}, Exaltation : {exaltation}\n{description}")
