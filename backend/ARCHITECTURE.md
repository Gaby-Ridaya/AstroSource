
# 🏗️ Architecture AstroSource Pro

```
AstroSource/
├── backend/                    # API Backend
│   ├── app/                   # Application principale
│   │   ├── api/              # Routes API
│   │   │   └── routes/       # Modules de routage
│   │   │       ├── status.py           # Status API
│   │   │       ├── etude_astro.py      # Interprétations
│   │   │       ├── nouvelle_roue.py    # Génération SVG
│   │   │       └── prompt_generation.py # 🆕 Génération Prompts IA
│   │   ├── core/             # Configuration
│   │   │   ├── config.py     # Settings avec Pydantic
│   │   │   └── logging.py    # Logging professionnel
│   │   └── services/         # Logique métier
│   │       ├── astro_generation.py     # Service SVG
│   │       ├── interpretation.py       # Service interprétations
│   │       └── prompt_generation.py    # 🆕 Service Prompts IA
│   ├── scripts/              # Scripts d'administration
│   │   └── fusion_complte_legacy.py   # Ancien système
│   └── tests/                # Tests automatisés
├── frontend/                  # Application React
│   ├── src/
│   │   ├── pages/            # Pages de l'application
│   │   ├── components/       # Composants réutilisables
│   │   └── services/         # API Client
└── data/                     # Données partagées
    ├── interpretations_json/ # Interprétations astrologiques
    └── Prompt_art_json/      # 🎨 Données artistiques pour IA
```

## 🔄 Flux de Génération de Prompts

1. **Calcul Astrologique** → `astro_calcule.py` → `theme.json`
2. **Génération Prompt** → `PromptGenerationService` → `prompt_final.txt`
3. **API REST** → `/api/generer-prompt` → Résultat JSON

## 🎨 Styles Poétiques Disponibles

- **Lumière des Anciens** (Raphaël, Blake, da Vinci)
- **Brume romantique divine** (Turner, Friedrich, Monet)
- **Mystères Symboliques** (Moreau, Redon, Böcklin)
- **Rêve éveillé** (Dali, Chagall, Ernst)
- **Fusion des astres** (Kandinsky, Klee, af Klint)
