
import svgwrite
import json
import random

SIZE = (900, 1400)  # Hauteur augmentée
MARGIN = 40
LINE_HEIGHT = 30    # Espacement vertical raisonnable
FONT = "DejaVu Sans, Arial"

def load_theme(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def draw_background(dwg, size):
    gradient = dwg.linearGradient(start=(0, 0), end=(0, 1), id="bg_grad")
    gradient.add_stop_color(0, '#030a23')
    gradient.add_stop_color(0.5, '#0a174e')
    gradient.add_stop_color(1, '#101c3c')
    dwg.defs.add(gradient)
    dwg.add(dwg.rect(insert=(0,0), size=size, fill="url(#bg_grad)"))
    for _ in range(80):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        r = random.uniform(0.8, 2.5)
        dwg.add(dwg.circle(center=(x, y), r=r, fill='#fff', opacity=random.uniform(0.5, 1)))

planet_glyphs = {
    "Sun": "\u2609", "Moon": "\u263D", "Mercury": "\u263F", "Venus": "\u2640",
    "Mars": "\u2642", "Jupiter": "\u2643", "Saturn": "\u2644", "Uranus": "\u2645",
    "Neptune": "\u2646", "Pluto": "\u2647", "Chiron": "\u26B7", "North Node": "\u260A"
}
sign_glyphs = [
    "\u2648", "\u2649", "\u264A", "\u264B", "\u264C", "\u264D", "\u264E", "\u264F", "\u2650", "\u2651", "\u2652", "\u2653"
]
sign_names = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
planet_colors = [
    "#ff3300", "#b8860b", "#8f00ff", "#00e5ee", "#ffe066", "#ff66cc",
    "#66ff66", "#6699ff", "#ffcc66", "#cc66ff", "#66ffff", "#ff6666"
]


def format_deg_min(val):
    d = int(val)
    m = int(round((val - d) * 60))
    return f"{d:02d}°{m:02d}"

def export_report_svg(filename, theme_data):
    dwg = svgwrite.Drawing(filename, size=SIZE, profile='tiny')
    draw_background(dwg, SIZE)
    # Centralisation des définitions
    sign_ranges = [
        (0, 30),    # Aries
        (30, 60),   # Taurus
        (60, 90),   # Gemini
        (90, 120),  # Cancer
        (120, 150), # Leo
        (150, 180), # Virgo
        (180, 210), # Libra
        (210, 240), # Scorpio
        (240, 270), # Sagittarius
        (270, 300), # Capricorn
        (300, 330), # Aquarius
        (330, 360)  # Pisces
    ]
    element_ranges = {
        'Fire':   [0, 4, 8],   # Aries, Leo, Sagittarius
        'Earth':  [1, 5, 9],   # Taurus, Virgo, Capricorn
        'Air':    [2, 6, 10],  # Gemini, Libra, Aquarius
        'Water':  [3, 7, 11],  # Cancer, Scorpio, Pisces
    }
    element_fr = {'Fire': 'Feu', 'Earth': 'Terre', 'Water': 'Eau', 'Air': 'Air'}
    aspect_colors = {
        "Conjonction": "#ffcc00",
        "Opposition": "#ff3300",
        "Carré": "#ff6600",
        "Trigone": "#66ff66",
        "Sextile": "#6699ff",
        # Ajoutez d'autres aspects si besoin
    }
    y = MARGIN
    # === Header supprimé ===
    # Le titre n'est plus affiché en haut
    # === Informations générales & Éléments côte à côte ===
    # Titre Informations générales
    dwg.add(dwg.text("Informations générales", insert=(MARGIN, y), font_size=24, font_family=FONT, fill="#ffe066"))
    dwg.add(dwg.text("Éléments", insert=(MARGIN+350, y), font_size=24, font_family=FONT, fill="#ffe066"))
    y += 32
    # Extraction des infos depuis le titre
    titre = theme_data.get("titre", "")
    import re
    nom = ""
    date = "2018-10-09"
    heure = "17:30"
    lieu = "Paris"
    match = re.search(r'Thème de ([^(]+)\(([^)]+)\)', titre)
    if match:
        nom = match.group(1).strip()
        infos = match.group(2).split()
        if len(infos) >= 4:
            date = infos[0]
            heure = infos[1]
            lieu = infos[3]
    latitude = theme_data.get("latitude", "...")
    longitude = theme_data.get("longitude", "...")
    dwg.add(dwg.text(f"Prénom : {nom}", insert=(MARGIN+20, y), font_size=18, font_family=FONT, fill="#fff"))
    dwg.add(dwg.text(f"Date : {date}", insert=(MARGIN+20, y+LINE_HEIGHT), font_size=18, font_family=FONT, fill="#fff"))
    dwg.add(dwg.text(f"Heure : {heure}", insert=(MARGIN+20, y+2*LINE_HEIGHT), font_size=18, font_family=FONT, fill="#fff"))
    dwg.add(dwg.text(f"Lieu : {lieu}", insert=(MARGIN+20, y+3*LINE_HEIGHT), font_size=18, font_family=FONT, fill="#fff"))
    dwg.add(dwg.text(f"Latitude : {latitude}", insert=(MARGIN+20, y+4*LINE_HEIGHT), font_size=18, font_family=FONT, fill="#fff"))
    dwg.add(dwg.text(f"Longitude : {longitude}", insert=(MARGIN+20, y+5*LINE_HEIGHT), font_size=18, font_family=FONT, fill="#fff"))
    # Éléments à droite
    planet_positions = theme_data.get("planetes", {})
    element_planets = {'Fire': [], 'Earth': [], 'Air': [], 'Water': []}
    for name, deg in planet_positions.items():
        try:
            deg = float(deg)
        except Exception:
            continue
        sign_idx = None
        for idx, (start, end) in enumerate(sign_ranges):
            if start <= (deg % 360) < end:
                sign_idx = idx
                break
        if sign_idx is not None:
            for elem, idxs in element_ranges.items():
                if sign_idx in idxs:
                    element_planets[elem].append(name)
                    break
    y_elem = y
    for elem in ['Fire', 'Earth', 'Water', 'Air']:
        dwg.add(dwg.text(f"{element_fr[elem]} :", insert=(MARGIN+350+20, y_elem), font_size=18, font_family=FONT, fill="#ffe066"))
        x = MARGIN+350+160
        for name in element_planets[elem]:
            glyph = planet_glyphs.get(name, name[0])
            dwg.add(dwg.text(glyph, insert=(x, y_elem), font_size=22, font_family=FONT, fill="#fff"))
            x += 28
        y_elem += 28
    y += 3*LINE_HEIGHT + 10

    # === Planètes & Maisons côte à côte ===
    dwg.add(dwg.text("Planètes", insert=(MARGIN, y), font_size=28, font_family=FONT, fill="#ffe066"))
    dwg.add(dwg.text("Maisons", insert=(MARGIN+350, y), font_size=28, font_family=FONT, fill="#ffe066"))
    y += 40
    planetes = list(theme_data.get("planetes", {}).items())
    maisons_deg = theme_data.get("maisons_deg", [])
    max_len = max(len(planetes), 12)
    for i in range(max_len):
        # Planètes
        if i < len(planetes):
            name, deg = planetes[i]
            glyph = planet_glyphs.get(name, name[0])
            color = "#ff9900" if name=="Sun" else planet_colors[i % len(planet_colors)]
            deg_aff = format_deg_min(deg)
            dwg.add(dwg.text(glyph, insert=(MARGIN+20, y), font_size=24, font_family=FONT, fill=color))
            dwg.add(dwg.text(f" {name:12} : {deg_aff}", insert=(MARGIN+55, y), font_size=24, font_family=FONT, fill="#fff"))
        # Maisons
        x = MARGIN+350
        if i < len(maisons_deg):
            deg = maisons_deg[i]
            sign_idx = int((deg % 360) // 30)
            sign_name = sign_names[sign_idx]
            sign_glyph = sign_glyphs[sign_idx]
            deg_aff = format_deg_min(deg)
            dwg.add(dwg.text(sign_glyph, insert=(x, y), font_size=24, font_family=FONT, fill="#ffe066"))
            dwg.add(dwg.text(f" Maison {i+1:2} : {deg_aff} {sign_name}", insert=(x+35, y), font_size=24, font_family=FONT, fill="#fff"))
        else:
            dwg.add(dwg.text(f"Maison {i+1:2} : --", insert=(x+35, y), font_size=24, font_family=FONT, fill="#fff"))
        y += LINE_HEIGHT
    y += 20

    # === Points clés ===
    dwg.add(dwg.text("Points clés", insert=(MARGIN, y), font_size=28, font_family=FONT, fill="#ffe066"))
    y += 40
    asc = theme_data.get('ascendant', '')
    mc = theme_data.get('mc', '')
    asc_aff = format_deg_min(asc) if asc != '' else ''
    mc_aff = format_deg_min(mc) if mc != '' else ''
    asc_sign_idx = int((float(asc) % 360) // 30) if asc != '' else None
    mc_sign_idx = int((float(mc) % 360) // 30) if mc != '' else None
    asc_sign = sign_names[asc_sign_idx] if asc_sign_idx is not None else ""
    asc_glyph = sign_glyphs[asc_sign_idx] if asc_sign_idx is not None else ""
    mc_sign = sign_names[mc_sign_idx] if mc_sign_idx is not None else ""
    mc_glyph = sign_glyphs[mc_sign_idx] if mc_sign_idx is not None else ""
    dwg.add(dwg.text(f"Ascendant : {asc_aff} {asc_glyph} {asc_sign}", insert=(MARGIN+20, y), font_size=24, font_family=FONT, fill="#fff"))
    y += LINE_HEIGHT
    dwg.add(dwg.text(f"Milieu du Ciel (MC) : {mc_aff} {mc_glyph} {mc_sign}", insert=(MARGIN+20, y), font_size=24, font_family=FONT, fill="#fff"))
    y += LINE_HEIGHT + 10

    # === Aspects majeurs (cadrillage) ===
    # On descend les aspects plus bas dans la page
    y_aspect = y + 120
    dwg.add(dwg.text("Aspects majeurs", insert=(MARGIN, y_aspect), font_size=28, font_family=FONT, fill="#ffe066"))
    y_aspect += 40
    x = MARGIN + 20
    cell_w = 80
    cell_h = 60
    max_cells_per_row = (SIZE[0] - 2*MARGIN) // cell_w
    cell_count = 0
    for asp in theme_data.get("aspects", []):
        planets = asp.get("planetes", "")
        aspect = asp.get("aspect", "")
        planet_names = [p.strip() for p in planets.split("-") if p.strip()]
        # Dessin du rectangle de la case avec encadrement blanc
        dwg.add(dwg.rect(insert=(x, y_aspect), size=(cell_w-8, cell_h), fill="#101c3c", opacity=0.8, rx=10, ry=10, stroke="#fff", stroke_width=2))
        # Glyphes planétaires en haut de la case
        px = x + 10
        for pname in planet_names:
            glyph = planet_glyphs.get(pname, pname[0])
            # Couleur réelle selon la planète
            planet_list = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "North Node"]
            if pname in planet_list:
                idx_color = planet_list.index(pname)
                color = planet_colors[idx_color % len(planet_colors)]
            else:
                color = "#fff"
            dwg.add(dwg.text(glyph, insert=(px, y_aspect+22), font_size=22, font_family=FONT, fill=color))
            px += 26
        # Symbole d'aspect au centre en dessous
        aspect_color = aspect_colors.get(aspect, "#fff")
        dwg.add(dwg.text(f"{aspect}", insert=(x+cell_w//2, y_aspect+44), text_anchor="middle", font_size=24, font_family=FONT, fill=aspect_color))
        # Avancement horizontal
        x += cell_w
        cell_count += 1
        if cell_count >= max_cells_per_row:
            cell_count = 0
            x = MARGIN + 20
            y_aspect += cell_h + 10
    dwg.save()

if __name__ == "__main__":
    import sys
    # Utilisation du fichier theme_data.json fourni
    theme_path = "theme_data.json"
    svg_path = "rapport_astrologique.svg"
    print(f"Génération du rapport SVG à partir de '{theme_path}' vers '{svg_path}'...")
    theme_data = load_theme(theme_path)
    export_report_svg(svg_path, theme_data)
    print(f"SVG généré : {svg_path}")
