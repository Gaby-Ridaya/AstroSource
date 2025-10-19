# README – Structure du dossier `data/`

Ce dossier contient toutes les données générées et utilisées par l’application AstroSource côté backend. Il est organisé pour séparer les données par utilisateur, session ou usage partagé.

## Structure générale

```
data/
  <NomUser>/           # Dossier pour chaque utilisateur ou session (ex: Gaby, Amadeo, TestUser...)
    theme.json         # Thème astral de l’utilisateur (format JSON)
    roue.svg           # Roue astrologique générée (SVG)
    images/            # Images générées (OpenAI, planètes, etc.)
    prompts/           # Prompts utilisés/générés pour cet utilisateur
    ...                # Autres fichiers liés à l’utilisateur
  interpretations_json/ # Fichiers d’interprétation partagés (planètes, maisons, aspects...)
    planetes.json
    maisons.json
    ...
  <autres dossiers>/   # (ex: test_prompte/, dossiers temporaires, etc.)
```

## Détail des sous-dossiers

- `<NomUser>/` :
  - Contient toutes les données propres à un utilisateur ou une session.
  - Peut inclure :
    - `theme.json` : données du thème astral (planètes, maisons, aspects...)
    - `roue.svg` : roue astrologique personnalisée
    - `images/` : images générées pour ce thème
    - `prompts/` : prompts OpenAI ou autres générés pour ce thème
    - autres fichiers liés à l’utilisateur

- `interpretations_json/` :
  - Contient les fichiers JSON d’interprétation utilisés par tous les utilisateurs (planètes, maisons, aspects, etc.)
  - Ces fichiers servent de base pour générer les textes d’interprétation.

- Autres dossiers :
  - `test_prompte/`, `yop/`, etc. : dossiers de test, temporaires ou spécifiques à certains usages.

## Bonnes pratiques

- **Ne pas versionner** ce dossier dans Git (déjà ignoré dans `.gitignore`).
- Nettoyer régulièrement les dossiers inutilisés ou temporaires.
- Centraliser les ressources partagées dans `interpretations_json/`.
- Organiser les sous-dossiers par utilisateur pour éviter les collisions de fichiers.

---

*Ce fichier peut être adapté selon l’évolution de la structure ou des besoins du projet.*
Automatisation actuelle (juillet 2025)
Workflow complet automatisé :

Génération du thème astral (theme_<id>.json)
Génération du prompt artistique (prompt_final.txt)
Génération automatique de la roue astrologique SVG (theme_<id>.svg)
Génération d’un prompt d’interprétation poétique astrologique (prompt_interpretation.txt)
Tous les fichiers sont signés © 2025 Gaby Ridaya
Structure harmonisée : tous les scripts utilisent data/Utilisateurs/<Nom>/
Prêt pour l’intégration IA :

Les prompts générés sont prêts à être envoyés à une IA d’image ou de texte (OpenAI, Stable Diffusion, etc.)
Les fichiers sont organisés pour faciliter l’automatisation et la maintenance


Prêt pour l’intégration IA :

Les prompts générés sont prêts à être envoyés à une IA d’image ou de texte (OpenAI, Stable Diffusion, etc.)
Les fichiers sont organisés pour faciliter l’automatisation et la maintenance
Prochaines étapes possibles
Intégration directe avec une API d’IA pour générer les images et interprétations automatiquement
Ajout de notifications ou d’un suivi d’état pour informer l’utilisateur de l’avancement (chargement, image prête, etc.)
Interface web ou mobile pour lancer et visualiser les résultats
Amélioration de la gestion des utilisateurs et de l’historique
Sécurisation et gestion fine des droits d’accès
