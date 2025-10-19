# 📋 Documentation Technique AstroSource

## 🔧 Architecture détaillée

### Backend (FastAPI + Python 3.11)

#### Modules principaux

##### `backend/main.py` - Point d'entrée API
- **FastAPI** : Serveur web moderne avec documentation automatique
- **CORS** : Configuration pour développement React
- **Routes** : Organisation modulaire des endpoints
- **Middleware** : Gestion des erreurs et logging

##### `backend/astro_calcule.py` - Moteur astrologique
- **Flatlib** : Calculs de positions planétaires précis
- **Géolocalisation** : API GeoNames pour coordonnées des villes
- **Fuseaux horaires** : Gestion automatique UTC/local
- **Aspects** : Calcul des relations planétaires (conjonction, trigone, carré...)
- **Maisons** : Système Placidus pour les secteurs astrologiques

```python
# Exemple d'utilisation
theme = generate_theme(
    nom="Caroline",
    date="1985-03-15", 
    heure="14:30",
    ville="Paris",
    pays="FR"
)
```

##### `backend/nouvelle_roue.py` - Générateur SVG optimisé
- **SVGWrite** : Création de graphiques vectoriels
- **Optimisation des conjonctions** : Algorithme d'espacement intelligent
- **Thèmes personnalisables** : JSON de configuration visuelle
- **Couches multiples** : Zodiac, planètes, aspects, maisons

**🌟 Innovation : Algorithme d'optimisation des conjonctions**
```python
def detecter_conjonctions(self, planetes, orbe=4.0):
    """Détecte automatiquement les groupes de planètes proches"""
    # Algorithme optimisé pour éviter les chevauchements visuels
    
def calculer_ajustements_positions(self, planetes, min_separation=4.0):
    """Calcule l'espacement optimal selon le nombre de planètes"""
    # 2 planètes : ±2.4°
    # 3 planètes : -3.6°, 0°, +3.6° 
    # 4+ planètes : espacement logarithmique
```

##### `backend/fusion_complte.py` - Fusion des prompts artistiques
- **Combinaison intelligente** : Merge des données astrologiques + styles
- **Templates JSON** : Prompts modulaires et réutilisables
- **Variables dynamiques** : Insertion automatique des données calculées
- **Optimisation IA** : Prompts adaptés pour DALL·E 3

##### `backend/utils/openai_image.py` - Interface OpenAI
- **DALL·E 3** : Génération d'images HD (1024x1024)
- **GPT-4** : Résumés créatifs et interprétations poétiques
- **Gestion d'erreurs** : Retry automatique et fallback
- **Optimisation des coûts** : Cache des requêtes similaires

#### Flux de données

```
1. Formulaire → [Validation] → astro_calcule.py
2. Calculs → [JSON Theme] → nouvelle_roue.py  
3. SVG + JSON → [Fusion] → fusion_complte.py
4. Prompt → [OpenAI] → Image + Interprétation
5. Fichiers → [API] → Frontend
```

### Frontend (React 19 + Vite)

#### Structure des composants

```
src/
├── App.jsx                 # Routeur principal
├── components/
│   ├── FormAstro.jsx       # Formulaire de saisie
│   ├── ResultDisplay.jsx   # Affichage des résultats
│   └── DownloadButton.jsx  # Boutons de téléchargement
├── hooks/
│   └── useAstroAPI.js      # Hook personnalisé pour l'API
└── styles/
    └── App.css             # Styles globaux
```

#### Technologies utilisées
- **React 19** : Framework UI moderne avec Server Components
- **Vite** : Build tool ultra-rapide avec HMR
- **React Router** : Navigation SPA
- **Fetch API** : Communication avec le backend

### Base de données et stockage

#### Structure des fichiers utilisateur
```
data/Utilisateurs/{nom}/
├── theme_{id}.json         # Données astrologiques complètes
├── theme_{id}.svg          # Carte du ciel vectorielle
├── theme_{id}_openai.png   # Image artistique IA
├── prompt_final.txt        # Prompt artistique utilisé
├── prompt_interpretation.txt # Prompt d'interprétation
└── interpretation_ia.txt   # Interprétation générée
```

#### Format JSON du thème astrologique
```json
{
  "utilisateur": {
    "nom": "Caroline",
    "date_naissance": "1985-03-15",
    "heure_naissance": "14:30",
    "lieu": {"ville": "Paris", "pays": "FR"}
  },
  "planetes": {
    "Sun": 354.28,    # Position en degrés absolus
    "Moon": 123.45,
    "Mercury": 12.67,
    # ... toutes les planètes
  },
  "maisons_deg": [325.36, 20.92, ...], # 12 cuspides
  "aspects": [
    {
      "planetes": "Sun - Moon",
      "aspect": "☌",           # Symbole Unicode
      "orb": 2.34,            # Orbe en degrés
      "energie": "harmonique"
    }
  ],
  "ascendant": 325.36,
  "mc": 234.12,
  "theme": {
    # Configuration visuelle SVG
    "background": "#181824",
    "planet_colors": {...},
    "aspect_colors": {...}
  }
}
```

## 🎨 Système de prompts artistiques

### Architecture modulaire JSON

Chaque style artistique est défini dans un fichier JSON structuré :

```json
{
  "style_name": "Mystique 4K",
  "description": "Atmosphère mystérieuse et spirituelle",
  "base_prompt": "Cosmic mandala in deep space...",
  "prompts": {
    "planetes": {
      "Sun": "Golden solar disc radiating divine light",
      "Moon": "Silver crescent reflecting ethereal glow"
    },
    "signes": {
      "Aries": "Ram constellation in fiery nebula",
      "Taurus": "Bull silhouette in emerald cosmic dust"
    },
    "aspects": {
      "conjonction": "Planets merging in brilliant fusion",
      "trigone": "Harmonious triangle of celestial energy"
    }
  },
  "palette_couleurs": ["#1a0033", "#4a0e4e", "#6a1b9a"],
  "techniques": ["digital art", "HDR", "cosmic realism"],
  "resolution": "4K UHD",
  "style_modifiers": ["mystical", "ethereal", "luminous"]
}
```

### Fusion intelligente

Le système combine automatiquement :
1. **Données astrologiques** : Positions réelles des planètes
2. **Prompts spécifiques** : Descriptions par planète/signe/aspect  
3. **Style artistique** : Palette, techniques, ambiance
4. **Optimisation DALL·E** : Résumé créatif sous 400 caractères

## 🔬 Algorithmes et calculs

### Calculs astrologiques

#### Positions planétaires (Swiss Ephemeris)
```python
# Conversion coordonnées géocentriques → topocentriques
def geocentric_to_topocentric(planet_pos, observer_lat, observer_lon):
    # Correction de parallaxe pour Lune et planètes proches
    # Précision : 0.01 seconde d'arc
```

#### Système de maisons Placidus
```python
def calculate_houses_placidus(jd_ut, lat, lon):
    # Calcul des 12 cuspides de maisons
    # Gestion des hautes latitudes (>66°)
    # Fallback sur système Equal House si nécessaire
```

#### Calcul des aspects
```python
ORBES_MAJEURS = {
    'conjonction': 8.0,   # ± 8°
    'opposition': 8.0,    # ± 8°  
    'trigone': 6.0,       # ± 6°
    'carre': 6.0,         # ± 6°
    'sextile': 4.0        # ± 4°
}

def calculate_aspects(planets_dict):
    # Parcours toutes les combinaisons de planètes
    # Calcul de l'angle entre deux positions
    # Application des orbes selon l'aspect
    # Tri par force (orbe le plus serré en premier)
```

### Optimisation visuelle SVG

#### Algorithme d'espacement des conjonctions

```python
def optimize_conjunctions(planets, min_separation=4.0):
    """
    Optimise l'espacement visuel des planètes en conjonction
    
    Entrée : Dict des positions planétaires en degrés
    Sortie : Dict avec positions ajustées pour l'affichage
    
    Algorithme :
    1. Détecter les groupes (orbe ≤ 4°)
    2. Calculer l'espacement optimal selon la taille du groupe
    3. Appliquer les décalages en préservant l'ordre zodiacal
    4. Vérifier les chevauchements avec d'autres groupes
    """
    
    # Groupes de 2 : ±2.4°
    # Groupes de 3 : -3.6°, 0°, +3.6°  
    # Groupes de 4 : -4.8°, -1.6°, +1.6°, +4.8°
    # Groupes de 5+ : répartition logarithmique
```

#### Rendu SVG optimisé

```python
class AstroChartSVG:
    def __init__(self, size=(1800, 1200)):
        # Canvas 1800x1200 pour qualité impression
        # Ratio 3:2 optimal pour affichage/print
        
    def draw_layered_chart(self):
        # Ordre des couches (z-index) :
        # 1. Fond et cercles décoratifs
        # 2. Graduation et secteurs de maisons  
        # 3. Signes zodiacaux
        # 4. Aspects (en arrière-plan)
        # 5. Planètes et angles (premier plan)
        # 6. Textes et légendes
```

## 🚀 Performance et optimisations

### Cache et mémoire

#### Cache des calculs astrologiques
```python
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=1000)
def cached_planetary_positions(jd_ut, location_hash):
    """Cache les positions planétaires pour éviter les recalculs"""
    # Validité : 1 heure (positions changent lentement)
    # Clé : Julian Day + hash(lat,lon)
```

#### Optimisation des requêtes OpenAI
```python
class OpenAICache:
    def __init__(self, ttl=3600):  # 1 heure
        self.cache = {}
        
    def get_cached_image(self, prompt_hash):
        """Évite les générations d'images identiques"""
        # Hash du prompt + style
        # Économie : ~0.04$ par image évitée
```

### Optimisations frontend

#### Code splitting et lazy loading
```javascript
// Chargement différé des composants lourds
const ResultDisplay = lazy(() => import('./components/ResultDisplay'));
const SVGViewer = lazy(() => import('./components/SVGViewer'));

// Bundle analysis : 
// - Chunk principal : ~150KB
// - Chunk résultats : ~80KB  
// - Chunk SVG : ~45KB
```

#### Optimisation des images
```javascript
// Compression automatique des images DALL·E
const optimizeImage = async (imageUrl) => {
    // WebP si supporté, sinon JPEG 90%
    // Responsive images : 1024px, 512px, 256px
    // Lazy loading avec intersection observer
};
```

## 🔒 Sécurité et validation

### Validation des entrées

#### Côté frontend (React)
```javascript
const astroSchema = {
    nom: /^[a-zA-ZÀ-ÿ\s-]{2,50}$/,           // Noms avec accents
    date: /^\d{4}-\d{2}-\d{2}$/,              // Format ISO
    heure: /^([01]\d|2[0-3]):[0-5]\d$/,       // Format 24h
    ville: /^[a-zA-ZÀ-ÿ\s-']{2,100}$/,       // Villes internationales
    pays: /^[A-Z]{2}$/                        // Code ISO pays
};
```

#### Côté backend (FastAPI)
```python
from pydantic import BaseModel, validator

class ThemeRequest(BaseModel):
    nom: str
    date: str  
    heure: str
    ville: str
    pays: str
    style: str
    
    @validator('date')
    def validate_date(cls, v):
        # Vérification date valide + âge réaliste (1900-2030)
        
    @validator('ville')  
    def validate_city(cls, v):
        # Vérification existence via GeoNames API
```

### Sécurité des fichiers

#### Isolation des données utilisateur
```python
import os
from pathlib import Path

class SecureFileManager:
    def __init__(self, base_dir="data/Utilisateurs"):
        self.base_dir = Path(base_dir).resolve()
        
    def get_user_dir(self, username):
        # Sanitisation du nom utilisateur
        clean_name = re.sub(r'[^\w\s-]', '', username)
        user_dir = self.base_dir / clean_name
        
        # Vérification path traversal
        if not str(user_dir).startswith(str(self.base_dir)):
            raise SecurityError("Invalid path")
            
        return user_dir
```

#### Protection des API keys
```python
import os
from cryptography.fernet import Fernet

class APIKeyManager:
    def __init__(self):
        # Chiffrement des clés sensibles en base
        self.cipher = Fernet(os.environ['ENCRYPTION_KEY'])
        
    def get_openai_key(self):
        # Déchiffrement à la volée
        encrypted_key = os.environ['OPENAI_API_KEY_ENCRYPTED']
        return self.cipher.decrypt(encrypted_key)
```

## 📊 Monitoring et logs

### Logging structuré

```python
import structlog
import sys

# Configuration des logs
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Utilisation
logger.info("theme_generated", 
           user=username, 
           generation_time=elapsed,
           style=style_name,
           file_size=svg_size)
```

### Métriques de performance

```python
from time import perf_counter
from contextlib import contextmanager

@contextmanager
def measure_time(operation_name):
    start = perf_counter()
    try:
        yield
    finally:
        duration = perf_counter() - start
        logger.info("performance_metric",
                   operation=operation_name,
                   duration_ms=duration * 1000)

# Utilisation
with measure_time("astrological_calculations"):
    theme = generate_theme(...)
    
with measure_time("svg_generation"):
    chart.make_svg()
    
with measure_time("openai_image_generation"):
    image_url = generate_image(prompt)
```

## 🧪 Tests et qualité

### Tests unitaires

```python
import pytest
from backend.astro_calcule import generate_theme

class TestAstrologicalCalculations:
    def test_known_planetary_positions(self):
        """Test avec des positions connues (éphémérides)"""
        theme = generate_theme(
            nom="Test",
            date="2000-01-01", 
            heure="12:00",
            ville="Greenwich",
            pays="GB"
        )
        
        # Soleil à ~280° en Capricorne le 1er janvier
        assert 279 <= theme['planetes']['Sun'] <= 281
        
    def test_conjunction_optimization(self):
        """Test de l'algorithme d'optimisation"""
        from backend.nouvelle_roue import AstroChartSVG
        
        # Planètes en conjonction serrée
        planets = {
            'Sun': 100.0,
            'Moon': 102.0,    # 2° d'écart
            'Mercury': 103.5  # 3.5° d'écart  
        }
        
        chart = AstroChartSVG("test.svg")
        optimized = chart.appliquer_optimisation_planetes(planets)
        
        # Vérifier l'espacement minimal
        positions = list(optimized.values())
        for i in range(len(positions)-1):
            assert abs(positions[i+1] - positions[i]) >= 4.0
```

### Tests d'intégration

```python
import requests
import tempfile
from pathlib import Path

class TestAPIIntegration:
    def test_complete_workflow(self):
        """Test du workflow complet via API"""
        
        # Requête de génération
        response = requests.post(
            "http://localhost:8000/api/generer-theme",
            json={
                "nom": "TestUser",
                "date": "1985-06-15",
                "heure": "09:30", 
                "ville": "Paris",
                "pays": "FR",
                "style": "mystique"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        
        # Vérifier que tous les fichiers sont générés
        files = data['files']
        for file_type in ['json', 'svg', 'image', 'prompt', 'interpretation']:
            assert file_type in files
            
            # Télécharger et vérifier le fichier
            file_response = requests.get(f"http://localhost:8000{files[file_type]}")
            assert file_response.status_code == 200
            assert len(file_response.content) > 0
```

### Tests de charge

```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

async def load_test_api():
    """Test de charge : 50 requêtes simultanées"""
    
    async def make_request(session, user_id):
        async with session.post(
            "http://localhost:8000/api/generer-theme",
            json={
                "nom": f"User{user_id}",
                "date": "1990-01-01",
                "heure": "12:00",
                "ville": "Paris", 
                "pays": "FR",
                "style": "mystique"
            }
        ) as response:
            return await response.json()
    
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, i) for i in range(50)]
        results = await asyncio.gather(*tasks)
        
    # Analyser les résultats
    success_count = sum(1 for r in results if r.get('success'))
    print(f"Succès : {success_count}/50")
    
    # Vérifier temps de réponse < 30s
    # Vérifier utilisation CPU < 90%
    # Vérifier utilisation RAM < 2GB
```

## 📈 Évolutions futures

### Architecture microservices

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Auth Service  │
│   (React)       │────│   (FastAPI)     │────│   (JWT)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌────────┼────────┐
                       │                 │
            ┌─────────────────┐    ┌─────────────────┐
            │ Astro Service   │    │   AI Service    │
            │ (Calculations)  │    │ (OpenAI/Local)  │
            └─────────────────┘    └─────────────────┘
                       │                 │
            ┌─────────────────┐    ┌─────────────────┐
            │   File Service  │    │   Cache Service │
            │   (MinIO/S3)    │    │   (Redis)       │
            └─────────────────┘    └─────────────────┘
```

### Intelligence artificielle avancée

#### Modèles personnalisés
```python
# Entraînement d'un modèle spécialisé en astrologie
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class AstroGPT:
    def __init__(self, model_path="./models/astro-gpt"):
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        
    def generate_interpretation(self, theme_data):
        # Génération d'interprétations plus précises
        # Corpus d'entraînement : 10k+ thèmes annotés
        # Spécialisation : aspects, transits, synastrie
```

#### Vision artificielle pour SVG
```python
# Analyse automatique de la qualité des graphiques
from PIL import Image
import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification

class SVGQualityAnalyzer:
    def analyze_chart_readability(self, svg_path):
        # Conversion SVG → PNG
        # Analyse : contraste, espacement, lisibilité
        # Score qualité : 0-100
        # Suggestions d'amélioration automatiques
```

---

*Documentation mise à jour : Août 2025*
*Version : 2.0*
*Auteur : Gaby - AstroSource Team*
