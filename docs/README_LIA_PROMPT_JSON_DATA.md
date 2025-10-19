
# README — Explications pour LIA
#
# ---
#
# ## Synthèse de ce qui a été réalisé
#
# 1. Création et structuration des fichiers JSON artistiques :
#    - signes.json, Maisons.json, aspets.json, planetaires.json, planetes_dignites.json, ultra_perso.json, mystical_4k.json
#    - Chaque fichier contient des descriptions artistiques pour chaque élément astrologique
#
# 2. Script Python de fusion (`fusion_complte.py`) :
#    - Lit le thème utilisateur (data/[NomUser]/theme_xxx.json)
#    - Charge tous les fichiers JSON artistiques
#    - Pour chaque planète, assemble tous les prompts (planète, signe, maison, dignité, ultra_perso, mystical_4k, mystique)
#    - Pour chaque aspect, ajoute le prompt artistique correspondant
#    - Génère un prompt final complet et le sauvegarde dans un fichier texte
#
# 3. Workflow automatisé côté web :
#    - L’utilisateur remplit le formulaire sur la page ART Astro
#    - Les données sont envoyées au backend Flask
#    - Le backend calcule le thème, fusionne les prompts et prépare le texte pour l’IA
#
# 4. Documentation et exemples :
#    - README détaillé sur le workflow et la structure des fichiers
#    - Exemples de résultats attendus et de prompts générés
#
# ---
#
# ## Prochaine étape : Intégration avec DALL·E, Stable Diffusion, etc.
#
# 1. Ajouter un module Python pour envoyer le prompt généré à une API d’image (DALL·E, SD, etc.)
#    - Utiliser l’API officielle (openai, diffusers, etc.)
#    - Exemple :
#      ```python
#      import openai
#      # Charger la clé API depuis .env
#      # Envoyer le prompt à l’API DALL·E
#      response = openai.Image.create(prompt=prompt_final, n=1, size="1024x1024")
#      image_url = response['data'][0]['url']
#      ```
#    - Pour Stable Diffusion : utiliser le package diffusers ou une API tierce
#
# 2. Afficher ou sauvegarder l’image générée pour l’utilisateur
#    - Intégrer l’affichage dans la page web
#    - Permettre le téléchargement ou l’enregistrement dans le dossier utilisateur
#
# 3. (Optionnel) Ajouter des options de style ou de personnalisation dans le formulaire
#    - Choix du style artistique, format, influences, etc.
#
# ---
#
# Pour toute question ou adaptation, se référer aux scripts et à la documentation ci-dessous.

## Où générer une image astrologique ?

La fenêtre de génération d’image astrologique se trouve dans la page « ART Astro » de l’application web.

- Cette page affiche un grand formulaire de saisie astrologique (nom, date, heure, ville, pays).
- L’utilisateur remplit ce formulaire puis clique sur le bouton « Générer votre image astrale ».
- Le formulaire est transparent, stylé turquoise, et placé à gauche de la roue zodiacale.
- Après validation, le système LIA récupère les données et génère le prompt artistique, puis l’image.

Ce formulaire est le point d’entrée pour toute génération d’image astrologique personnalisée.
---

## 0. Que se passe-t-il quand un utilisateur veut générer une image astrologique ?

### Workflow complet pour LIA

1. **L’utilisateur clique sur le bouton "Générer une image astrologique" dans l’application.**
2. **LIA récupère le thème astrologique de l’utilisateur** (exemple : `data/TestUser/theme_xxx.json`).
3. **LIA charge tous les fichiers JSON artistiques** dans `Prompt_art_json/` (signes, maisons, aspects, planètes, dignités, ultra_perso, mystical_4k).
4. **LIA fusionne toutes les données** :
   - Pour chaque planète du thème, elle assemble le prompt planète, le prompt signe, le prompt maison, la dignité, les aspects, etc.
   - Pour chaque aspect, elle récupère le prompt artistique correspondant.
   - Pour chaque maison, elle récupère le prompt maison.
5. **LIA construit un prompt artistique complet** (texte détaillé, structuré, prêt pour l’IA image).
6. **LIA envoie ce prompt à l’API de génération d’image** (Stable Diffusion, DALL-E, etc.).
7. **L’image générée est affichée ou sauvegardée pour l’utilisateur.**

Ce processus est entièrement automatisé : l’utilisateur n’a qu’à cliquer, LIA s’occupe de tout le reste.

---

## Structure des fichiers JSON et workflow

Ce projet utilise plusieurs fichiers JSON pour générer des prompts artistiques astrologiques destinés à l’IA (LIA). Voici comment tout fonctionne :

---

## 1. Fichiers de données

- **data/[NomUser]/theme_xxx.json**
  - Contient le thème astrologique de l’utilisateur : positions des planètes, maisons, aspects, ascendant, MC, etc.
  - Exemple : `data/TestUser/theme_1753266684.json`

- **Prompt_art_json/**
  - **signes.json** : prompts artistiques pour chaque signe astrologique
  - **Maisons.json** : prompts pour chaque maison astrologique
  - **aspets.json** : prompts pour chaque aspect (conjonction, trigone, carré, etc.)
  - **planetaires.json** : prompts pour chaque planète
  - **planetes_dignites.json** : dignités (domicile, exaltation) pour chaque planète
  - **ultra_perso.json** et **mystical_4k.json** : enrichissements artistiques spéciaux

---

## 2. Fusion des données
section “Exemple de résultat attendu”
 /home/gaby/AstroSource/Boogy/bin/python /home/gaby/AstroSource/test_prompt_global.py
=== TEST GLOBAL DU THEME ARTISTIQUE ===

Planète : Venus (235.07°) — Signe : Scorpion — Maison 8
  [Prompt Planète] ♀ Vénus — La Splendeur Aimante
    Texte : A celestial muse reclining in a rose-garden that melts into the stars. She is adorned in velvet, copper jewelry, and golden spirals.
  [Prompt Signe] ♏️ 8. Scorpion — Le Gardien des Portes Invisibles
    Texte : A shamanic figure wrapped in shadow and violet flame, eyes glowing with inner vision. Influences: Zdzisław Beksiński’s underworld textures, alchemical ruins, Carrington’s psychic surrealism. Scorpion glyph carved in obsidian behind them.
  [Aspect] Conjonction entre Sun - Venus : ☌ Conjonction — Le Point d’Incandescence
    Prompt : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
  [Aspect] Trigone entre Venus - Saturn : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.

Planète : Mars (222.41°) — Signe : Scorpion — Maison 8
  [Prompt Planète] ♂ Mars — Le Guerrier du Feu Sacré
    Texte : A red-armored warrior emerging from volcanic mists, wielding a blade inscribed with glyphs of action and will.
  [Prompt Signe] ♏️ 8. Scorpion — Le Gardien des Portes Invisibles
    Texte : A shamanic figure wrapped in shadow and violet flame, eyes glowing with inner vision. Influences: Zdzisław Beksiński’s underworld textures, alchemical ruins, Carrington’s psychic surrealism. Scorpion glyph carved in obsidian behind them.
  [Dignité] Mars en domicile en Scorpion : Mars est chez lui en Bélier et en Scorpion, incarnant l’action, la passion et la transformation. Il est exalté en Capricorne, où il canalise sa force dans la persévérance et la stratégie.
  [Aspect] Conjonction entre Mercury - Mars : ☌ Conjonction — Le Point d’Incandescence
    Prompt : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
  [Aspect] Trigone entre Mars - Jupiter : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
  [Aspect] Trigone entre Mars - Saturn : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.

Planète : Jupiter (338.23°) — Signe : Poissons — Maison 12
  [Prompt Planète] ♃ Jupiter — Le Sage aux Mille Mondes
    Texte : A bearded philosopher seated in a colossal library floating among clouds, surrounded by scrolls, orbs, and astral maps.
  [Prompt Signe] ♓️ 12. Poissons — L’Onde de l’Invisible
    Texte : A figure dissolving into a sea of stars, eyes closed in ecstatic surrender. Her veil becomes the cosmos. Influences: pre-Raphaelite Virgin Mary, Neptune symbolism, and visionary art by Alex Grey.
  [Dignité] Jupiter en domicile en Poissons : Jupiter est chez lui en Sagittaire et en Poissons, porteur d’expansion, de foi et de sagesse. Il est exalté en Cancer, où il protège et nourrit.
  [Aspect] Carre entre Moon - Jupiter : □ Carré — Le Croisement Sacré
    Prompt : Un coffre caché dans la lumière, entouré de symboles de chance et d’abondance. Une figure découvre un trésor intérieur, baigné d’or et de nacre.
  [Aspect] Trigone entre Mercury - Jupiter : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
  [Aspect] Trigone entre Mars - Jupiter : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
  [Aspect] Trigone entre Jupiter - Uranus : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
  [Aspect] Carre entre Jupiter - Neptune : □ Carré — Le Croisement Sacré
    Prompt : Un coffre caché dans la lumière, entouré de symboles de chance et d’abondance. Une figure découvre un trésor intérieur, baigné d’or et de nacre.

Planète : Uranus (209.66°) — Signe : Balance — Maison 7
  [Prompt Planète] ♅ Uranus — Le Révélateur du Futur
    Texte : A radiant figure shattering a glass temple, lightning bolts dancing in their eyes. Futuristic sacred art, cyber fractals, electric glyphs.
  [Prompt Signe] ♎️ 7. Balance — La Danseuse des Mondes
    Texte : A celestial figure in perfect poise on a golden thread suspended between two worlds. Inspired by Byzantine iconography and pre-Raphaelite elegance. Behind her, a giant mandala of balance, half light, half shadow.
  [Aspect] Conjonction entre Mercury - Uranus : ☌ Conjonction — Le Point d’Incandescence
    Prompt : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
  [Aspect] Trigone entre Jupiter - Uranus : △ Trigone — Le Souffle Harmonique
    Prompt : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.

Planète : Neptune (248.73°) — Signe : Sagittaire — Maison 9
  [Prompt Planète] ♆ Neptune — Le Chant de l’Invisible
    Texte : A dream-being dissolving into a wave of stars, their eyes lost in an infinite ocean. Visionary surrealism meets deep spiritual art.
  [Prompt Signe] ♐️ 9. Sagittaire — L’Archer Céleste
    Texte : A centaur philosopher shooting an arrow into a cosmic spiral. His body is covered with constellations and inscriptions in ancient languages. A blend of Moreau’s mythological grandeur and visionary galactic landscape.
  [Aspect] Conjonction entre Moon - Neptune : ☌ Conjonction — Le Point d’Incandescence
    Prompt : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
  [Aspect] Carre entre Jupiter - Neptune : □ Carré — Le Croisement Sacré
    Prompt : Un coffre caché dans la lumière, entouré de symboles de chance et d’abondance. Une figure découvre un trésor intérieur, baigné d’or et de nacre.
  [Aspect] Sextile entre Neptune - Pluto : ⚹ Sextile — Le Passage Subtil
    Prompt : Two figures face each other across a sacred crossroad, each holding a staff carved with opposing glyphs. Between them, sparks fly.
  [Aspect] Conjonction entre Neptune - North Node : ☌ Conjonction — Le Point d’Incandescence
    Prompt : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.

--- PROMPTS DES MAISONS ---

--- PROMPTS DES ASPECTS ---

Aspect Conjonction entre Sun - Venus : ☌ Conjonction — Le Point d’Incandescence
  Texte : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
Aspect Trigone entre Sun - Saturn : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Carre entre Moon - Jupiter : □ Carré — Le Croisement Sacré
  Texte : Un coffre caché dans la lumière, entouré de symboles de chance et d’abondance. Une figure découvre un trésor intérieur, baigné d’or et de nacre.
Aspect Conjonction entre Moon - Neptune : ☌ Conjonction — Le Point d’Incandescence
  Texte : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
Aspect Sextile entre Moon - Pluto : ⚹ Sextile — Le Passage Subtil
  Texte : Two figures face each other across a sacred crossroad, each holding a staff carved with opposing glyphs. Between them, sparks fly.
Aspect Trigone entre Moon - Chiron : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Conjonction entre Moon - North Node : ☌ Conjonction — Le Point d’Incandescence
  Texte : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
Aspect Conjonction entre Mercury - Mars : ☌ Conjonction — Le Point d’Incandescence
  Texte : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
Aspect Trigone entre Mercury - Jupiter : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Conjonction entre Mercury - Uranus : ☌ Conjonction — Le Point d’Incandescence
  Texte : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.
Aspect Trigone entre Venus - Saturn : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Trigone entre Mars - Jupiter : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Trigone entre Mars - Saturn : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Trigone entre Jupiter - Uranus : △ Trigone — Le Souffle Harmonique
  Texte : Three floating figures connected by golden threads, forming a perfect triangle in the night sky. Each holds a glowing orb representing gifts and flow.
Aspect Carre entre Jupiter - Neptune : □ Carré — Le Croisement Sacré
  Texte : Un coffre caché dans la lumière, entouré de symboles de chance et d’abondance. Une figure découvre un trésor intérieur, baigné d’or et de nacre.
Aspect Carre entre Saturn - Chiron : □ Carré — Le Croisement Sacré
  Texte : Un coffre caché dans la lumière, entouré de symboles de chance et d’abondance. Une figure découvre un trésor intérieur, baigné d’or et de nacre.
Aspect Sextile entre Neptune - Pluto : ⚹ Sextile — Le Passage Subtil
  Texte : Two figures face each other across a sacred crossroad, each holding a staff carved with opposing glyphs. Between them, sparks fly.
Aspect Conjonction entre Neptune - North Node : ☌ Conjonction — Le Point d’Incandescence
  Texte : Two celestial beings fused in a spiral of light and darkness, indistinguishable yet distinct. A glowing mandala forms around them, symbol of unity and tension.

=== SYNTHESE ARTISTIQUE DU THEME ===

Fusion de tous les prompts pour une inspiration créative complète !
(À personnaliser selon tes besoins)

LIA doit :
- Lire le thème utilisateur (`data/[NomUser]/theme_xxx.json`)
- Lire tous les fichiers de prompts dans `Prompt_art_json/`
- Pour chaque planète du thème :
  - Récupérer le prompt planète, le prompt signe, le prompt maison, la dignité, les aspects, ultra_perso, mystical_4k
- Pour chaque aspect du thème :
  - Récupérer le prompt artistique correspondant
- Pour chaque maison :
  - Récupérer le prompt maison
- Fusionner toutes ces informations pour générer un prompt artistique complet

---

## 3. Génération du prompt final

- Le prompt final est un texte qui regroupe tous les éléments artistiques du thème astrologique
- Ce texte est utilisé par LIA pour générer une image (via Stable Diffusion, DALL-E, etc.)
- Exemple de workflow :
  1. LIA lit tous les JSON
  2. LIA fusionne les données comme dans le script `test_prompt_global.py`
  /home/gaby/AstroSource/test_prompte/test_prompt_global.py
  3. LIA construit le prompt artistique
  4. LIA envoie le prompt à l’API d’image
  5. L’image est affichée ou sauvegardée

---

## 4. Exemple de code pour LIA

```python
import json
# Charger tous les fichiers JSON
with open('Prompt_art_json/signes.json') as f: signes = json.load(f)
with open('Prompt_art_json/Maisons.json') as f: maisons = json.load(f)
with open('Prompt_art_json/aspets.json') as f: aspects = json.load(f)
with open('Prompt_art_json/planetaires.json') as f: planetaires = json.load(f)
with open('Prompt_art_json/planetes_dignites.json') as f: dignites = json.load(f)
with open('Prompt_art_json/ultra_perso.json') as f: ultra_perso = json.load(f)
with open('Prompt_art_json/mystical_4k.json') as f: mystical_4k = json.load(f)
with open('data/TestUser/theme_1753266684.json') as f: theme = json.load(f)
# Fusionner les données comme dans test_prompt_global.py
# Construire le prompt artistique
# Envoyer le prompt à l’API d’image
```

---

## 5. À personnaliser

- Tu peux enrichir le prompt avec des styles, des mantras, des influences artistiques, etc.
- Tu peux adapter la structure pour chaque utilisateur ou chaque style d’image

---

## 6. Résumé

- Les fichiers JSON sont la source principale pour LIA
- LIA doit fusionner ces données pour générer le prompt artistique
- Le prompt sert à créer l’image astrologique personnalisée

---

Pour toute question ou adaptation, se référer aux scripts : `test_prompt_global.py`, `fusion_prompt_lia.py`, `generate_final_prompt.py`.
/home/gaby/AstroSource/test_prompte

5bis. Choix du style artistique par l’utilisateur (option poétique)
Pour aller plus loin dans la personnalisation et l’expérience créative, il est possible de proposer à l’utilisateur de choisir une « ambiance artistique » pour la génération de son image astrologique. Ce choix ne révèle pas directement les peintres ou les techniques, mais oriente subtilement la fusion des influences dans le prompt final.

Exemples de catégories poétiques à proposer :
Lumière des Anciens (classique & visionnaire)
Brume romantique divine (romantique & poétique)
Mystères Symboliques (symboliste & mystique)
Rêve éveillé (surréaliste & onirique)
Fusion des astres (mélange céleste, inspiration libre)
L’utilisateur sélectionne simplement une ambiance, et le script adapte en interne la sélection des peintres, des textures et des influences pour générer un prompt cohérent avec ce choix. Le mystère est préservé, car la liste exacte des artistes ou des styles n’est jamais affichée.

Fonctionnement suggéré :
Afficher une liste de 3 à 5 ambiances poétiques lors de la génération de l’image.
L’utilisateur choisit celle qui l’inspire le plus.
Le script fusionne les prompts en privilégiant les styles, textures et influences correspondant à cette ambiance.
Le prompt final reste mystérieux, évocateur, et adapté à la sensibilité de l’utilisateur.
Ce système permet de varier naturellement les résultats, d’impliquer l’utilisateur dans le processus créatif, tout en gardant la magie et la poésie des images générées.

Lumière des Anciens
Brume romantique divine
Mystères Symboliques
Rêve éveillé
Fusion des astres 