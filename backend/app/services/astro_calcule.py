"""
Copyright © 2025 Gabriel Alba
Tous droits réservés.
Usage personnel uniquement. Toute utilisation commerciale ou publication nécessite une autorisation écrite.
Voir LICENSE pour les détails.
"""

# --- Imports regroupés et propres ---
import os
import sys
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import aspects
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Charger la clé GeoNames
load_dotenv()
GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")


def get_lat_lon(city, country=None):
    """Retourne (latitude, longitude) pour une ville/pays via GeoNames."""
    url = "http://api.geonames.org/searchJSON"
    params = {"q": city, "maxRows": 1, "username": GEONAMES_USERNAME}
    if country:
        # Convertir les noms de pays en codes ISO
        country_codes = {
            "France": "FR",
            "Belgique": "BE",
            "Suisse": "CH",
            "Canada": "CA",
            "USA": "US",
            "États-Unis": "US",
            "Allemagne": "DE",
            "Italie": "IT",
            "Espagne": "ES",
        }
        country_code = country_codes.get(country, country)
        params["country"] = country_code
    response = requests.get(url, params=params)
    data = response.json()
    if data["totalResultsCount"] == 0:
        return None
    geo = data["geonames"][0]
    return geo["lat"], geo["lng"]


def get_timezone(lat, lon):
    """Retourne le fuseau horaire pour des coordonnées via GeoNames."""
    url = "http://api.geonames.org/timezoneJSON"
    params = {"lat": lat, "lng": lon, "username": GEONAMES_USERNAME}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("timezoneId", "Europe/Paris")  # Valeur par défaut


def local_to_utc(date_str, time_str, tz_str):
    """Convertit une date/heure locale en UTC selon le fuseau horaire."""
    dt_str = f"{date_str} {time_str}"
    dt_naive = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    dt_local = dt_naive.replace(tzinfo=ZoneInfo(tz_str))
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))
    return dt_utc


# --- Refactorisation professionnelle ---
def astro_theme_calcul(nom, date, heure, ville, pays=None):
    """Calcule toutes les données astrologiques pour un utilisateur."""
    # Convertir le format de date si nécessaire (DD/MM/YYYY vers YYYY-MM-DD)
    if "/" in date and len(date.split("/")) == 3:
        parts = date.split("/")
        if len(parts[0]) == 2:
            date = f"{parts[2]}-{parts[1]}-{parts[0]}"
    console = Console()
    maison_system = "Placidus"
    table = Table(title="Infos de naissance")
    table.add_column("Champ", style="cyan", no_wrap=True)
    table.add_column("Valeur", style="magenta")
    coords = get_lat_lon(ville, pays)
    if not coords:
        console.print("[red]Ville non trouvée ! Aucun thème généré.[/red]")
        return None, None
    lat, lon = coords
    table.add_row("Nom", nom)
    table.add_row("Date", date)
    table.add_row("Heure", heure)
    table.add_row("Ville", ville)
    table.add_row("Pays", pays if pays else "-")
    table.add_row("Latitude", str(lat))
    table.add_row("Longitude", str(lon))
    console.print(table)
    fuseau = get_timezone(lat, lon)
    console.print(f"Fuseau horaire détecté : {fuseau}")
    latitude = f"{int(float(lat))}:{int((float(lat)%1)*60):02d}"
    longitude = f"{int(float(lon))}:{int((float(lon)%1)*60):02d}"
    location = GeoPos(latitude, longitude)
    dt_utc = local_to_utc(date, heure, fuseau)
    date_utc = dt_utc.strftime("%Y/%m/%d")
    heure_utc = dt_utc.strftime("%H:%M")
    dt = Datetime(date_utc, heure_utc, "+00:00")
    objects = [
        const.SUN,
        const.MOON,
        const.MERCURY,
        const.VENUS,
        const.MARS,
        const.JUPITER,
        const.SATURN,
        const.URANUS,
        const.NEPTUNE,
        const.PLUTO,
        const.CHIRON,
        const.NORTH_NODE,
    ]
    chart = Chart(dt, location, IDs=objects, hsys=maison_system)
    signes = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]

    def degre_zodiaque(lon):
        signe_idx = int(lon // 30)
        degre = lon % 30
        return f"{signes[signe_idx]} {degre:.2f}°"

    for obj in objects:
        try:
            planet = chart.get(obj)
            console.print(f"{obj}: {degre_zodiaque(planet.lon)}")
        except KeyError:
            console.print(f"{obj}: not available in this flatlib version")
    asc = chart.get(const.ASC)
    mc = chart.get(const.MC)
    console.print(f"\nAscendant: {degre_zodiaque(asc.lon)}")
    console.print(f"Milieu du Ciel (MC): {degre_zodiaque(mc.lon)}")
    console.print("\nMaisons astrologiques :")
    maisons_deg_data = []
    for i in range(1, 13):
        house_const = getattr(const, f"HOUSE{i}")
        house = chart.get(house_const)
        maisons_deg_data.append(house.lon)
        console.print(f"Maison {i}: {degre_zodiaque(house.lon)}")
    aspList = [
        const.CONJUNCTION,
        const.OPPOSITION,
        const.TRINE,
        const.SQUARE,
        const.SEXTILE,
    ]
    console.print("\nAspects planétaires (orbe max 10°) :")
    aspects_data = []
    for i, obj1 in enumerate(objects):
        for obj2 in objects[i + 1 :]:
            aspect = aspects.getAspect(chart.get(obj1), chart.get(obj2), aspList)
            if aspect:
                if aspect.type == -1:
                    continue
                symboles = {0: "☌", 180: "☍", 120: "△", 90: "□", 60: "✶"}
                symbole = symboles.get(aspect.type, str(aspect.type))
                if abs(aspect.orb) <= 10:
                    console.print(f"{obj1} {symbole} {obj2} (orbe: {aspect.orb:.2f}°)")
                    aspects_data.append(
                        {
                            "planetes": f"{obj1} - {obj2}",
                            "aspect": symbole,
                            "angle": aspect.type,
                            "orb": aspect.orb,
                        }
                    )
    planetes_data = {}
    for obj in objects:
        try:
            planet = chart.get(obj)
            planetes_data[obj] = planet.lon
        except KeyError:
            pass
    planetes_maison = {}
    for obj in objects:
        planet = chart.get(obj)
        lon = planet.lon
        maison_num = None
        for i in range(12):
            debut = maisons_deg_data[i]
            fin = maisons_deg_data[(i + 1) % 12]
            if debut < fin:
                if debut <= lon < fin:
                    maison_num = i + 1
                    break
            else:
                if lon >= debut or lon < fin:
                    maison_num = i + 1
                    break
        planetes_maison[obj] = maison_num
    signes_dict = {
        "Aries": 0,
        "Taurus": 30,
        "Gemini": 60,
        "Cancer": 90,
        "Leo": 120,
        "Virgo": 150,
        "Libra": 180,
        "Scorpio": 210,
        "Sagittarius": 240,
        "Capricorn": 270,
        "Aquarius": 300,
        "Pisces": 330,
    }
    default_theme = {
        "background": "#0a1833",
        "band_color": "#23263a",
        "deco1_fill_opacity": 0.5,
        "deco2_fill_opacity": 0.2,
        "house_colors": [
            "#e6194b",
            "#3cb44b",
            "#ffe119",
            "#4363d8",
            "#f58231",
            "#911eb4",
            "#46f0f0",
            "#f032e6",
            "#bcf60c",
            "#fabebe",
            "#008080",
            "#e6beff",
        ],
        "planet_colors": {
            "Sun": "#ffcc00",
            "Moon": "#b0b0ff",
            "Mercury": "#a0a0a0",
            "Venus": "#ffb6c1",
            "Mars": "#ff6363",
            "Jupiter": "#ffd700",
            "Saturn": "#c2b280",
            "Uranus": "#7fffd4",
            "Neptune": "#6495ed",
            "Pluto": "#dda0dd",
            "Chiron": "#b8860b",
            "North Node": "#00ffcc",
        },
        "signs_glyphs_colors": {
            "Aries": "#ff0000",
            "Taurus": "#00ff00",
            "Gemini": "#00e5ee",
            "Cancer": "#ffff00",
            "Leo": "#ff00ff",
            "Virgo": "#00ffff",
            "Libra": "#ff8800",
            "Scorpio": "#00aaff",
            "Sagittarius": "#aaff00",
            "Capricorn": "#ff5500",
            "Aquarius": "#0055ff",
            "Pisces": "#00ff55",
        },
        "title_font": "DejaVu Sans, Arial",
        "title_font_size": 30,
        "title_color": "#f8b400",
        "title_opacity": 0.95,
        "signature_font": "DejaVu Sans, Arial",
        "signature_font_size": 22,
        "signature_color": "#888",
        "signature_opacity": 0.55,
        "house_num_font_size": 32,
        "house_num_color": "#f8b400",
        "house_num_font": "DejaVu Sans, Arial",
        "house_num_weight": "bold",
        "planet_deg_font_size": 22,
        "planet_deg_color": "#f8b400",
        "planet_deg_font": "DejaVu Sans, Arial",
        "planet_deg_weight": "bold",
        "deco1_color": "#393e46",
        "deco1_width": 3,
        "deco3_width": 5,
        "deco2_radius": 290,
        "deco2_color": "#00adb5",
        "deco2_width": 2,
    }
    retrogrades = []
    css_variables = ":root {\n  /* Personnalisez vos couleurs ici ! */\n  /* Exemple : pour changer la couleur du Soleil, modifiez la ligne ci-dessous */\n  --astrochart-color-sun: #ffcc00; /* Jaune doré */\n  --astrochart-color-moon: #150052;\n  --astrochart-color-mercury: #520800;\n  --astrochart-color-venus: #400052;\n  --astrochart-color-mars: #540000;\n  --astrochart-color-jupiter: #47133d;\n  --astrochart-color-saturn: #124500;\n  --astrochart-color-uranus: #6f0766;\n  --astrochart-color-neptune: #06537f;\n  --astrochart-color-pluto: #713f04;\n  --astrochart-color-mean-node: #4c1541;\n  --astrochart-color-true-node: #4c1541;\n  --astrochart-color-chiron: #666f06;\n  --astrochart-color-first-house: #ff7e00;\n  --astrochart-color-tenth-house: #ff0000;\n  --astrochart-color-seventh-house: #0000ff;\n  --astrochart-color-fourth-house: #000000;\n  --astrochart-color-mean-lilith: #000000;\n  /* Exemples pour les signes */\n  --astrochart-color-zodiac-bg-0: #ff7200;\n  --astrochart-color-zodiac-bg-1: #6b3d00;\n  --astrochart-color-zodiac-bg-2: #69acf1;\n  --astrochart-color-zodiac-bg-3: #2b4972;\n  /* ...etc pour chaque signe ... */\n  /* Exemples pour les aspects */\n  --astrochart-color-conjunction: #5757e2;\n  --astrochart-color-square: #dc0000;\n  --astrochart-color-trine: #36d100;\n  --astrochart-color-opposition: #510060;\n  /* ...etc pour chaque aspect ... */\n  /* Exemples pour les éléments */\n  --astrochart-color-air-percentage: #6f76d1;\n  --astrochart-color-earth-percentage: #6a2d04;\n  --astrochart-color-fire-percentage: #ff6600;\n  --astrochart-color-water-percentage: #630e73;\n  /* Autres exemples */\n  --astrochart-color-house-number: #f00;\n}\n\n/* Les classes SVG utilisent ces variables automatiquement ! */\n.planets-layer text { fill: var(--astrochart-color-sun); }\n/* .signs-layer text { fill: var(--astrochart-color-zodiac-icon-0); } */\n.quadrants path { opacity: 0.13; }\n.legend text { font-size: 18px; }\n"
    theme_dict = {
        "planetes": planetes_data,
        "maisons_deg": maisons_deg_data,
        "planetes_maison": planetes_maison,
        "aspects": aspects_data,
        "ascendant": asc.lon,
        "mc": mc.lon,
        "signes": signes_dict,
        "theme": default_theme,
        "retrogrades": retrogrades,
        "css_variables": css_variables,
        "titre": f"Thème de {nom} ({date} {heure} {ville})",
    }
    return theme_dict, console


def export_theme_json(theme_dict, nom, export_path=None):
    """Exporte le thème astrologique au format JSON dans le dossier utilisateur sécurisé."""
    # Dossier racine unique pour tous les utilisateurs
    base_data_dir = "/home/gaby/AstroSource/data/Utilisateurs"
    user_dir = os.path.join(base_data_dir, nom)
    os.makedirs(user_dir, exist_ok=True)
    if export_path is None:
        export_path = os.path.join(user_dir, f"theme_{nom}.json")
    else:
        if not os.path.isabs(export_path):
            export_path = os.path.join(user_dir, export_path)
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, "w", encoding="utf-8") as f:
        import json

        json.dump(theme_dict, f, ensure_ascii=False, indent=2)
    return export_path


def generate_svg(export_path, console):
    """Génère le SVG astrologique à partir du JSON exporté."""
    import importlib.util

    # Correction du chemin pour nouvelle_roue.py (toujours dans backend/ racine)
    roue_path = "/home/gaby/AstroSource/backend/nouvelle_roue.py"
    from app.services.nouvelle_roue import AstroChartSVG

    svg_export_path = os.path.splitext(export_path)[0] + ".svg"
    console.print(f"[yellow]Chemin SVG cible : {svg_export_path}[yellow]")
    svg_dir = os.path.dirname(svg_export_path) or "."
    os.makedirs(svg_dir, exist_ok=True)
    chart = AstroChartSVG(svg_export_path, export_path)
    chart.make_svg()
    console.print(f"[green]SVG généré dans {svg_export_path}[green]")
    return svg_export_path


def generate_prompt(theme_dict, nom, ville, date, heure, export_path, console):
    """Génère le prompt texte récapitulatif du thème astrologique."""
    prompt_export_path = os.path.splitext(export_path)[0] + "_prompt.txt"
    with open(prompt_export_path, "w", encoding="utf-8") as f:
        f.write(f"Thème astral de {nom} généré pour {ville} le {date} à {heure}.\n")
        f.write("Résumé des aspects principaux :\n")
        for asp in theme_dict.get("aspects", []):
            f.write(f"- {asp['planetes']} : {asp['aspect']} (orbe {asp['orb']:.2f})\n")
    console.print(f"[green]Prompt texte généré dans {prompt_export_path}[green]")
    return prompt_export_path


def generate_theme(nom, date, heure, ville, pays=None, export_path=None):
    """Pipeline complet : calcul, export JSON, SVG et prompt pour un utilisateur."""
    try:
        theme_dict, console = astro_theme_calcul(nom, date, heure, ville, pays)
        if theme_dict is None:
            return None
        export_path = export_theme_json(theme_dict, nom, export_path)
        console.print(f"\n[green]Thème exporté dans {export_path}[green]")
        try:
            with open(export_path, "r", encoding="utf-8") as f:
                contenu = f.read()
                console.print(
                    f"[cyan]Contenu JSON ({export_path}) :\n{contenu[:500]}...\n[/cyan]"
                )
        except Exception as e:
            console.print(
                f"[red]Erreur lors de la lecture du JSON avant SVG : {e}[red]"
            )
        try:
            svg_export_path = generate_svg(export_path, console)
        except Exception as svg_exc:
            console.print(f"[red]Erreur lors de la génération du SVG : {svg_exc}[red]")
        try:
            generate_prompt(theme_dict, nom, ville, date, heure, export_path, console)
        except Exception as prompt_exc:
            console.print(
                f"[red]Erreur lors de la génération du prompt : {prompt_exc}[red]"
            )
        return export_path
    except Exception as e:
        import traceback

        print(f"[red]Erreur lors du calcul ou de l'export du thème : {e}[red]")
        print(f"[red]{traceback.format_exc()}[red]")
        return None


# --- Exemple d'appel (à adapter selon votre backend) ---
# if __name__ == "__main__":
#     result = generate_theme(
#         nom="Test Pro",
#         date="01/01/1990",
#         heure="12:00",
#         ville="New York",
#         pays="USA"
#     )
#     print("Export JSON :", result)
