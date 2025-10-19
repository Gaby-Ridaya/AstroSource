# 📦 Fichiers Dépréciés

Ce dossier contient les anciens points d'entrée archivés pour référence historique.

## 📋 Historique des versions

### `main_legacy_v1.py` (Anciennement `main.py`)

- **Version** : 1.0.0
- **Architecture** : Monolithique
- **Caractéristiques** :
  - Imports directs (`astro_calcule`, `nouvelle_roue`)
  - Structure simple mais non modulaire
  - Fonctionnelle mais non scalable

### `main_experimental_v2.py` (Anciennement `main_new.py`)

- **Version** : 2.1.0
- **Architecture** : Moderne avec lifespan events
- **Caractéristiques** :
  - Utilise les nouveaux gestionnaires de cycle de vie FastAPI
  - Architecture expérimentale
  - Non testée en production

## 🎯 Version Actuelle

**`../main.py`** (Anciennement `main_pro.py`)

- **Version** : 2.0.0 Pro
- **Architecture** : Modulaire professionnelle
- **Statut** : ✅ Production
- **Caractéristiques** :
  - Services dans `app/services/`
  - Routes dans `app/api/routes/`
  - Configuration avec Pydantic
  - Logging professionnel
  - Tests intégrés

## ⚠️ Important

Ces fichiers sont conservés uniquement pour référence historique.
**N'utilisez que `../main.py`** pour le développement et la production.
