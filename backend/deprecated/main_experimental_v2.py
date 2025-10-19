"""
AstroSource Pro - Backend API
Générateur de thèmes astraux avancé avec IA

Point d'entrée principal de l'application FastAPI
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import API_HOST, API_PORT, API_DEBUG, CORS_ORIGINS, validate_paths
from app.core.logging import logger
from app.api.etude_astro import router as etude_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de cycle de vie de l'application"""
    # Startup
    logger.info("🚀 Démarrage d'AstroSource Backend...")

    try:
        validate_paths()
        logger.info("✅ Validation des chemins réussie")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la validation: {e}")
        raise

    logger.info("✅ AstroSource Backend démarré avec succès!")

    yield

    # Shutdown
    logger.info("🛑 Arrêt d'AstroSource Backend...")


# Application FastAPI
app = FastAPI(
    title="AstroSource Pro API",
    description="API avancée pour la génération de thèmes astraux avec IA",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(etude_router, prefix="/api", tags=["Étude Astrologique"])

# Import des anciens endpoints (transition)
# TODO: Migrer ces endpoints vers des routers séparés
from astro_calcule import generate_theme
from websocket_manager import websocket_manager
import json
import time
from datetime import datetime


@app.get("/api/status")
async def get_status():
    """Endpoint de santé de l'API"""
    return JSONResponse(
        {
            "status": "healthy",
            "service": "AstroSource Pro API",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.post("/api/generer-svg")
async def generer_svg(data: dict):
    """
    Génère un thème astral SVG

    TODO: Migrer vers un router dédié avec validation Pydantic
    """
    logger.info(f"Génération SVG demandée pour: {data.get('nom', 'N/A')}")

    try:
        result = await generate_theme(data)
        logger.info("✅ SVG généré avec succès")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur génération SVG: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files")
async def list_files():
    """
    Liste les fichiers générés

    TODO: Migrer vers un router dédié
    """
    try:
        # Implementation temporaire
        return {"files": []}
    except Exception as e:
        logger.error(f"❌ Erreur listage fichiers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info(f"🌟 Lancement d'AstroSource Pro sur {API_HOST}:{API_PORT}")

    uvicorn.run(
        "main:app", host=API_HOST, port=API_PORT, reload=API_DEBUG, log_level="info"
    )
