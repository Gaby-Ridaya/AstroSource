# 🌟 AstroSource Pro - Backend API

API FastAPI professionnelle pour la génération de thèmes astraux et l'interprétation astrologique.

## 🚀 Architecture

```
backend/
├── app/                    # Application principale
│   ├── api/               # Routes et endpoints
│   │   └── routes/        # Modules de routage
│   ├── core/              # Configuration et utilitaires core
│   ├── services/          # Logique métier
│   └── models/            # Modèles de données (futur)
├── scripts/               # Scripts d'administration
├── tests/                 # Tests automatisés
└── temp/                  # Fichiers temporaires
```

## 📋 Fonctionnalités

### 🎯 API Endpoints

- **Status** : `/api/status` - Statut de l'API
- **Génération SVG** : `/api/generer-svg` - Génération de thèmes astraux
- **Interprétations** :
  - `/api/interpretations/planets` - Interprétations des planètes
  - `/api/interpretations/houses` - Interprétations des maisons
  - `/api/interpretations/aspects` - Interprétations des aspects
  - `/api/interpretations/signs` - Interprétations des signes
- **Célébrités** : `/api/celebrities` - Liste des célébrités pour études
- **Fichiers** : `/api/files` - Liste des fichiers générés

### 🛠️ Services

- **AstroGenerationService** : Génération de thèmes astraux SVG
- **InterpretationService** : Gestion des interprétations astrologiques

## 🔧 Installation

### Prérequis

- Python 3.11+
- Environnement virtuel activé (`Boogy`)

### Configuration

1. **Copier le fichier de configuration** :

   ```bash
   cp .env.example .env
   ```

2. **Modifier les variables d'environnement** :

   ```bash
   nano .env
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Démarrage

### Mode Development

```bash
# Avec le main professionnel
python main_pro.py

# Ou avec uvicorn directement
uvicorn main_pro:app --reload --host localhost --port 8000
```

### Mode Production

```bash
uvicorn main_pro:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Configuration

### Variables d'environnement

| Variable     | Description       | Défaut      |
| ------------ | ----------------- | ----------- |
| `API_HOST`   | Host de l'API     | `localhost` |
| `API_PORT`   | Port de l'API     | `8000`      |
| `API_DEBUG`  | Mode debug        | `True`      |
| `LOG_LEVEL`  | Niveau de logging | `INFO`      |
| `SECRET_KEY` | Clé secrète       | À définir   |

### Logging

- **Rotation automatique** des logs
- **Niveaux configurables** (DEBUG, INFO, WARNING, ERROR)
- **Formatage professionnel** avec timestamps et contexte

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/

# Tests avec couverture
pytest tests/ --cov=app --cov-report=html

# Tests d'un module spécifique
pytest tests/test_api/
```

## 📈 Monitoring

### Endpoints de santé

- **Status** : `GET /api/status` - Statut général de l'API
- **Métriques** : Logs détaillés avec rotation

### Performance

- **Cache LRU** pour les interprétations
- **Gestion d'erreurs** robuste
- **Logging structuré** pour le monitoring

## 🔒 Sécurité

- **CORS** configuré pour le frontend
- **TrustedHost** middleware en production
- **Gestion d'erreurs** sécurisée (pas de stack traces en prod)
- **Variables d'environnement** pour les secrets

## 📦 Dépendances principales

### Core

- **FastAPI** : Framework web moderne
- **Uvicorn** : Serveur ASGI performant
- **Pydantic** : Validation de données

### Astrologie

- **Kerykeion** : Calculs astrologiques
- **Pyephem** : Calculs astronomiques
- **Timezonefinder** : Gestion des fuseaux horaires

### Utilitaires

- **Requests** : Client HTTP
- **Pillow** : Traitement d'images
- **python-multipart** : Upload de fichiers

## 🛠️ Développement

### Structure des modules

```python
# Route typique
from fastapi import APIRouter
from app.services.interpretation import interpretation_service

router = APIRouter()

@router.get("/endpoint")
async def endpoint_handler():
    return await interpretation_service.method()
```

### Bonnes pratiques

- **Services** pour la logique métier
- **Modèles Pydantic** pour la validation
- **Logging** systématique
- **Gestion d'erreurs** avec HTTPException
- **Documentation** automatique avec FastAPI

## 📚 Documentation

- **API Docs** : `http://localhost:8000/docs` (mode debug)
- **ReDoc** : `http://localhost:8000/redoc` (mode debug)
- **OpenAPI** : `http://localhost:8000/openapi.json`

## 🤝 Contribution

1. Créer une branche feature
2. Ajouter des tests pour les nouvelles fonctionnalités
3. S'assurer que tous les tests passent
4. Documenter les changements
5. Créer une pull request

## 📝 Changelog

### Version 2.0.0

- ✅ Architecture modulaire avec services
- ✅ Configuration professionnelle avec environnement
- ✅ Logging avec rotation
- ✅ Structure de projet standardisée
- ✅ Documentation complète

### Version 1.0.0

- ✅ API de base fonctionnelle
- ✅ Génération SVG
- ✅ Interprétations astrologiques

## 📞 Support

Pour toute question ou problème :

- Consulter la documentation API : `/docs`
- Vérifier les logs : `logs/astrosource.log`
- Tester les endpoints : `/api/status`

---

**AstroSource Pro** - Une application astrologique moderne et professionnelle 🌟
