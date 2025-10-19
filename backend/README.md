Workflow Terminal AstroSource (avec Boogy)
Ce workflow permet de générer, pour un utilisateur donné, :

Un thème astral complet (JSON)
Un prompt artistique détaillé (texte)
Une image artistique IA (PNG, via DALL·E 3)
Un SVG astrologique
Une interprétation poétique IA (texte)
Prérequis
Python 3.11
Environnement virtuel activé :
source Boogy/bin/activate

Variables d’environnement .env avec ta clé OpenAI
Lancement du workflow
Depuis la racine du projet :

python gen_prompt_terminal.py

## Déroulement du workflow

1. **Saisie des informations utilisateur**
   - Nom
   - Date de naissance (YYYY-MM-DD)
   - Heure de naissance (HH:MM)
   - Ville
   - Pays (code, ex : FR)
   - Choix du style artistique (menu interactif)

2. **Calcul du thème astral**
   - Génération d’un fichier JSON dans `data/Utilisateurs/<Nom>/theme_<id>.json`

3. **Génération du prompt artistique**
   - Création d’un prompt détaillé dans `data/Utilisateurs/<Nom>/prompt_final.txt`

4. **Génération de l’image IA (DALL·E 3)**
   - Résumé créatif du prompt via GPT
   - Génération et sauvegarde de l’image PNG dans `data/Utilisateurs/<Nom>/theme_<id>_openai.png`

5. **Génération du SVG astrologique**
   - SVG créé dans `data/Utilisateurs/<Nom>/theme_<id>.svg`

6. **Génération de l’interprétation poétique IA**
   - Prompt d’interprétation : `data/Utilisateurs/<Nom>/prompt_interpretation.txt`
   - Interprétation IA : `data/Utilisateurs/<Nom>/interpretation_ia.txt`

### Exemple de fichiers générés

- `data/Utilisateurs/Caroline/theme_test_terminal.json` (thème astral)
- `data/Utilisateurs/Caroline/prompt_final.txt` (prompt artistique)
- `data/Utilisateurs/Caroline/theme_test_terminal_openai.png` (image IA)
- `data/Utilisateurs/Caroline/theme_test_terminal.svg` (SVG astrologique)
- `data/Utilisateurs/Caroline/interpretation_ia.txt` (interprétation poétique)

---

Le workflow est interactif et guide l’utilisateur étape par étape. Les fichiers sont organisés par utilisateur dans `data/Utilisateurs/<Nom>/`.


