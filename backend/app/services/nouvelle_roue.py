planet_glyphs = {
    "Sun": "\u2609",
    "Moon": "\u263d",
    "Mercury": "\u263f",
    "Venus": "\u2640",
    "Mars": "\u2642",
    "Jupiter": "\u2643",
    "Saturn": "\u2644",
    "Uranus": "\u2645",
    "Neptune": "\u2646",
    "Pluto": "\u2647",
    "Chiron": "\u26b7",
    "North Node": "\u260a",
}
import svgwrite
from math import cos, sin, radians
import json
import sys
import os

SIZE_W = 1800
SIZE_H = 1200
# Paramètres façon Kerykeion : cercle à 600px du bord gauche, rayon 540
CENTER = 600
RAYON = 420

# Glyphes Unicode des signes du zodiaque
zodiac_glyphs = [
    "\u2648",  # Bélier
    "\u2649",  # Taureau
    "\u264a",  # Gémeaux
    "\u264b",  # Cancer
    "\u264c",  # Lion
    "\u264d",  # Vierge
    "\u264e",  # Balance
    "\u264f",  # Scorpion
    "\u2650",  # Sagittaire
    "\u2651",  # Capricorne
    "\u2652",  # Verseau
    "\u2653",  # Poissons
]


def pol2cart(center, r, angle_deg):
    angle = radians(angle_deg)
    x = center + r * cos(angle)
    y = center + r * sin(angle)
    return (x, y)


import json
import sys


class AstroChartSVG:
    # 🌟 MÉTHODES D'OPTIMISATION DES CONJONCTIONS
    def detecter_conjonctions(self, planetes, orbe=4.0):
        """Détecte les groupes de planètes en conjonction"""
        planet_names = list(planetes.keys())
        visited = set()
        groups = []

        for planet in planet_names:
            if planet in visited:
                continue

            current_group = [planet]
            visited.add(planet)

            for other_planet in planet_names:
                if other_planet in visited:
                    continue

                diff = abs(planetes[planet] - planetes[other_planet])
                if diff > 180:
                    diff = 360 - diff

                if diff <= orbe:
                    current_group.append(other_planet)
                    visited.add(other_planet)

            groups.append(current_group)

        return groups

    def calculer_ajustements_positions(self, planetes, min_separation=4.0):
        """Calcule les ajustements pour éviter les superpositions"""
        adjustments = {planet: 0.0 for planet in planetes.keys()}
        groups = self.detecter_conjonctions(planetes, orbe=min_separation)

        for group in groups:
            if len(group) <= 1:
                continue

            if len(group) == 2:
                adjustments[group[0]] = -min_separation * 0.6
                adjustments[group[1]] = +min_separation * 0.6
            elif len(group) == 3:
                adjustments[group[0]] = -min_separation * 0.9
                adjustments[group[1]] = 0.0
                adjustments[group[2]] = +min_separation * 0.9
            elif len(group) == 4:
                adjustments[group[0]] = -min_separation * 1.2
                adjustments[group[1]] = -min_separation * 0.4
                adjustments[group[2]] = +min_separation * 0.4
                adjustments[group[3]] = +min_separation * 1.2
            else:  # 5+ planètes
                total_span = (len(group) - 1) * min_separation * 0.7
                start_offset = -total_span / 2
                for i, planet in enumerate(group):
                    adjustments[planet] = start_offset + i * min_separation * 0.7

        return adjustments

    def appliquer_optimisation_planetes(self, planetes_originales):
        """Applique l'optimisation aux positions des planètes"""
        planetes_optimisees = {}
        for planet, degre in planetes_originales.items():
            planetes_optimisees[planet] = degre

        adjustments = self.calculer_ajustements_positions(planetes_originales)

        for planet_name, adjustment in adjustments.items():
            if planet_name in planetes_optimisees:
                nouvelle_position = planetes_optimisees[planet_name] + adjustment

                if nouvelle_position < 0:
                    nouvelle_position += 360
                elif nouvelle_position >= 360:
                    nouvelle_position -= 360

                planetes_optimisees[planet_name] = nouvelle_position

        return planetes_optimisees

    def draw_house_sectors(self):
        """
        Dessine les secteurs colorés des maisons autour de la roue, chaque secteur avec une couleur turquoise pâle.
        """
        t = self.theme
        # Palette turquoise pâle pour chaque maison
        house_colors = [
            "#00cfff33",
            "#00e0ff33",
            "#00bfff33",
            "#00d8ff33",
            "#00cfff33",
            "#00e0ff33",
            "#00bfff33",
            "#00d8ff33",
            "#00cfff33",
            "#00e0ff33",
            "#00bfff33",
            "#00d8ff33",
        ]

        def hex_rgba_to_rgb_opacity(hex_rgba):
            if (
                isinstance(hex_rgba, str)
                and len(hex_rgba) == 9
                and hex_rgba.startswith("#")
            ):
                rgb = hex_rgba[:7]
                alpha = int(hex_rgba[7:9], 16) / 255.0
                return rgb, alpha
            return hex_rgba, 0.18  # fallback turquoise pâle

        r_outer = RAYON
        r_inner = t.get("deco2_radius", RAYON * 0.78)
        group = self.dwg.g(id="house-sectors")
        for i in range(12):
            start_deg = self.maisons_deg[i]
            end_deg = self.maisons_deg[(i + 1) % 12]
            angle_start = (360 - start_deg + 90) % 360
            angle_end = (360 - end_deg + 90) % 360
            sweep = (angle_end - angle_start) % 360
            if sweep == 0:
                sweep = 360
            if sweep > 180:
                angle_start, angle_end = angle_end, angle_start
                sweep = (angle_end - angle_start) % 360
            large_arc = 1 if sweep > 180 else 0
            x1, y1 = pol2cart(CENTER, r_outer, angle_start)
            x2, y2 = pol2cart(CENTER, r_outer, angle_end)
            x3, y3 = pol2cart(CENTER, r_inner, angle_end)
            x4, y4 = pol2cart(CENTER, r_inner, angle_start)
            color = house_colors[i % len(house_colors)]
            rgb, alpha = hex_rgba_to_rgb_opacity(color)
            path = self.dwg.path(
                d=(
                    f"M {x1},{y1} "
                    f"A {r_outer},{r_outer} 0 {large_arc},1 {x2},{y2} "
                    f"L {x3},{y3} "
                    f"A {r_inner},{r_inner} 0 {large_arc},0 {x4},{y4} Z"
                ),
                fill=rgb,
                fill_opacity=alpha,
                stroke="none",
            )
            group.add(path)
        self.dwg.add(group)

    def draw_aspect_grid(self, x_start=1550, y_start=120, box=32):
        """
        Dessine un tableau croisé des aspects (aspect grid) façon Kerykeion à droite de la roue.
        """
        aspects = self.aspects
        planetes = list(self.planetes.keys())
        n = len(planetes)
        group = self.dwg.g(id="aspect-grid")
        # En-tête horizontal (glyphes planètes)
        planet_colors = self.theme.get("planet_colors", {})
        default_color = self.theme.get("planet_default", "#fff")
        for j, planet in enumerate(planetes):
            glyphe = planet_glyphs.get(planet, planet[0])
            color = planet_colors.get(planet, default_color)
            group.add(
                self.dwg.text(
                    glyphe,
                    insert=(x_start + (j + 1) * box + box // 2, y_start),
                    font_size=22,
                    fill=color,
                    text_anchor="middle",
                )
            )
        # En-tête vertical (glyphes planètes)
        for i, planet in enumerate(planetes):
            glyphe = planet_glyphs.get(planet, planet[0])
            color = planet_colors.get(planet, default_color)
            group.add(
                self.dwg.text(
                    glyphe,
                    insert=(x_start, y_start + (i + 1) * box + box // 2 + 6),
                    font_size=22,
                    fill=color,
                    text_anchor="middle",
                )
            )
        # Cellules d'aspects avec grille
        for i, p1 in enumerate(planetes):
            for j, p2 in enumerate(planetes):
                if i == j:
                    continue
                # Dessiner la grille (rectangle autour de chaque case)
                rect_x = x_start + (j + 1) * box
                rect_y = y_start + (i + 1) * box
                group.add(
                    self.dwg.rect(
                        insert=(rect_x, rect_y),
                        size=(box, box),
                        fill="none",
                        stroke="#bbb",
                        stroke_width=1.7,
                        opacity=0.85,
                    )
                )
                # Chercher l'aspect entre p1 et p2
                asp = next(
                    (
                        a
                        for a in aspects
                        if (a["planetes"] == f"{p1} - {p2}")
                        or (a["planetes"] == f"{p2} - {p1}")
                    ),
                    None,
                )
                if asp:
                    aspect_type = asp.get("aspect", "?")
                    color = self.theme.get("aspect_colors", {}).get(aspect_type, "#bbb")
                    group.add(
                        self.dwg.text(
                            aspect_type,
                            insert=(rect_x + box // 2, rect_y + box // 2 + 6),
                            font_size=18,
                            fill=color,
                            text_anchor="middle",
                        )
                    )
        self.dwg.add(group)

    def draw_house_numbers(self):
        """
        Affiche uniquement les numéros des maisons autour du cercle, en turquoise bien visible.
        """
        t = self.theme
        house_num_color = "#00cfff"
        house_num_font = t.get("house_num_font", "DejaVu Sans, Arial")
        house_num_weight = "bold"
        house_num_font_size = 15
        deco2_radius = t.get("deco2_radius", RAYON * 0.78)
        r_num = deco2_radius + 12
        for i, deg in enumerate(self.maisons_deg):
            angle = (360 - deg + 90) % 360
            x, y = pol2cart(CENTER, r_num, angle)
            self.dwg.add(
                self.dwg.text(
                    str(i + 1),
                    insert=(x, y + house_num_font_size / 2),
                    text_anchor="middle",
                    font_size=house_num_font_size,
                    fill=house_num_color,
                    font_family=house_num_font,
                    font_weight=house_num_weight,
                )
            )

    def draw_planets(self):
        """
        Affiche les glyphes des planètes avec la VRAIE méthode Kerykeion d'ajustement des conjonctions.
        """
        t = self.theme
        planets_group = self.dwg.g(id="planets-layer", class_="planets-layer")
        planet_colors = t.get("planet_colors", {})
        base_radius = RAYON + 60

        # --- REPRODUCTION EXACTE DE LA MÉTHODE KERYKEION ---

        # 1. Créer la liste des planètes triées par position
        planets_list = []
        for i, (planet, deg) in enumerate(self.planetes.items()):
            planets_list.append([i, deg, planet])

        # Trier par position
        planets_list.sort(key=lambda x: x[1])

        # 2. Calculer les différences avec planètes voisines (comme Kerykeion)
        planet_drange = 4.0  # Distance minimale (comme Kerykeion)
        groups = []

        planets_by_pos = []
        for i, planet_data in enumerate(planets_list):
            # Calculer diffa (différence avec planète précédente)
            if i == 0:
                diffa = (planet_data[1] - planets_list[-1][1]) % 360
                if diffa > 180:
                    diffa = 360 - diffa
            else:
                diffa = abs(planet_data[1] - planets_list[i - 1][1])
                if diffa > 180:
                    diffa = 360 - diffa

            # Calculer diffb (différence avec planète suivante)
            if i == len(planets_list) - 1:
                diffb = (planets_list[0][1] - planet_data[1]) % 360
                if diffb > 180:
                    diffb = 360 - diffb
            else:
                diffb = abs(planets_list[i + 1][1] - planet_data[1])
                if diffb > 180:
                    diffb = 360 - diffb

            planets_by_pos.append([i, diffa, diffb, planet_data[2]])

        # 3. Détecter les groupes (reproduction exacte de Kerykeion)
        group_open = False
        for i, planet_info in enumerate(planets_by_pos):
            e, diffa, diffb, planet_name = planet_info

            if (diffa < planet_drange) or (diffb < planet_drange):
                if not group_open:
                    groups.append([])
                    group_open = True
                groups[-1].append([e, diffa, diffb, planet_name])
            else:
                if group_open:
                    groups[-1].append([e, diffa, diffb, planet_name])
                group_open = False

        # 4. Calculer planets_delta (ajustements) - REPRODUCTION EXACTE
        def zero(x):
            return 0

        planets_delta = list(map(zero, range(len(planets_list))))

        for a in range(len(groups)):
            # Deux planètes groupées
            if len(groups[a]) == 2:
                next_to_a = groups[a][0][0] - 1
                if groups[a][1][0] == (len(planets_by_pos) - 1):
                    next_to_b = 0
                else:
                    next_to_b = groups[a][1][0] + 1

                min_separation = planet_drange * 1.2

                # Si les deux planètes ont de l'espace
                if (groups[a][0][1] > (2.5 * planet_drange)) and (
                    groups[a][1][2] > (2.5 * planet_drange)
                ):
                    planets_delta[groups[a][0][0]] = -min_separation / 2
                    planets_delta[groups[a][1][0]] = +min_separation / 2
                # Si planète a a de l'espace
                elif groups[a][0][1] > (2.5 * planet_drange):
                    planets_delta[groups[a][0][0]] = -min_separation
                # Si planète b a de l'espace
                elif groups[a][1][2] > (2.5 * planet_drange):
                    planets_delta[groups[a][1][0]] = +min_separation
                # Si les planètes voisines ont de l'espace
                elif (planets_by_pos[next_to_a][1] > (2.8 * planet_drange)) and (
                    planets_by_pos[next_to_b][2] > (2.8 * planet_drange)
                ):
                    planets_delta[next_to_a] = groups[a][0][1] - planet_drange * 2.2
                    planets_delta[groups[a][0][0]] = -planet_drange * 0.6
                    planets_delta[next_to_b] = -(groups[a][1][2] - planet_drange * 2.2)
                    planets_delta[groups[a][1][0]] = +planet_drange * 0.6

            # Trois planètes ou plus
            xl = len(groups[a])
            if xl >= 3:
                available = groups[a][0][1]
                for f in range(xl):
                    available += groups[a][f][2]
                need = (3.5 * planet_drange) + (1.4 * (xl - 1) * planet_drange)

                if available > need:
                    startA = (
                        groups[a][0][1] - (need * 0.5)
                        if groups[a][0][1] > (need * 0.5)
                        else 0
                    )
                    planets_delta[groups[a][0][0]] = (
                        startA - groups[a][0][1] + (1.8 * planet_drange)
                    )
                    for f in range(xl - 1):
                        planets_delta[groups[a][(f + 1)][0]] = (
                            1.4 * planet_drange
                            + planets_delta[groups[a][f][0]]
                            - groups[a][f][2]
                        )
                else:
                    # Distribution forcée
                    center_offset = -(xl - 1) * 0.7 * planet_drange / 2
                    for f in range(xl):
                        planets_delta[groups[a][f][0]] = (
                            center_offset + f * 0.7 * planet_drange
                        )

        # 5. Dessiner les planètes avec les ajustements
        for i, planet_data in enumerate(planets_list):
            planet_idx, original_deg, planet_name = planet_data

            # Position ajustée (avec planets_delta)
            adjusted_deg = original_deg + planets_delta[i]
            if adjusted_deg < 0:
                adjusted_deg += 360
            elif adjusted_deg >= 360:
                adjusted_deg -= 360

            # Angles pour le dessin
            true_angle = (360 - original_deg + 90) % 360
            adjusted_angle = (360 - adjusted_deg + 90) % 360

            # Positions
            true_x, true_y = pol2cart(CENTER, base_radius, true_angle)
            planet_x, planet_y = pol2cart(CENTER, base_radius, adjusted_angle)

            glyphe = planet_glyphs.get(planet_name, planet_name[0])
            color = planet_colors.get(planet_name, t["planet_default"])

            # Tick principal : du centre vers position vraie
            planets_group.add(
                self.dwg.line(
                    start=(CENTER, CENTER),
                    end=(true_x, true_y),
                    stroke=color,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )

            # Si ajusté, tick de connexion vers position ajustée
            if abs(planets_delta[i]) > 0.1:
                planets_group.add(
                    self.dwg.line(
                        start=(true_x, true_y),
                        end=(planet_x, planet_y),
                        stroke=color,
                        stroke_width=0.8,
                        opacity=0.9,
                    )
                )

            # Glyphe à la position ajustée (ou vraie si pas d'ajustement)
            final_x = planet_x if abs(planets_delta[i]) > 0.1 else true_x
            final_y = planet_y if abs(planets_delta[i]) > 0.1 else true_y

            planets_group.add(
                self.dwg.text(
                    glyphe,
                    insert=(final_x, final_y + 18),
                    text_anchor="middle",
                    font_size=t["planet_font_size"],
                    fill=color,
                    font_family=t["planet_font"],
                    font_weight="bold",
                )
            )

        print(
            f"PLANETS_GROUP avec {len(groups)} groupes détectés, ajustements: {[f'{p:.1f}' for p in planets_delta]}"
        )
        self.dwg.add(planets_group)

    def draw_zodiac(self):
        """
        Dessine le cercle principal et les séparations des signes du zodiaque.
        """
        t = self.theme
        zodiac_group = self.dwg.g(id="zodiac-layer", class_="zodiac-layer")
        # Cercle principal : contour bien visible, intérieur transparent ou très léger
        # Toujours utiliser CENTER pour le centre du cercle principal
        zodiac_group.add(
            self.dwg.circle(
                center=(CENTER, CENTER),
                r=RAYON,
                stroke="#fff",
                fill="none",
                stroke_width=10,
            )
        )
        # Séparations des signes (épaisseur augmentée)
        for i in range(12):
            angle_rad = radians(i * 30 + 90)
            x1 = CENTER + RAYON * cos(angle_rad)
            y1 = CENTER + RAYON * sin(angle_rad)
            x2 = CENTER + (RAYON * 0.75) * cos(angle_rad)
            y2 = CENTER + (RAYON * 0.75) * sin(angle_rad)
            zodiac_group.add(
                self.dwg.line(
                    start=(x1, y1), end=(x2, y2), stroke="#fff", stroke_width=5
                )
            )
        self.dwg.add(zodiac_group)

    def draw_aspect_table(self, group, x_start, y_start, row_height=28):
        """Dessine la liste des aspects sous le tableau des planètes, colonne de droite."""
        t = self.theme
        aspect_colors = t.get("aspect_colors", {})
        planet_glyphs = t.get("planet_glyphs", globals().get("planet_glyphs", {}))
        font = t.get("legend_font", "DejaVu Sans, Arial")
        font_size = t.get("legend_font_size", 18)
        y = y_start
        # Titre
        group.add(
            self.dwg.text(
                "Aspects :",
                insert=(x_start, y),
                font_size=font_size,
                font_family=font,
                font_weight="bold",
                fill="#fff",
            )
        )
        y += row_height
        for asp in self.aspects:
            aspect_type = asp.get("aspect", "?")
            color = aspect_colors.get(aspect_type, "#bbb")
            planets = asp.get("planetes", "")
            orb = asp.get("orb", None)
            # Format : glyphe aspect, planètes, orbe
            txt = f"{aspect_type}  {planets}"
            if orb is not None:
                txt += f"  (orb {orb:.2f})"
            group.add(
                self.dwg.text(
                    txt,
                    insert=(x_start + 10, y),
                    font_size=font_size,
                    font_family=font,
                    fill=color,
                )
            )
            y += row_height

    def draw_degree_labels(self):
        """
        Affiche la numérotation des degrés à l'extérieur de la roue, sur la couronne des ticks (façon Kerykeion),
        et ajoute un cercle fin juste au-dessus pour bien délimiter l'anneau.
        """
        t = self.theme
        labels_group = self.dwg.g(id="degree-labels")
        r_label = t.get("deco1_radius", RAYON * 0.92) + 18
        font_size = t.get("degree_label_font_size", 14)
        font_color = t.get("degree_label_color", "#bbb")
        font_family = t.get("degree_label_font", "DejaVu Sans, Arial")
        # Suppression des chiffres de la graduation : on ne dessine plus les labels
        # Ajout d'un cercle fin juste au-dessus de la numérotation pour délimiter l'anneau
        r_cercle = r_label + font_size * 0.9
        labels_group.add(
            self.dwg.circle(
                center=(CENTER, CENTER),
                r=r_cercle,
                stroke="#bbb",
                stroke_width=2,
                fill="none",
            )
        )
        self.dwg.add(labels_group)

    def draw_planet_table(self, group, x_start, y_start, row_height=40):
        """Dessine un tableau des positions planétaires à droite du cercle."""
        t = self.theme
        planet_glyphs = t.get("planet_glyphs", globals().get("planet_glyphs", {}))
        planet_colors = t.get(
            "planet_colors", t.get("planet_default", globals().get("planet_glyphs", {}))
        )
        sign_glyphs = [
            "\u2648",
            "\u2649",
            "\u264a",
            "\u264b",
            "\u264c",
            "\u264d",
            "\u264e",
            "\u264f",
            "\u2650",
            "\u2651",
            "\u2652",
            "\u2653",
        ]
        sign_names = [
            "Bélier",
            "Taureau",
            "Gémeaux",
            "Cancer",
            "Lion",
            "Vierge",
            "Balance",
            "Scorpion",
            "Sagittaire",
            "Capricorne",
            "Verseau",
            "Poissons",
        ]
        retrogrades = self.retrogrades if hasattr(self, "retrogrades") else []
        # En-têtes
        # Suppression de l’en-tête pour un affichage épuré (astrologue confirmé)
        # Lignes planètes
        # Affichage de l'AS et du MC en haut de la colonne
        y_offset = 0
        if self.ascendant is not None:
            y_as = y_start + y_offset * row_height
            deg_as = self.ascendant % 30
            sign_index_as = int(self.ascendant // 30) % 12
            sign_glyph_as = sign_glyphs[sign_index_as]
            signs_glyphs_colors = t.get("signs_glyphs_colors", {})
            glyph_color_as = signs_glyphs_colors.get(
                self.signs[sign_index_as], t.get("sign_glyph_color", "#fff")
            )
            deg_txt_as = f"{int(deg_as):02d}°{int((deg_as%1)*60):02d}'"
            group.add(
                self.dwg.text(
                    "AS",
                    insert=(x_start, y_as),
                    font_size=26,
                    fill="#00cfff",
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            group.add(
                self.dwg.text(
                    deg_txt_as,
                    insert=(x_start + 70, y_as),
                    font_size=20,
                    fill="#fff",
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            group.add(
                self.dwg.text(
                    sign_glyph_as,
                    insert=(x_start + 140, y_as),
                    font_size=26,
                    fill=glyph_color_as,
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            y_offset += 1
        if self.mc is not None:
            y_mc = y_start + y_offset * row_height
            deg_mc = self.mc % 30
            sign_index_mc = int(self.mc // 30) % 12
            sign_glyph_mc = sign_glyphs[sign_index_mc]
            signs_glyphs_colors = t.get("signs_glyphs_colors", {})
            glyph_color_mc = signs_glyphs_colors.get(
                self.signs[sign_index_mc], t.get("sign_glyph_color", "#fff")
            )
            deg_txt_mc = f"{int(deg_mc):02d}°{int((deg_mc%1)*60):02d}'"
            group.add(
                self.dwg.text(
                    "MC",
                    insert=(x_start, y_mc),
                    font_size=26,
                    fill="#ffe066",
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            group.add(
                self.dwg.text(
                    deg_txt_mc,
                    insert=(x_start + 70, y_mc),
                    font_size=20,
                    fill="#fff",
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            group.add(
                self.dwg.text(
                    sign_glyph_mc,
                    insert=(x_start + 140, y_mc),
                    font_size=26,
                    fill=glyph_color_mc,
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            y_offset += 1

        # Affichage des planètes
        for idx, (planet, deg) in enumerate(self.planetes.items()):
            y = y_start + (idx + y_offset) * row_height
            glyphe = planet_glyphs.get(planet, planet[0])
            color = planet_colors.get(planet, t["planet_default"])
            sign_index = int(deg // 30) % 12
            deg_in_sign = deg % 30
            sign_glyph = sign_glyphs[sign_index]
            signs_glyphs_colors = t.get("signs_glyphs_colors", {})
            glyph_color = signs_glyphs_colors.get(
                self.signs[sign_index], t.get("sign_glyph_color", "#fff")
            )
            deg_txt = f"{int(deg_in_sign):02d}°{int((deg_in_sign%1)*60):02d}'"
            retro = "R" if planet in retrogrades else ""
            # Planète
            group.add(
                self.dwg.text(
                    glyphe,
                    insert=(x_start, y),
                    font_size=26,
                    fill=color,
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            # Position (degré)
            group.add(
                self.dwg.text(
                    deg_txt,
                    insert=(x_start + 70, y),
                    font_size=20,
                    fill="#fff",
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            # Signe (glyphe seul, colorisé)
            group.add(
                self.dwg.text(
                    sign_glyph,
                    insert=(x_start + 140, y),
                    font_size=26,
                    fill=glyph_color,
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )
            # Rétro (R rapproché du glyphe du signe)
            group.add(
                self.dwg.text(
                    retro,
                    insert=(x_start + 175, y),
                    font_size=20,
                    fill="#fff",
                    font_family="DejaVu Sans",
                    text_anchor="start",
                )
            )

    def draw_degree_ticks(self):
        """
        Ajoute la graduation zodiacale (ticks de degré) façon Kerykeion.
        """
        t = self.theme
        ticks_group = self.dwg.g(id="degree-ticks")
        # Rayon extérieur et intérieur des ticks (entre deco1 et deco2)
        r_outer = RAYON  # Place la graduation sur le cercle extérieur principal
        tick_color = t.get("tick_color", "#bbb")
        for deg in range(360):
            angle = (360 - deg + 90) % 360
            # Ticks sur une couronne fine
            if deg % 10 == 0:
                r_inner = r_outer - 22
                width = 3.5
                opacity = 1.0
            elif deg % 5 == 0:
                r_inner = r_outer - 16
                width = 2.2
                opacity = 0.85
            else:
                r_inner = r_outer - 10
                width = 1.2
                opacity = 0.6
            x1, y1 = pol2cart(CENTER, r_outer, angle)
            x2, y2 = pol2cart(CENTER, r_inner, angle)
            ticks_group.add(
                self.dwg.line(
                    start=(x1, y1),
                    end=(x2, y2),
                    stroke=tick_color,
                    stroke_width=width,
                    opacity=opacity,
                )
            )
        self.dwg.add(ticks_group)

    def draw_angles(self):
        """
        Dessine les ticks et labels pour l'AS et le MC dans un groupe dédié, façon Kerykeion.
        """
        t = self.theme
        angles_group = self.dwg.g(id="angles-layer")
        # Rayon et angle pour AS/MC identiques à ceux utilisés pour les glyphes planétaires
        base_radius = RAYON + 60
        r_c3 = RAYON - 120  # Cercle intérieur (c3)
        r_inter = base_radius - 30  # Cercle intermédiaire
        r_glyphe = base_radius  # Position du glyphe AS/MC (même que planète)
        # AS
        if self.ascendant is not None:
            angle_as = (360 - self.ascendant + 90) % 360
            x1, y1 = pol2cart(CENTER, r_c3, angle_as)
            x2, y2 = pol2cart(CENTER, r_inter, angle_as)
            x3, y3 = pol2cart(CENTER, r_glyphe, angle_as)
            color_as = t.get("angle_as", "#00cfff")
            # Tick principal fin façon planète
            angles_group.add(
                self.dwg.line(
                    start=(CENTER, CENTER),
                    end=(x3, y3),
                    stroke=color_as,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )
            # Optionnel : petit tick intermédiaire (du cercle intérieur au cercle intermédiaire)
            angles_group.add(
                self.dwg.line(
                    start=(x1, y1),
                    end=(x2, y2),
                    stroke=color_as,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )
            # Glyphe AS
            angles_group.add(
                self.dwg.text(
                    "AS",
                    insert=(x3, y3 + 18),
                    text_anchor="middle",
                    font_size=t["angle_font_size"],
                    fill=color_as,
                    font_weight=t["angle_font_weight"],
                )
            )
        # MC
        if self.mc is not None:
            angle_mc = (360 - self.mc + 90) % 360
            x1, y1 = pol2cart(CENTER, r_c3, angle_mc)
            x2, y2 = pol2cart(CENTER, r_inter, angle_mc)
            x3, y3 = pol2cart(CENTER, r_glyphe, angle_mc)
            color_mc = t.get("angle_mc", "#ffe066")
            angles_group.add(
                self.dwg.line(
                    start=(CENTER, CENTER),
                    end=(x3, y3),
                    stroke=color_mc,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )
            angles_group.add(
                self.dwg.line(
                    start=(x1, y1),
                    end=(x2, y2),
                    stroke=color_mc,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )
            angles_group.add(
                self.dwg.text(
                    "MC",
                    insert=(x3, y3 + 18),
                    text_anchor="middle",
                    font_size=t["angle_font_size"],
                    fill=color_mc,
                    font_weight=t["angle_font_weight"],
                )
            )
        self.dwg.add(angles_group)

    def draw_house_list(self, group, x_start=80, y_start=120, row_height=40):
        """
        Affiche la liste des maisons à gauche : numéro bleu turquoise, glyphe du signe colorisé, degré en blanc.
        """
        t = self.theme
        signs_glyphs = t.get("signs_glyphs", {})
        signs_glyphs_colors = t.get("signs_glyphs_colors", {})
        house_num_color = "#00cfff"
        deg_color = "#fff"
        font = "DejaVu Sans"
        font_size = 22
        for i, maison in enumerate(self.maisons_deg):
            y = y_start + i * row_height
            sign_index = int(maison // 30) % 12
            sign = self.signs[sign_index]
            sign_glyph = signs_glyphs.get(sign, "?")
            glyph_color = signs_glyphs_colors.get(
                sign, t.get("sign_glyph_color", "#fff")
            )
            deg = maison % 30
            deg_txt = f"{int(deg):02d}°{int((deg%1)*60):02d}'"
            # Numéro de maison
            group.add(
                self.dwg.text(
                    str(i + 1),
                    insert=(x_start, y),
                    font_size=font_size,
                    fill=house_num_color,
                    font_family=font,
                    font_weight="bold",
                    text_anchor="end",
                )
            )
            # Glyphe du signe
            group.add(
                self.dwg.text(
                    sign_glyph,
                    insert=(x_start + 15, y),
                    font_size=26,
                    fill=glyph_color,
                    font_family=font,
                    text_anchor="start",
                )
            )
            # Degré
            group.add(
                self.dwg.text(
                    deg_txt,
                    insert=(x_start + 55, y),
                    font_size=20,
                    fill=deg_color,
                    font_family=font,
                    text_anchor="start",
                )
            )

    def create_signs_defs(self):
        """
        Crée les définitions des glyphes des signes avec leurs couleurs dans <defs> comme Kerykeion.
        """
        t = self.theme
        signs_glyphs_colors = t.get("signs_glyphs_colors", {})

        # Créer un groupe defs pour les signes colorés
        defs = self.dwg.defs

        for sign in self.signs:
            sign_glyph = self.theme["signs_glyphs"][sign]
            glyph_color = signs_glyphs_colors.get(sign, t["sign_glyph_color"])

            # Créer un élément text avec la couleur définie
            sign_def = self.dwg.text(
                sign_glyph,
                insert=(0, 0),
                text_anchor="middle",
                font_size=t["sign_glyph_font_size"],
                fill=glyph_color,
                font_family=t["sign_glyph_font"],
                font_weight="bold",
                id=f"sign_{sign.lower()}",
            )
            defs.add(sign_def)

    def draw_signs(self):
        """
        Affiche les glyphes des signes du zodiaque autour du cercle avec leurs couleurs directement.
        """
        t = self.theme
        signs_group = self.dwg.g(id="signs-layer", class_="signs-layer")
        signs_glyphs_colors = t.get("signs_glyphs_colors", {})

        print(
            f"[DEBUG draw_signs] Drawing {len(self.signs)} signs avec couleurs directes"
        )

        for i, sign in enumerate(self.signs):
            angle = (360 - (i * 30 + 15) + 90) % 360
            r_glyphe = RAYON * 0.87
            x, y = pol2cart(CENTER, r_glyphe, angle)

            # Obtenir le glyphe et la couleur du signe
            sign_glyph = self.theme["signs_glyphs"][sign]
            glyph_color = signs_glyphs_colors.get(sign, t["sign_glyph_color"])

            print(
                f"[DEBUG draw_signs] Sign {i}: {sign} = {sign_glyph} couleur {glyph_color} at ({x:.1f}, {y:.1f})"
            )

            # Dessiner directement le glyphe avec sa couleur (pas de <use>)
            signs_group.add(
                self.dwg.text(
                    sign_glyph,
                    insert=(x, y + 28),
                    text_anchor="middle",
                    font_size=t["sign_glyph_font_size"],
                    fill=glyph_color,
                    font_family=t["sign_glyph_font"],
                    font_weight="bold",
                )
            )

        self.dwg.add(signs_group)
        print(
            f"[DEBUG draw_signs] Ajouté signs_group avec {len(self.signs)} signes colorés directement"
        )

    def draw_quadrants(self):
        """
        Dessine 4 arcs/quadrants colorés et semi-transparents pour visualiser les axes et secteurs.
        """
        t = self.theme
        # Couleurs par défaut ou personnalisables
        quad_colors = t.get(
            "quadrant_colors", ["#00adb5", "#f8b400", "#ff6363", "#393e46"]
        )
        quad_opacity = t.get("quadrant_opacity", 0.13)
        r1 = RAYON * 0.75
        r2 = RAYON
        quad_group = self.dwg.g(id="quadrants", class_="quadrants")
        for i in range(4):
            start_angle = i * 90
            end_angle = start_angle + 90
            # Points sur le cercle extérieur
            x1, y1 = pol2cart(CENTER, r2, (360 - start_angle + 90) % 360)
            x2, y2 = pol2cart(CENTER, r2, (360 - end_angle + 90) % 360)
            # Points sur le cercle intérieur
            x3, y3 = pol2cart(CENTER, r1, (360 - end_angle + 90) % 360)
            x4, y4 = pol2cart(CENTER, r1, (360 - start_angle + 90) % 360)
            path = self.dwg.path(
                d=f"M {x1},{y1} A {r2},{r2} 0 0,1 {x2},{y2} L {x3},{y3} A {r1},{r1} 0 0,0 {x4},{y4} Z",
                fill=quad_colors[i % len(quad_colors)],
                fill_opacity=quad_opacity,
                stroke="none",
            )
            quad_group.add(path)
        self.dwg.add(quad_group)

    def draw_legend(self, position="bottom"):
        """
        Dessine une légende expliquant les couleurs des aspects, les glyphes planétaires et zodiacaux.
        :param position: "bottom" (par défaut) ou "right"
        """
        t = self.theme
        legend_group = self.dwg.g(id="legend", class_="legend")
        # Positionnement
        if position == "bottom":
            x0, y0 = 60, SIZE_H - 160
        else:
            x0, y0 = SIZE_W - 320, 60
        y = y0
        line_h = 34
        font = t.get("legend_font", "DejaVu Sans, Arial")
        font_size = t.get("legend_font_size", 22)
        # Aspects
        legend_group.add(
            self.dwg.text(
                "Aspects :",
                insert=(x0, y),
                font_size=font_size,
                font_family=font,
                font_weight="bold",
                fill="#333",
            )
        )
        y += line_h
        for asp, color in t["aspect_colors"].items():
            asp_name = {
                "☌": "Conjonction",
                "△": "Trigone",
                "□": "Carré",
                "☍": "Opposition",
                "✶": "Sextile",
            }.get(asp, asp)
            legend_group.add(
                self.dwg.text(
                    f"{asp}  {asp_name}",
                    insert=(x0 + 10, y),
                    font_size=font_size,
                    font_family=font,
                    fill=color,
                )
            )
            y += line_h
        y += 10
        # Planètes
        legend_group.add(
            self.dwg.text(
                "Planètes :",
                insert=(x0, y),
                font_size=font_size,
                font_family=font,
                font_weight="bold",
                fill="#333",
            )
        )
        y += line_h
        for planet, glyphe in planet_glyphs.items():
            legend_group.add(
                self.dwg.text(
                    f"{glyphe}  {planet}",
                    insert=(x0 + 10, y),
                    font_size=font_size,
                    font_family=font,
                    fill=t["planet_default"],
                )
            )
            y += line_h
        y += 10
        # Signes
        legend_group.add(
            self.dwg.text(
                "Signes :",
                insert=(x0, y),
                font_size=font_size,
                font_family=font,
                font_weight="bold",
                fill="#333",
            )
        )
        y += line_h
        sign_names = [
            "Bélier",
            "Taureau",
            "Gémeaux",
            "Cancer",
            "Lion",
            "Vierge",
            "Balance",
            "Scorpion",
            "Sagittaire",
            "Capricorne",
            "Verseau",
            "Poissons",
        ]
        for i, glyphe in enumerate(zodiac_glyphs):
            legend_group.add(
                self.dwg.text(
                    f"{glyphe}  {sign_names[i]}",
                    insert=(x0 + 10, y),
                    font_size=font_size,
                    font_family=font,
                    fill=t["sign_glyph_color"],
                )
            )
            y += line_h
        self.dwg.add(legend_group)

    def draw_decorative_circles(self):
        """
        Ajoute des cercles décoratifs intermédiaires (entièrement personnalisables via le thème).
        """
        t = self.theme
        deco1_radius = t.get("deco1_radius", RAYON)
        deco1_color = t.get("deco1_color", "#bbb")
        deco1_width = t.get("deco1_width", 2)
        deco2_radius = t.get("deco2_radius", RAYON * 0.78)
        deco2_color = t.get("deco2_color", "#bbb")
        deco2_width = t.get("deco2_width", 2)
        deco3_radius = t.get("deco3_radius", RAYON * 0.75)
        deco3_color = t.get("deco3_color", "#bbb")
        deco3_width = t.get("deco3_width", 2)
        deco_group = self.dwg.g(id="decorative-circles")
        # Tous les cercles décoratifs sont centrés sur (CENTER, CENTER)
        deco_group.add(
            self.dwg.circle(
                center=(CENTER, CENTER),
                r=deco1_radius,
                stroke=deco1_color,
                stroke_width=deco1_width,
                fill="#23263a",
                fill_opacity=0.5,
            )
        )
        deco_group.add(
            self.dwg.circle(
                center=(CENTER, CENTER),
                r=deco2_radius,
                stroke=deco2_color,
                stroke_width=deco2_width,
                fill="#23263a",
                fill_opacity=0.2,
            )
        )
        deco_group.add(
            self.dwg.circle(
                center=(CENTER, CENTER),
                r=deco3_radius,
                stroke=deco3_color,
                stroke_width=deco3_width,
                fill="none",
            )
        )
        self.dwg.add(deco_group)

    def inject_css_variables(self):
        """
        Injecte les variables CSS Kerykeion et des classes dans le SVG pour personnalisation avancée.
        """
        # ... CSS déplacé dans le JSON, voir clé 'css_variables' ...

        # ...
        # ... CSS déplacé dans le JSON, voir clé 'css_variables' ...
        # ...
        # ...
        house_num_color = t.get("house_num_color", "#f8b400")
        house_num_font = t.get("house_num_font", "DejaVu Sans, Arial")
        house_num_weight = t.get("house_num_weight", "bold")
        r_num = RAYON * 0.68
        for i, deg in enumerate(self.maisons_deg):
            angle = (360 - deg + 90) % 360
            x, y = pol2cart(CENTER, r_num, angle)
            self.dwg.add(
                self.dwg.text(
                    str(i + 1),
                    insert=(x, y + house_num_font_size / 2),
                    text_anchor="middle",
                    font_size=house_num_font_size,
                    fill=house_num_color,
                    font_family=house_num_font,
                    font_weight=house_num_weight,
                )
            )

    def __init__(self, filename, theme_path="/home/gaby/AstroSource/theme_data.json"):
        # ATTENTION : l'ordre des arguments doit toujours être (svg_path, json_path)
        # Exemple d'appel correct : AstroChartSVG("chemin/vers/mon_theme.svg", "chemin/vers/mon_theme.json")
        # Si l'ordre est inversé, une erreur de parsing JSON se produira !
        """
        Initialise le générateur de roue astrologique SVG.
        :param filename: Nom du fichier SVG de sortie
        :param theme_path: Chemin du fichier JSON contenant les données et le thème
        """
        import os

        self.filename = filename
        svg_dir = os.path.dirname(filename) or "."
        os.makedirs(svg_dir, exist_ok=True)
        self.dwg = svgwrite.Drawing(filename, size=(SIZE_W, SIZE_H), profile="full")
        # Thème par défaut
        default_theme = {
            "background": "#fff",
            "circle_stroke": "#222",
            "circle_stroke_width": 3,
            "sign_line": "#888",
            "sign_line_width": 2,
            "house_line": "#00cfff",
            "house_line_width": 2,
            "house_line_opacity": 0.7,
            "planet_sun": "#ff9900",
            "planet_default": "#222",
            "planet_font": "DejaVu Sans, Arial Unicode MS, Segoe UI, Arial",
            "planet_font_size": 48,
            "aspect_colors": {
                "☌": "#888",
                "△": "#3399ff",
                "□": "#ff2222",
                "☍": "#ff2222",
                "✶": "#00e5ee",
            },
            "aspect_line_width": 2,
            "aspect_opacity": 0.7,
            "angle_as": "#00cfff",
            "angle_mc": "#ffe066",
            "angle_font_size": 36,
            "angle_font_weight": "bold",
            "sign_glyph_font": "DejaVu Sans, Arial Unicode MS, Segoe UI, Arial",
            "sign_glyph_font_size": 72,
            "sign_glyph_color": "#222",
            "title_font": "DejaVu Sans, Arial",
            "title_font_size": 28,
            "title_color": "#888",
            "title_opacity": 0.85,
            "signature_font": "DejaVu Sans, Arial",
            "signature_font_size": 22,
            "signature_color": "#888",
            "signature_opacity": 0.55,
        }
        # Affichage du chemin et du contenu du JSON avant lecture
        print(f"[AstroChartSVG] Lecture du JSON : {theme_path}")
        try:
            with open(theme_path, encoding="utf-8") as f:
                contenu = f.read()
                print(f"[AstroChartSVG] Contenu JSON (début) : {contenu[:500]}...\n")
            # Recharger le fichier pour le parsing JSON
            with open(theme_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[AstroChartSVG] Erreur lors de la lecture ou du parsing JSON : {e}")
            raise
        # Charger le thème depuis le JSON si présent
        self.theme = default_theme.copy()
        if "theme" in data and isinstance(data["theme"], dict):
            self.theme.update(data["theme"])

        # IMPORTANT: Charger signs_glyphs_colors depuis le thème dans le JSON
        if "theme" in data and "signs_glyphs_colors" in data["theme"]:
            self.theme["signs_glyphs_colors"] = data["theme"]["signs_glyphs_colors"]
            print(
                f"[AstroChartSVG] Couleurs des signes chargées depuis theme: {data['theme']['signs_glyphs_colors']}"
            )
        elif "signs_glyphs_colors" in data:
            self.theme["signs_glyphs_colors"] = data["signs_glyphs_colors"]
            print(
                f"[AstroChartSVG] Couleurs des signes chargées depuis racine: {data['signs_glyphs_colors']}"
            )
        else:
            print(
                f"[AstroChartSVG] ATTENTION: Aucune couleur de signes trouvée dans le JSON"
            )
        # Ajout d'un fond sombre (dark) APRÈS self.theme
        fond_color = self.theme.get(
            "background", "#181824"
        )  # Couleur par défaut sombre
        self.dwg.add(
            self.dwg.rect(insert=(0, 0), size=(SIZE_W, SIZE_H), fill=fond_color)
        )
        # Stockage des données principales
        self.planetes = data.get("planetes", {})
        # 🌟 ACTIVATION DE L'OPTIMISATION DES CONJONCTIONS
        self.planetes = self.appliquer_optimisation_planetes(self.planetes)

        self.maisons_deg = data.get("maisons_deg", [])
        self.aspects = data.get("aspects", [])
        self.ascendant = data.get("ascendant")
        self.mc = data.get("mc")
        self.titre = data.get("titre", "Thème astrologique")
        self.retrogrades = data.get("retrogrades", [])
        # Initialiser la liste des signes (ordre zodiacal)
        self.signs = data.get(
            "signs",
            [
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
            ],
        )
        # Initialiser les glyphes des signes si absents du thème
        default_signs_glyphs = {
            "Aries": "\u2648",
            "Taurus": "\u2649",
            "Gemini": "\u264a",
            "Cancer": "\u264b",
            "Leo": "\u264c",
            "Virgo": "\u264d",
            "Libra": "\u264e",
            "Scorpio": "\u264f",
            "Sagittarius": "\u2650",
            "Capricorn": "\u2651",
            "Aquarius": "\u2652",
            "Pisces": "\u2653",
        }
        if "signs_glyphs" not in self.theme:
            self.theme["signs_glyphs"] = default_signs_glyphs

    def inject_css_variables(self):
        """
        Injecte les variables CSS personnalisées depuis le JSON de thème (clé 'css_variables').
        """
        css = self.theme.get("css_variables", None)
        if css:
            self.dwg.defs.add(self.dwg.style(css))

    def draw_houses(self):
        """
        Dessine les lignes fines des maisons astrologiques (séparateurs).
        """
        t = self.theme
        houses_group = self.dwg.g(id="houses-layer")
        for deg in self.maisons_deg:
            angle = (360 - deg + 90) % 360
            x1, y1 = pol2cart(CENTER, RAYON * 0.75, angle)
            x2, y2 = pol2cart(CENTER, RAYON, angle)
            houses_group.add(
                self.dwg.line(
                    start=(x1, y1),
                    end=(x2, y2),
                    stroke=t["house_line"],
                    stroke_width=t["house_line_width"],
                    opacity=t["house_line_opacity"],
                )
            )
        self.dwg.add(houses_group)

    def draw_planets(self):
        """
        Affiche les glyphes des planètes, leur degré et le symbole rétrograde si besoin.
        """
        t = self.theme
        planets_group = self.dwg.g(id="planets-layer", class_="planets-layer")
        deg_font_size = t.get("planet_deg_font_size", 22)
        deg_color = t.get("planet_deg_color", "#f8b400")
        deg_font = t.get("planet_deg_font", "DejaVu Sans, Arial")
        deg_weight = t.get("planet_deg_weight", "bold")
        retrogrades = self.retrogrades
        planet_colors = t.get("planet_colors", {})
        sign_names = [
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
        sign_glyphs = [
            "\u2648",
            "\u2649",
            "\u264a",
            "\u264b",
            "\u264c",
            "\u264d",
            "\u264e",
            "\u264f",
            "\u2650",
            "\u2651",
            "\u2652",
            "\u2653",
        ]
        # --- Gestion du chevauchement façon Kerykeion ---
        # On trie les planètes par angle croissant
        planet_angles = []
        for planet, deg in self.planetes.items():
            angle = (360 - deg + 90) % 360
            planet_angles.append((angle, planet, deg))
        planet_angles.sort()
        # On applique un décalage radial si deux planètes sont trop proches
        min_angle_diff = 18  # seuil en degrés pour décaler
        base_radius = RAYON + 60
        radius_step = 22  # écart radial entre planètes superposées
        prev_angle = None
        prev_radius = base_radius
        for idx, (angle, planet, deg) in enumerate(planet_angles):
            # Si trop proche de la précédente, on décale
            if prev_angle is not None and abs(angle - prev_angle) < min_angle_diff:
                r_planete = prev_radius + radius_step
            else:
                r_planete = base_radius
            # Position normale (cercle principal)
            x0, y0 = pol2cart(CENTER, base_radius, angle)
            # Position décalée (si besoin)
            x, y = pol2cart(CENTER, r_planete, angle)
            glyphe = planet_glyphs.get(planet, planet[0])
            color = planet_colors.get(planet, t["planet_default"])
            # Tick de base : du centre au cercle principal (toujours)
            planets_group.add(
                self.dwg.line(
                    start=(CENTER, CENTER),
                    end=(x0, y0),
                    stroke=color,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )
            # Si la planète est décalée, ajouter un tick du cercle principal à la position décalée
            if r_planete > base_radius:
                planets_group.add(
                    self.dwg.line(
                        start=(x0, y0),
                        end=(x, y + 18),
                        stroke=color,
                        stroke_width=0.7,
                        opacity=0.7,
                    )
                )
            planets_group.add(
                self.dwg.text(
                    glyphe,
                    insert=(x, y + 18),
                    text_anchor="middle",
                    font_size=t["planet_font_size"],
                    fill=color,
                    font_family=t["planet_font"],
                    font_weight="bold",
                )
            )
            prev_angle = angle
            prev_radius = r_planete
        self.dwg.add(planets_group)

    def draw_aspects(self):
        """
        Dessine les aspects entre planètes avec styles avancés (pointillés, épaisseurs variables) et ajoute les ticks façon Kerykeion.
        """
        t = self.theme
        aspects_group = self.dwg.g(id="aspects-layer")
        couleur_aspects = t["aspect_colors"]
        # Seuls les carrés (□) sont en pointillé, sans flou. Les autres aspects sont en trait plein.
        aspect_styles = t.get(
            "aspect_styles",
            {
                "☌": {"width": 4, "dasharray": None},
                "△": {"width": 3, "dasharray": None},
                "✶": {"width": 3, "dasharray": None},
                "□": {"width": 3, "dasharray": "6,6"},
                "☍": {"width": 3, "dasharray": None},
            },
        )
        planet_colors = t.get("planet_colors", {})
        deco2_radius = t.get("deco2_radius", RAYON * 0.78)
        for asp in self.aspects:
            p1, p2 = asp["planetes"].split(" - ")
            deg1 = self.planetes.get(p1)
            deg2 = self.planetes.get(p2)
            if deg1 is None or deg2 is None:
                continue
            # Calcul des angles pour chaque planète
            angle1 = (360 - deg1 + 90) % 360
            angle2 = (360 - deg2 + 90) % 360
            # Les aspects s'arrêtent au premier cercle décoratif intérieur
            r_aspect = deco2_radius
            x1, y1 = pol2cart(CENTER, r_aspect, angle1)
            x2, y2 = pol2cart(CENTER, r_aspect, angle2)
            aspect_type = asp["aspect"]
            couleur = couleur_aspects.get(aspect_type, "#aaa")
            style = aspect_styles.get(
                aspect_type, {"width": t["aspect_line_width"], "dasharray": None}
            )
            line_args = dict(
                start=(x1, y1),
                end=(x2, y2),
                stroke=couleur,
                stroke_width=style["width"],
                opacity=t["aspect_opacity"],
            )
            if style["dasharray"]:
                line_args["stroke_dasharray"] = style["dasharray"]
            # Seuls les conjonctions (☌) ont un effet glow, pas les oppositions ni les carrés ni les sextiles
            if aspect_type == "☌":
                aspects_group.add(self.dwg.line(**line_args, filter="url(#glow)"))
            else:
                aspects_group.add(self.dwg.line(**line_args))
            # --- Ajout des ticks façon Kerykeion ---
            tick_r = RAYON + 30  # Rayon de départ du tick (extérieur)
            # Tick pour planète 1
            tick_color1 = planet_colors.get(p1, couleur)
            tx1, ty1 = pol2cart(CENTER, tick_r, angle1)
            aspects_group.add(
                self.dwg.line(
                    start=(tx1, ty1),
                    end=(x1, y1),
                    stroke=tick_color1,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )
            # Tick pour planète 2
            tick_color2 = planet_colors.get(p2, couleur)
            tx2, ty2 = pol2cart(CENTER, tick_r, angle2)
            aspects_group.add(
                self.dwg.line(
                    start=(tx2, ty2),
                    end=(x2, y2),
                    stroke=tick_color2,
                    stroke_width=0.5,
                    opacity=0.7,
                )
            )

        self.dwg.add(aspects_group)

    def draw_title(self):
        """
        Affiche le titre du thème astrologique si présent.
        """
        t = self.theme
        if self.titre and str(self.titre).strip():
            self.dwg.add(
                self.dwg.text(
                    self.titre,
                    insert=(SIZE_W // 2, 60),
                    text_anchor="middle",
                    font_size=t["title_font_size"],
                    fill=t["title_color"],
                    font_family=t["title_font"],
                    opacity=t["title_opacity"],
                    font_weight="bold",
                )
            )

    def draw_signature(self):
        """
        Affiche la signature en bas de page.
        """
        t = self.theme
        signature = "AstroSource - Générateur de thèmes astraux"
        self.dwg.add(
            self.dwg.text(
                signature,
                insert=(SIZE_W - 20, SIZE_H - 20),
                text_anchor="end",
                font_size=t["signature_font_size"],
                fill=t["signature_color"],
                font_family=t["signature_font"],
                opacity=t["signature_opacity"],
            )
        )

    def draw_title(self):
        """
        Affiche le titre du thème astrologique si présent.
        """
        t = self.theme
        if self.titre and str(self.titre).strip():
            self.dwg.add(
                self.dwg.text(
                    self.titre,
                    insert=(CENTER, SIZE_H - 40),
                    text_anchor="middle",
                    font_size=t["title_font_size"],
                    fill=t["title_color"],
                    font_family=t["title_font"],
                    opacity=t["title_opacity"],
                )
            )

    def draw_signature(self):
        """
        Ajoute la signature de l’auteur en bas à droite du SVG.
        """
        pass

    def save(self):
        """
        Sauvegarde le dessin SVG sur disque, en créant le dossier parent si besoin.
        """
        import os

        svg_dir = os.path.dirname(self.filename) or "."
        os.makedirs(svg_dir, exist_ok=True)
        print(f"[AstroChartSVG.save] Sauvegarde du SVG dans : {self.filename}")
        self.dwg.save()

    # Définir correctement make_svg comme méthode de la classe
    def make_svg(self):
        """
        Génère l’ensemble du thème astrologique SVG en appelant toutes les couches, puis la légende.
        """
        self.inject_css_variables()
        # Ajout d'un filtre glow SVG pour les aspects majeurs
        glow = self.dwg.defs.add(self.dwg.filter(id="glow"))
        glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=3)
        # DESSINER TOUTES LES COUCHES
        print("[DEBUG make_svg] Début de la génération SVG")
        self.inject_css_variables()
        self.draw_decorative_circles()
        self.draw_house_sectors()
        self.draw_degree_ticks()
        self.draw_zodiac()
        self.draw_houses()
        self.draw_house_numbers()
        self.draw_angles()
        self.draw_planets()

        # Créer les définitions des signes AVANT de les dessiner
        print("[DEBUG make_svg] Création des définitions des signes")
        self.create_signs_defs()
        print("[DEBUG make_svg] Dessin des signes avec <use>")
        self.draw_signs()

        # Affichage épuré des maisons à gauche
        group_maisons = self.dwg.g(id="house-list")
        self.draw_house_list(group_maisons, x_start=1500, y_start=160, row_height=40)
        self.dwg.add(group_maisons)
        self.draw_aspects()

        # Affichage du tableau des planètes et aspects à droite de la roue
        group = self.dwg.g(id="right-table")
        # Décalage plus à droite (x_start augmenté)
        self.draw_planet_table(group, x_start=1260, y_start=120)
        # Tableau croisé des aspects juste en dessous
        self.draw_aspect_grid(x_start=1300, y_start=700, box=32)
        self.dwg.add(group)

        print("[DEBUG make_svg] Sauvegarde du fichier SVG")
        self.save()


# Bloc principal pour exécution directe
if __name__ == "__main__":
    # Usage : python3 nouvelle_roue.py [theme_json_path] [svg_output_path]
    if len(sys.argv) > 2:
        theme_path = sys.argv[1]
        output_svg = sys.argv[2]
    elif len(sys.argv) > 1:
        theme_path = sys.argv[1]
        output_svg = "nouvelle_roue.svg"
    else:
        theme_path = "theme_data.json"
        output_svg = "nouvelle_roue.svg"
    chart = AstroChartSVG(output_svg, theme_path)
    chart.make_svg()
    print(f"SVG généré : {output_svg} (données : {theme_path})")
