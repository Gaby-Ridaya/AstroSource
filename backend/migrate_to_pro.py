#!/usr/bin/env python3
"""
Script de migration pour reorganiser l'architecture AstroSource
Déplace les anciens fichiers vers la nouvelle structure professionnelle
"""

import shutil
import os
from pathlib import Path


def migrate_fusion_complete():
    """Migre le fichier fusion_complte.py vers l'ancienne structure"""

    backend_dir = Path(__file__).parent
    old_file = backend_dir / "fusion_complte.py"
    scripts_dir = backend_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    if old_file.exists():
        # Déplacer vers scripts/ comme référence legacy
        new_location = scripts_dir / "fusion_complte_legacy.py"
        shutil.move(str(old_file), str(new_location))
        print(f"✅ Migré: {old_file} → {new_location}")

        # Créer un fichier de référence
        with open(backend_dir / "MIGRATION_NOTES.md", "w") as f:
            f.write(
                """# Notes de Migration AstroSource

## Architecture Professionnelle

### Ancien système:
- `fusion_complte.py` - Génération de prompts (ROOT)
- `astro_calcule.py` - Calculs astrologiques (ROOT)
- `nouvelle_roue.py` - Génération SVG (ROOT)

### Nouvelle structure:
- `app/services/prompt_generation.py` - Service de génération de prompts
- `app/services/astro_generation.py` - Service de génération SVG
- `app/services/interpretation.py` - Service d'interprétations
- `app/api/routes/prompt_generation.py` - API de génération de prompts

### Fonctionnalités migrées:
✅ Génération de prompts artistiques IA
✅ Styles poétiques configurables
✅ Fusion données astrologiques + art
✅ API RESTful professionnelle

### Fichiers legacy:
- `scripts/fusion_complte_legacy.py` - Ancienne version pour référence
"""
            )
        print("✅ Notes de migration créées")
    else:
        print("ℹ️  Fichier fusion_complte.py déjà migré ou inexistant")


def create_architecture_diagram():
    """Crée un diagramme de l'architecture"""

    diagram = """
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
"""

    with open(Path(__file__).parent / "ARCHITECTURE.md", "w") as f:
        f.write(diagram)

    print("✅ Diagramme d'architecture créé")


if __name__ == "__main__":
    print("🚀 Migration AstroSource vers architecture professionnelle")
    print("=" * 60)

    migrate_fusion_complete()
    create_architecture_diagram()

    print("\n✅ Migration terminée !")
    print("\n📋 Prochaines étapes:")
    print("1. Tester l'API: curl http://localhost:8003/api/styles-poetiques")
    print("2. Générer un prompt: POST /api/generer-prompt")
    print("3. Consulter: ARCHITECTURE.md pour la documentation")
