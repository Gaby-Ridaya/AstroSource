import os
import sys
import shutil
from backend.fusion_complte import create_final_prompt
from backend.astro_calcule import generate_theme
from backend.utils.openai_image import (
    generate_image_with_openai,
    summarize_prompt_for_image,
    generate_interpretation_with_openai,
)
import subprocess


def generate_all(nom, date, heure, ville, pays, style, theme_id):
    user_dir = os.path.join("data", "Utilisateurs", nom.replace(" ", "_"))
    os.makedirs(user_dir, exist_ok=True)
    theme_path = os.path.join(user_dir, f"theme_{theme_id}.json")
    prompt_path = os.path.join(user_dir, "prompt_final.txt")
    svg_path = os.path.join(user_dir, f"theme_{theme_id}.svg")
    image_path = os.path.join(user_dir, f"theme_{theme_id}_openai.png")
    interpretation_path = os.path.join(user_dir, "interpretation_ia.txt")

    # 1. Génération du thème astral (JSON)
    try:
        src_json = generate_theme(nom, date, heure, ville, pays, export_path=theme_path)
        if not src_json or not os.path.exists(theme_path):
            print(f"Erreur astro_calcule: le fichier {theme_path} n'a pas été généré.")
    except Exception as e:
        print(f"Erreur astro_calcule: {e}")

    # 1.5. Ajouter les couleurs des signes au fichier JSON du thème utilisateur
    try:
        import json

        # Charger les couleurs depuis theme_data.json principal
        theme_config_path = os.path.join(
            os.path.dirname(__file__), "..", "theme_data.json"
        )
        theme_config_path = os.path.abspath(theme_config_path)

        if os.path.exists(theme_config_path) and os.path.exists(theme_path):
            # Lire les couleurs des signes
            with open(theme_config_path, "r", encoding="utf-8") as f:
                theme_config = json.load(f)

            # Lire le thème utilisateur
            with open(theme_path, "r", encoding="utf-8") as f:
                theme_user = json.load(f)

            # Ajouter les couleurs des signes au thème utilisateur
            if (
                "theme" in theme_config
                and "signs_glyphs_colors" in theme_config["theme"]
            ):
                # Mettre les couleurs au niveau racine du JSON utilisateur (comme le test_theme.json)
                theme_user["signs_glyphs_colors"] = theme_config["theme"][
                    "signs_glyphs_colors"
                ]
                print(
                    f"[WORKFLOW] Couleurs des signes ajoutées au thème utilisateur au niveau racine"
                )

                # Sauvegarder le thème utilisateur avec les couleurs
                with open(theme_path, "w", encoding="utf-8") as f:
                    json.dump(theme_user, f, ensure_ascii=False, indent=2)
                print(
                    f"[WORKFLOW] Thème utilisateur sauvegardé avec couleurs dans: {theme_path}"
                )
            else:
                print(f"[WORKFLOW] ATTENTION: Pas de couleurs dans {theme_config_path}")
                print(f"[WORKFLOW] Structure trouvée: {list(theme_config.keys())}")
                if "theme" in theme_config:
                    print(
                        f"[WORKFLOW] Clés dans theme: {list(theme_config['theme'].keys())}"
                    )
    except Exception as e:
        print(f"[WORKFLOW] Erreur lors de l'ajout des couleurs: {e}")

    # 2. Génération du prompt artistique
    try:
        create_final_prompt(
            theme_path, "Prompt_art_json", prompt_path, style_poetique_choisi=style
        )
    except Exception as e:
        print(f"Erreur fusion_complte: {e}")

    # 3. Génération du SVG astrologique
    try:
        from app.services.nouvelle_roue import AstroChartSVG

        os.makedirs(os.path.dirname(svg_path), exist_ok=True)
        # Maintenant utiliser directement le fichier du thème utilisateur qui contient déjà les couleurs
        print(f"[SVG] Utilisation du thème utilisateur avec couleurs: {theme_path}")
        chart = AstroChartSVG(svg_path, theme_path)

        # Le fichier contient déjà toutes les données (positions + couleurs)
        chart.make_svg()
        print(f"[SVG] SVG généré : {svg_path}")
    except Exception as e:
        print(f"Erreur SVG: {e}")

    # 4. Génération de l'image IA
    try:
        with open(prompt_path, encoding="utf-8") as f:
            prompt_text = f.read()
        prompt_court = summarize_prompt_for_image(prompt_text, style)
        if not prompt_court:
            prompt_court = f"Portrait astrologique artistique, style {style.lower()}, couleurs célestes, inspiration visionnaire."
        generate_image_with_openai(prompt_court, image_path)
    except Exception as e:
        print(f"Erreur image IA: {e}")

    # 5. Génération de l'interprétation IA
    try:
        with open(prompt_path, encoding="utf-8") as f:
            prompt_image = f.read()
        prompt_interpretation = (
            "Voici le prompt artistique (fichier prompt_final.txt) qui a servi à générer l'image astrologique du thème natal de l'utilisateur. "
            "En t'appuyant uniquement sur ce texte, rédige une interprétation astrologique poétique du thème, en t'inspirant du style et des enseignements de Max Heindel (sans jamais citer l'auteur), "
            "et en utilisant la poésie et la langue de William Shakespeare.\n\n"
            "Prompt artistique utilisé :\n" + prompt_image.strip() + "\n\n"
            "Commence ton interprétation :\n"
        )
        with open(
            os.path.join(user_dir, "prompt_interpretation.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(prompt_interpretation)
        generate_interpretation_with_openai(prompt_interpretation, interpretation_path)
    except Exception as e:
        print(f"Erreur interprétation IA: {e}")

    return {
        "image_path": image_path,
        "svg_path": svg_path,
        "interpretation_path": interpretation_path,
    }
