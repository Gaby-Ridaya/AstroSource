import json

"""
Copyright © 2025 Gabriel Alba
Tous droits réservés.
Usage personnel uniquement. Toute utilisation commerciale ou publication nécessite une autorisation écrite.
Voir LICENSE pour les détails.
"""
import json
import os


# Fonction pour récupérer le signe astrologique à partir du degré
def deg_to_signe(deg):
    signes = [
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
    return signes[int(deg // 30) % 12]


# Fonction pour récupérer la maison astrologique
def deg_to_maison(maison_num):
    return f"Maison {maison_num}"


# Fonction principale pour créer le prompt
def create_final_prompt(
    theme_path, prompt_dir, output_path, style_poetique_choisi=None
):
    final_prompt = ""
    # --- Style poétique sélectionné ---
    STYLE_POETIQUE = {
        "Lumière des Anciens": {
            "artistes": ["Raphaël", "William Blake", "Leonard de Vinci"],
            "textures": ["lumière dorée", "fresque ancienne", "halo mystique"],
            "ambiance": ["visionnaire", "classique", "sacré"],
        },
        "Brume romantique divine": {
            "artistes": ["Turner", "Friedrich", "Bouguereau"],
            "textures": ["brume", "lumière diffuse", "voile éthéré"],
            "ambiance": ["romantique", "poétique", "divin"],
        },
        "Mystères Symboliques": {
            "artistes": ["Odilon Redon", "Gustave Moreau", "Fernand Khnopff"],
            "textures": ["pastel vaporeux", "ombres colorées", "symboles énigmatiques"],
            "ambiance": ["mystique", "symboliste", "rêveur"],
        },
        "Rêve éveillé": {
            "artistes": ["Dali", "Carrington", "Ernst"],
            "textures": ["surréalisme", "formes flottantes", "visions oniriques"],
            "ambiance": ["onirique", "surréaliste", "éveillé"],
        },
        "Fusion des astres": {
            "artistes": ["Alex Grey", "Hilma af Klint", "Kandinsky"],
            "textures": ["galaxie", "spirale céleste", "lumière cosmique"],
            "ambiance": ["céleste", "libre", "inspiration"],
        },
    }
    # --- Mapping des styles poétiques ---
    styles_artistiques = {
        "Lumière des Anciens": {
            "artistes": ["Raphaël", "Rembrandt", "Botticelli", "Vermeer"],
            "textures": ["lumière dorée", "clair-obscur", "fresque", "velours"],
            "ambiance": "visionnaire, classique, noble",
        },
        "Brume romantique divine": {
            "artistes": [
                "Friedrich",
                "Turner",
                "Delacroix",
                "Constable",
                "Monet",
                "Renoir",
                "Sisley",
                "Pissarro",
                "Degas",
                "Caillebotte",
            ],
            "textures": ["brume", "lumière diffuse", "pastel", "rosée", "voile"],
            "ambiance": "romantique, poétique, rêveur, impressionniste",
        },
        "Mystères Symboliques": {
            "artistes": ["Moreau", "Redon", "Khnopff", "Böcklin"],
            "textures": ["symboles", "miroir", "aura", "ombre colorée"],
            "ambiance": "mystique, profond, secret",
        },
        "Rêve éveillé": {
            "artistes": ["Dali", "Chagall", "Ernst", "Leonora Carrington"],
            "textures": ["surréaliste", "flottant", "translucide", "irisé"],
            "ambiance": "onirique, étrange, visionnaire",
        },
        "Fusion des astres": {
            "artistes": ["Kandinsky", "Klee", "Hilma af Klint", "Miro"],
            "textures": ["cosmique", "fusion", "éclat", "spirale"],
            "ambiance": "libre, céleste, expérimental",
        },
    }
    # Vérification de l'existence du fichier thème
    if not os.path.exists(theme_path):
        raise FileNotFoundError(f"Fichier thème introuvable : {theme_path}")
    with open(theme_path, "r", encoding="utf-8") as f:
        try:
            theme = json.load(f)
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du fichier thème : {e}")

    # Si un style global est choisi, l'appliquer à toutes les planètes
    # Appliquer le style choisi à toutes les planètes du thème
    if style_poetique_choisi:
        style_par_planete = {
            planet: style_poetique_choisi for planet in theme.get("planetes", {}).keys()
        }
    else:
        style_par_planete = {
            "Sun": "Lumière des Anciens",
            "Moon": "Brume romantique divine",
            "Mercury": "Mystères Symboliques",
            "Venus": "Rêve éveillé",
            "Mars": "Fusion des astres",
            "Jupiter": "Lumière des Anciens",
            "Saturn": "Mystères Symboliques",
            "Uranus": "Fusion des astres",
            "Neptune": "Rêve éveillé",
            "Pluto": "Mystères Symboliques",
            "Chiron": "Brume romantique divine",
            "North Node": "Fusion des astres",
        }

    # Ajout de l'en-tête artistique au début du prompt
    # Récupération des infos du style poétique choisi
    style_data = styles_artistiques.get(style_poetique_choisi, {})
    ambiance = style_data.get("ambiance", "Ambiance inconnue")
    influences = style_data.get("artistes", ["Artiste inconnu"])
    textures = style_data.get("textures", ["Texture inconnue"])
    final_prompt += (
        f"Ambiance : {ambiance}. "
        f"Influences : {', '.join(influences)}. "
        f"Textures : {', '.join(textures)}.\n\n"
    )
    # Section : Aspects majeurs du thème
    ASPECT_SYMBOL_TO_NAME = {
        "☌": "Conjonction",
        "△": "Trigone",
        "□": "Carre",
        "☍": "Opposition",
        "✶": "Sextile",
        "✷": "Sextile",
        "⚹": "Sextile",
    }
    aspects_majeurs = {"Conjonction", "Carre", "Trigone", "Opposition", "Sextile"}
    if "aspects" in theme:
        with open(f"{prompt_dir}/aspets.json", "r", encoding="utf-8") as f:
            aspects_json = json.load(f)
        final_prompt += "--- Aspects majeurs du thème ---\n"
        for aspect in theme["aspects"]:
            aspect_symbol = aspect.get("aspect")
            aspect_type = ASPECT_SYMBOL_TO_NAME.get(aspect_symbol)
            if aspect_type in aspects_majeurs:
                aspect_info = aspects_json.get(aspect_type, {})
                titre = aspect_info.get("titre", "")
                prompt_artistique = aspect_info.get("prompt", "")
                style = aspect_info.get("style", "")
                texture = aspect_info.get("texture", "")
                mantra = aspect_info.get("mantra", "")
                planetes = aspect.get("planetes", [])
                final_prompt += (
                    f"{planetes} ({aspect_symbol} {aspect_type}) : {titre}\n"
                )
                if prompt_artistique:
                    final_prompt += f"  Prompt artistique : {prompt_artistique}\n"
                if style:
                    final_prompt += f"  Style : {style}\n"
                if texture:
                    final_prompt += f"  Texture : {texture}\n"
                if mantra:
                    final_prompt += f"  Mantra : {mantra}\n"
                final_prompt += "\n"
    # Définition des éléments par signe
    elements_signes = {
        "Bélier": "Feu",
        "Lion": "Feu",
        "Sagittaire": "Feu",
        "Taureau": "Terre",
        "Vierge": "Terre",
        "Capricorne": "Terre",
        "Gémeaux": "Air",
        "Balance": "Air",
        "Verseau": "Air",
        "Cancer": "Eau",
        "Scorpion": "Eau",
        "Poissons": "Eau",
    }

    # Calcul du nombre de planètes par élément
    element_count = {"Feu": 0, "Terre": 0, "Air": 0, "Eau": 0}
    for planet, deg in theme.get("planetes", {}).items():
        signe = deg_to_signe(deg)
        elem = elements_signes.get(signe, "?")
        if elem in element_count:
            element_count[elem] += 1

    # Bloc résumé des éléments dominants
    final_prompt += "\n--- Éléments dominants du thème ---\n"
    for elem, count in element_count.items():
        final_prompt += f"{elem} : {count} planète(s)\n"
    final_prompt += "\n"

    # Section : Signe sur la cuspide de chaque maison avec description abstraite (plus d'animaux mythiques)
    if "maisons_cuspides" in theme:
        final_prompt += (
            "--- Signe et symbolique abstraite sur la cuspide de chaque maison ---\n"
        )
        with open(
            f"{prompt_dir}/symbolique_abstraite.json", "r", encoding="utf-8"
        ) as f:
            symbolique_abstraite_json = json.load(f)
        maisons_abstraites = symbolique_abstraite_json.get(
            "maison_animaux_mythiques", {}
        )
        for maison_num, signe in theme["maisons_cuspides"].items():
            elem = elements_signes.get(signe, "?")
            maison_abstraite = maisons_abstraites.get(str(maison_num), {})
            description_abstraite = maison_abstraite.get("description abstraite", "")
            final_prompt += f"Maison {maison_num} en {signe} ({elem}) : "
            if description_abstraite:
                final_prompt += f"{description_abstraite}"
            final_prompt += "\n"
        final_prompt += "\n"

    # Ajout spécial pour Mystères Symboliques : intégrer toute la symbolique abstraite
    if style_poetique_choisi and style_poetique_choisi.startswith(
        "Mystères Symboliques"
    ):
        with open(
            f"{prompt_dir}/symbolique_abstraite.json", "r", encoding="utf-8"
        ) as f:
            symbolique_abstraite_json = json.load(f)
        maisons_abstraites = symbolique_abstraite_json.get(
            "maison_animaux_mythiques", {}
        )
        final_prompt += (
            "--- Symbolique complète abstraite des maisons (Mystères Symboliques) ---\n"
        )
        for num, maison in maisons_abstraites.items():
            description_abstraite = maison.get("description abstraite", "")
            final_prompt += f"Maison {num} : {description_abstraite}\n"
        final_prompt += "\n"

    # Charger la palette couleurs zodiacale
    with open(f"{prompt_dir}/palette_couleurs.json", "r", encoding="utf-8") as f:
        palette_data = json.load(f)
    zodiac_map = palette_data.get("zodiac_artist_map", {})

    # Charger les infos artistiques des signes
    with open(f"{prompt_dir}/signes.json", "r", encoding="utf-8") as f:
        signes_infos = json.load(f)

    # Charger le texte du nombre d'or
    with open(f"{prompt_dir}/nombre_dor.json", "r", encoding="utf-8") as f:
        nombre_dor_data = json.load(f)
    texte_nombre_dor = nombre_dor_data.get("texte", "")

    # Section : Palette & style des signes dominants
    signes_dominants = []
    if "Sun" in theme.get("planetes", {}):
        signes_dominants.append(("Soleil", deg_to_signe(theme["planetes"]["Sun"])))
    if "ascendant" in theme:
        signes_dominants.append(("Ascendant", theme["ascendant"]))
    if "Moon" in theme.get("planetes", {}):
        signes_dominants.append(("Lune", deg_to_signe(theme["planetes"]["Moon"])))
    if "milieu_ciel" in theme:
        signes_dominants.append(("Milieu du Ciel", theme["milieu_ciel"]))

    if signes_dominants:
        final_prompt += "\n--- Palette & style des signes dominants du thème ---\n"
        for label, signe in signes_dominants:
            info = zodiac_map.get(signe, {})
            peintre = info.get("peintre", "")
            couleurs = info.get("couleurs", "")
            style_palette = info.get("style", "")
            symbolique = info.get("symbolique", "")
            signe_info = signes_infos.get(signe, {})
            titre = signe_info.get("titre", "")
            prompt_signe = signe_info.get("prompt", "")
            style_signe = signe_info.get("style", "")
            mantra = signe_info.get("mantra", "")
            final_prompt += f"{label} en {signe} :\n"
            if peintre:
                final_prompt += f"  Peintre : {peintre}\n"
            if couleurs:
                final_prompt += f"  Couleurs : {couleurs}\n"
            if style_palette:
                final_prompt += f"  Style (palette) : {style_palette}\n"
            if symbolique:
                final_prompt += f"  Symbolique (palette) : {symbolique}\n"
            if titre:
                final_prompt += f"  Titre : {titre}\n"
            if prompt_signe:
                final_prompt += f"  Prompt artistique : {prompt_signe}\n"
            if style_signe:
                final_prompt += f"  Style (signe) : {style_signe}\n"
            if mantra:
                final_prompt += f"  Mantra : {mantra}\n"
            final_prompt += "\n"
        if texte_nombre_dor:
            final_prompt += f"Nombre d'or : {texte_nombre_dor}\n\n"
    # Charger données astrologiques
    with open(theme_path, "r", encoding="utf-8") as f:
        theme = json.load(f)

    # Charger tous les fichiers prompts artistiques supplémentaires
    with open(f"{prompt_dir}/signes.json", "r", encoding="utf-8") as f:
        signes_data = json.load(f)
    with open(f"{prompt_dir}/Maisons.json", "r", encoding="utf-8") as f:
        maisons_data = json.load(f)
    with open(f"{prompt_dir}/planetaires.json", "r", encoding="utf-8") as f:
        planetaires_data = json.load(f)
    with open(f"{prompt_dir}/aspets.json", "r", encoding="utf-8") as f:
        aspects_data = json.load(f)
    with open(f"{prompt_dir}/ultra_perso.json", "r", encoding="utf-8") as f:
        ultra_perso_data = json.load(f)
    with open(f"{prompt_dir}/mystical_4k.json", "r", encoding="utf-8") as f:
        mystical_4k_data = json.load(f)
    with open(f"{prompt_dir}/mystique.json", "r", encoding="utf-8") as f:
        mystique_data = json.load(f)
    with open(f"{prompt_dir}/planetes_dignites.json", "r", encoding="utf-8") as f:
        dignites_data = json.load(f)
    with open(f"{prompt_dir}/astro_peinter.json", "r", encoding="utf-8") as f:
        peinter_data = json.load(f)
    with open(f"{prompt_dir}/Filippo.json", "r", encoding="utf-8") as f:
        filippo_data = json.load(f)
    with open(f"{prompt_dir}/impressionniste_associe.json", "r", encoding="utf-8") as f:
        impressionniste_associe_data = json.load(f)
    with open(f"{prompt_dir}/nombre_dor.json", "r", encoding="utf-8") as f:
        nombre_dor_data = json.load(f)
    with open(f"{prompt_dir}/palette_couleurs.json", "r", encoding="utf-8") as f:
        palette_couleurs_data = json.load(f)
    with open(f"{prompt_dir}/planete_peintre.json", "r", encoding="utf-8") as f:
        planete_peintre_data = json.load(f)
    with open(f"{prompt_dir}/symbolique_abstraite.json", "r", encoding="utf-8") as f:
        symbolique_data = json.load(f)
    # Nouveaux fichiers enrichis et variantes
    with open(f"{prompt_dir}/enriched_nombre_dor.json", "r", encoding="utf-8") as f:
        enriched_nombre_dor_data = json.load(f)
    with open(
        f"{prompt_dir}/enriched_nombre_dor_abstrait.json", "r", encoding="utf-8"
    ) as f:
        enriched_nombre_dor_abstrait_data = json.load(f)
    with open(
        f"{prompt_dir}/enriched_symbolique_abstraite.json", "r", encoding="utf-8"
    ) as f:
        enriched_symbolique_abstraite_data = json.load(f)
    with open(f"{prompt_dir}/nombre_dor_abstrait.json", "r", encoding="utf-8") as f:
        nombre_dor_abstrait_data = json.load(f)

    final_prompt = theme.get("titre", "") + "\n\n"
    # Définir artiste_principal selon le style choisi
    if style_poetique_choisi:
        style_data = styles_artistiques.get(style_poetique_choisi, {})
        artistes = style_data.get("artistes", ["Artiste inconnu"])
        artiste_principal = artistes[0] if artistes else "Artiste inconnu"
    else:
        artiste_principal = "Artiste inconnu"
    # Ajout du style poétique choisi
    final_prompt += f"Ambiance artistique choisie : {style_poetique_choisi}\n"
    final_prompt += f"Influence principale : {artiste_principal}\n"
    final_prompt += f"Textures associées : {textures}\n"
    final_prompt += f"Ambiances : {ambiance}\n\n"
    # ...existing code...
    # Fusionner tous les styles et influences
    final_prompt += "--- Fusion des styles et influences ---\n"
    # Impressionniste
    if "description" in impressionniste_associe_data:
        final_prompt += (
            "Influence impressionniste : "
            + impressionniste_associe_data["description"]
            + "\n"
        )
    # Palette de couleurs
    if "couleurs" in palette_couleurs_data:
        final_prompt += (
            "Palette de couleurs : "
            + ", ".join(palette_couleurs_data["couleurs"])
            + "\n"
        )
    # Nombre d'or
    if "texte" in nombre_dor_data:
        final_prompt += "Nombre d'or : " + nombre_dor_data["texte"] + "\n"
    # Symbolique
    if "mantra" in symbolique_data:
        final_prompt += "Symbolique : " + symbolique_data["mantra"] + "\n"
    # Planète peintre
    if "description" in planete_peintre_data:
        final_prompt += (
            "Planète peintre : " + planete_peintre_data["description"] + "\n"
        )
    # Filippo
    if "influences" in filippo_data:
        if isinstance(filippo_data["influences"], list):
            final_prompt += (
                "Influences Filippo : " + ", ".join(filippo_data["influences"]) + "\n"
            )
        else:
            final_prompt += (
                "Influences Filippo : " + str(filippo_data["influences"]) + "\n"
            )

    # Boucle sur chaque planète pour générer le prompt
    for planet, deg in theme["planetes"].items():
        signe = deg_to_signe(deg)
        maison_num = theme["planetes_maison"][planet]
        maison = deg_to_maison(maison_num)

        planet_prompt = planetaires_data.get(planet, {}).get("texte", "")
        signe_prompt = signes_data.get(signe, {}).get("texte", "")
        maison_prompt = maisons_data.get(maison, {}).get("texte", "")
        ultra_perso_prompt = ultra_perso_data.get(planet, "")
        mystical_prompt = mystical_4k_data.get(planet, "")
        mystique_prompt = mystique_data.get(planet, "")
        dignite_prompt = dignites_data.get(planet, {}).get("dignite", "")

        # Logique de style :
        if style_poetique_choisi == "Lumière des Anciens":
            # On garde le mapping classique astrologique
            painter_example = None
            # 1. Style spécifique planète
            for key, val in peinter_data.get("examples", {}).items():
                if planet in key:
                    painter_example = val
                    break
            # 2. Style selon le signe
            if not painter_example:
                signe_styles = {
                    "Bélier": "Le Caravage (dramatisme, force)",
                    "Taureau": "Renoir (chaleur, sensualité)",
                    "Gémeaux": "Vermeer (lumière, subtilité)",
                    "Cancer": "Rembrandt (émotion, clair-obscur)",
                    "Lion": "Raphaël (noblesse, éclat)",
                    "Vierge": "Blake (détail, symbolisme)",
                    "Balance": "Botticelli (harmonie, grâce)",
                    "Scorpion": "Friedrich (mystère, profondeur)",
                    "Sagittaire": "Friedrich (horizon, quête)",
                    "Capricorne": "Rembrandt (structure, sagesse)",
                    "Verseau": "William Blake (visionnaire, originalité)",
                    "Poissons": "Vermeer (rêverie, lumière douce)",
                }
                painter_example = signe_styles.get(signe, None)
            # 3. Style selon la maison
            if not painter_example:
                maison_styles = {
                    "Maison 1": "Botticelli (identité, douceur)",
                    "Maison 2": "Renoir (matière, abondance)",
                    "Maison 3": "Vermeer (communication, subtilité)",
                    "Maison 4": "Rembrandt (racines, émotion)",
                    "Maison 5": "Raphaël (créativité, amour)",
                    "Maison 6": "Blake (service, détail)",
                    "Maison 7": "Botticelli (relation, harmonie)",
                    "Maison 8": "Friedrich (transformation, mystère)",
                    "Maison 9": "Friedrich (quête, horizon)",
                    "Maison 10": "Rembrandt (réalisation, structure)",
                    "Maison 11": "William Blake (collectif, vision)",
                    "Maison 12": "Vermeer (rêve, intériorité)",
                }
                painter_example = maison_styles.get(maison, None)
            # 4. Défaut
            painter_ref = (
                painter_example
                if painter_example
                else "Botticelli (préférence subtile)"
            )
        else:
            # Pour tous les autres styles, on applique la logique du style poétique choisi
            style_artistes = styles_artistiques.get(style_poetique_choisi, {}).get(
                "artistes", ["Artiste inconnu"]
            )
            idx = list(theme["planetes"].keys()).index(planet) % len(style_artistes)
            painter_ref = f"{style_artistes[idx]} ({style_poetique_choisi})"

        # Animal mythique et symbolique pour la maison
        maison_abstraite = symbolique_data.get("maison_animaux_mythiques", {}).get(
            str(maison_num), {}
        )
        description_abstraite = maison_abstraite.get("description abstraite", "")
        animal_str = f" | {description_abstraite}" if description_abstraite else ""

        # Déterminer le style pour la planète
        style_choisi = style_par_planete.get(planet, "Brume romantique divine")
        style_data = styles_artistiques.get(style_choisi)
        if style_data:
            influences = style_data["artistes"]
            textures = style_data["textures"]
            ambiance = style_data["ambiance"]
        else:
            influences = ["Artiste inconnu"]
            textures = ["texture inconnue"]
            ambiance = "ambiance inconnue"

        # Ajout spécial pour Fusion des astres : fusion Filippo + nombre d'or
        fusion_inspirations = ""
        if style_poetique_choisi == "Fusion des astres":
            # Charger Filippo et nombre d'or
            filippo = filippo_data.get("zodiac_perspective_brunelleschi", {})
            nombre_or = nombre_dor_data.get("zodiac_plantes_fleurs_nombre_or", {})
            key = f"{maison_num}_{signe}"
            # Si la clé existe dans Filippo
            fil = filippo.get(key, {})
            nom_fleur = fil.get("plante", "")
            couleur_fleur = fil.get("couleur", "")
            perspective = fil.get("perspective", "")
            inspiration = fil.get("inspiration", "")
            # Pour nombre d'or
            ndor = nombre_or.get(key, {})
            nombre_or_txt = ndor.get("nombre_or", "")
            motif = ndor.get("motif", "")
            # Fusionner les deux
            fusion_inspirations = f"[Fusion artistique] Fleur sacrée : {nom_fleur} ({couleur_fleur}). Perspective : {perspective} Inspiration : {inspiration} | Géométrie sacrée : {nombre_or_txt} Motif : {motif}"

        # Ajouter au prompt final
        final_prompt += f"{planet} en {signe}, {maison} : {planet_prompt} {signe_prompt} {maison_prompt} {ultra_perso_prompt} {mystical_prompt} {mystique_prompt} {dignite_prompt} | Style peintre recommandé : {painter_ref}{animal_str}\n"
        final_prompt += f"  [Style poétique] Ambiance : {ambiance} | Influences : {', '.join(influences)} | Textures : {', '.join(textures)}\n"
        if fusion_inspirations:
            final_prompt += f"  {fusion_inspirations}\n"
        final_prompt += "\n"

    # Ajouter les aspects
    final_prompt += "Aspects astrologiques détaillés :\n"
    for aspect in theme["aspects"]:
        aspect_symbol = aspect.get("aspect")
        aspect_type = ASPECT_SYMBOL_TO_NAME.get(aspect_symbol)
        aspect_info = aspects_data.get(aspect_type, {}) if aspect_type else {}
        planetes_concernees = aspect["planetes"]
        titre = aspect_info.get("titre", "")
        prompt_artistique = aspect_info.get("prompt", "")
        style = aspect_info.get("style", "")
        texture = aspect_info.get("texture", "")
        mantra = aspect_info.get("mantra", "")
        final_prompt += f"{planetes_concernees} ({aspect_symbol}{' ' + aspect_type if aspect_type else ''}) : {titre}\n"
        if prompt_artistique:
            final_prompt += f"  Prompt artistique : {prompt_artistique}\n"
        if style:
            final_prompt += f"  Style : {style}\n"
        if texture:
            final_prompt += f"  Texture : {texture}\n"
        if mantra:
            final_prompt += f"  Mantra : {mantra}\n"
        final_prompt += "\n"

    # Ajout de la mention copyright/licence en fin de prompt
    final_prompt += "\n---\n© 2025 Gabriel Alba — Tous droits réservés.\nUsage personnel uniquement. Toute utilisation commerciale ou publication nécessite une autorisation écrite.\nVoir LICENSE pour les détails.\n---\n"
    # Sauvegarder le prompt final
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_prompt)

    print(f"Prompt généré avec succès : {output_path}")


# Exemple d'utilisation :
if __name__ == "__main__":
    # Génération du prompt artistique pour Andrea
    theme_json = "/home/gaby/AstroSource/data/Utilisateurs/Andrea/theme_simple.json"
    prompts_json_dir = "/home/gaby/AstroSource/Prompt_art_json"
    output_file = (
        "/home/gaby/AstroSource/data/Utilisateurs/Andrea/prompt_artistique.txt"
    )

    create_final_prompt(theme_json, prompts_json_dir, output_file)
