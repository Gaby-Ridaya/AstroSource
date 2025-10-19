📜 README — Journal de modifications AstroSource (2025-08-09)
1️⃣ Objectif de la journée

Mettre en place un flux complet permettant :

    De détecter automatiquement le dernier JSON theme_<user>.json généré côté utilisateur.

    De lancer automatiquement la génération d'image à partir de ce JSON, sans intervention manuelle.

    De connecter ce flux à l’API existante (/api/astro-image/<user>).

    De résoudre les problèmes liés à Compel (tokenizer_2) et aux modules manquants.

2️⃣ Fichiers modifiés ou créés
pipeline.py

    Nouvelle fonction process_user_theme(json_path=None) :

        Cherche automatiquement le dernier JSON généré dans /home/gaby/AstroSource/data/Utilisateurs/<username>/theme_<username>.json.

        Détermine le chemin de sortie .png correspondant.

        Appelle generate_astro_image() (mode "figuratif").

        Archive et log le résultat (archive_results() et log_generation()).

        Retourne un dictionnaire avec user_id, prompt, image.

Particularité :

    Si style_image_path (moodboard) n’existe pas, on utilise le PNG généré.

    En cas d’erreur, on renvoie quand même "image" si elle existe, pour éviter les KeyError côté API.

image_gen.py

    Corrigé l’initialisation de Compel pour supprimer tokenizer_2 (non supporté dans ta version 2.1.1).

    Confirmé que le pipeline SDXL se lance sur GPU (cuda) avec logs au démarrage.

Répertoires de sortie

    Tous les fichiers générés (.json, .svg, .png, .txt) sont produits dans :

    /home/gaby/AstroSource/data/Utilisateurs/<username>/

3️⃣ Problèmes rencontrés et résolus
Problème Solution
Erreur tokenizer_2 dans Compel Retrait du paramètre tokenizer_2 → utilisation de la signature correcte pour Compel 2.1.1
Module manquant app.services.delivery Création/remplacement des imports vers des modules valides (archiver/logger)
KeyError: 'image' lors de l'appel API Dans pipeline.py, renvoi d’une clé "image" même en cas d'erreur si le PNG existe
4️⃣ Prochaines étapes
Option A — Optimiser SDXL

    Compactage des prompts pour éviter la troncature CLIP (77 tokens).

    Ajout d’un scheduler Karras et d’un refiner pour plus de détails.

    Possibilité d’upscale ×2 pour la qualité finale.

Option B — Backend alternatif OpenAI

    Ajouter un fichier openai_image_gen.py avec fonction :

    def generate_openai_image(prompt, out_path):
        # Appel à l’API OpenAI DALL·E 3 ou gpt-image

    Ajout d’un switch dans pipeline.py pour choisir le backend (sdxl ou openai).

5️⃣ Commandes utiles
Activer l’environnement

source /home/gaby/AstroSource/Boogy/bin/activate

Lancer le backend

cd /home/gaby/AstroSource/backend
python main.py

Vérifier la version de Compel

pip show compel

6️⃣ Schéma simplifié du flux actuel

[Frontend bouton] → [nouvelle_roue.py] → Génère SVG
↓
[astro_calcule.py] → Génère JSON
↓
/data/Utilisateurs/<username>/theme\_<username>.json
↓
[pipeline.py process_user_theme()]
↓
[image_gen.py generate_astro_image()]
↓
PNG dans /data/Utilisateurs/<username>/

💡 Note perso pour demain :

    Si tu passes sur OpenAI, garde astro_prompt_fusion.py pour préparer le prompt, et on remplace juste la partie génération d’image.

    Pour tester vite : on pourra mettre un paramètre backend=openai dans l’URL de génération.

Veux-tu que je te prépare aussi la version Option B (OpenAI) dans un petit fichier openai_image_gen.py pour que demain tu n’aies qu’à coller ta clé API et tester ?
Comme ça tu démarres direct avec DALL·E 3.
