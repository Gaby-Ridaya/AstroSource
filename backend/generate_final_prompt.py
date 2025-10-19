import json

# Exemple de fusion des deux fichiers JSON pour générer un prompt final pour l'IA

def generate_final_prompt(prompt_json_path, astro_json_path, output_path):
    # Charger le prompt artistique
    with open(prompt_json_path, 'r', encoding='utf-8') as f:
        prompt_data = json.load(f)
    # Charger les données astrologiques
    with open(astro_json_path, 'r', encoding='utf-8') as f:
        astro_data = json.load(f)

    # Exemple d'extraction de données astro
    sign_dominant = astro_data.get('planetes', {}).get('Sun', None)
    ascendant = astro_data.get('ascendant', None)
    titre = astro_data.get('titre', '')

    # Construction du prompt final (texte)
    prompt_text = f"{titre}\n"
    prompt_text += prompt_data.get('Create a mystical and symbolic artwork inspired by a fusion of Pre-Raphaelite softness, Byzantine sacred solemnity, and contemporary visionary art. Add layers of depth with influences from', '') + "\n"
    prompt_text += '\n'.join(prompt_data.get('prompts', [])) + "\n"
    prompt_text += f"Astrological archetype: {prompt_data.get('Center the composition on an astrological archetype — for example', '')} "
    if sign_dominant:
        prompt_text += f"(Sun position: {sign_dominant}) "
    if ascendant:
        prompt_text += f"Ascendant: {ascendant} "
    prompt_text += "\n"
    prompt_text += f"Symbolic elements: {prompt_data.get('Surround this character with symbolic elements', '')}\n"
    prompt_text += f"Style: {prompt_data.get('Style', '')}\n"

    # Ajout d'autres données astro si besoin
    # prompt_text += f"Aspects: {astro_data.get('aspects', [])}\n"

    # Sauvegarde du prompt final
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prompt_text)
    print(f"Prompt final généré dans : {output_path}")


def process_all_users(prompt_json_path, fusion_dir="data/fusion", data_dir="data"):
    import os
    for user in os.listdir(data_dir):
        user_path = os.path.join(data_dir, user)
        if not os.path.isdir(user_path):
            continue
        # Cherche le fichier thème dans le dossier utilisateur
        theme_file = None
        for f in os.listdir(user_path):
            if f.startswith("theme_") and f.endswith(".json"):
                theme_file = os.path.join(user_path, f)
                break
        if not theme_file:
            print(f"Aucun thème trouvé pour {user}")
            continue
        # Cherche le fichier fusionné pour l'utilisateur
        fusion_file = os.path.join(fusion_dir, f"theme_{user.lower()}_fusion.json")
        if not os.path.exists(fusion_file):
            print(f"Aucun fichier fusionné pour {user}")
            continue
        output_file = os.path.join(user_path, "prompt_final.txt")
        generate_final_prompt(fusion_file, theme_file, output_file)

# Exemple d'utilisation automatique pour tous les utilisateurs
if __name__ == "__main__":
    process_all_users(prompt_json_path=None)

# Exemple d'utilisation
# generate_final_prompt(
#     '/home/gaby/AstroSource/Prompt_art_json/ultra_perso.json',
#     '/home/gaby/AstroSource/data/Gabriel/theme_1753100677.json',
#     '/home/gaby/AstroSource/data/Gabriel/prompt_final.txt'
# )
