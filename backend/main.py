"""
AstroSource Pro - Point d'entrée principal de l'API
================================================

API FastAPI professionnelle pour la génération de thèmes astraux
et l'interprétation astrologique avec architecture modulaire.

Auteur: Gabriel
Version: 2.0.0
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import logging
import uvicorn
import os
from pathlib import Path
from app.api.routes import generation_image

# Import de nos modules personnalisés
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import status, etude_astro, nouvelle_roue, prompt_generation
from app.api.routes.downloads import router as downloads_router
from app.api.routes import galerie_categories

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
setup_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Factory pour créer l'application FastAPI avec toute la configuration
    """
    # Initialisation de l'application
    app = FastAPI(
        title="AstroSource Pro API",
        description="API professionnelle pour la génération de thèmes astraux et l'interprétation astrologique",
        version="2.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )

    # Configuration CORS (doit être AVANT l'inclusion des routes)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,  # si tu utilises des cookies/sessions
        allow_methods=["*"],  # GET, POST, OPTIONS, etc.
        allow_headers=["*"],  # Content-Type, Authorization, etc.
    )

    # Middleware de sécurité pour les hosts de confiance
    if not settings.DEBUG:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

    # Configuration des fichiers statiques
    static_path = Path(settings.DATA_DIR) / "images"
    if static_path.exists():
        app.mount(
            "/images",
            StaticFiles(directory="/home/gaby/AstroSource/data/images"),
            name="images",
        )

    # Gestionnaire d'erreurs global
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Erreur non gérée: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Erreur interne du serveur",
                "detail": (
                    str(exc)
                    if settings.DEBUG
                    else "Une erreur inattendue s'est produite"
                ),
            },
        )

    # Enregistrement des routes
    app.include_router(
        generation_image.router, prefix="/api", tags=["Génération Images IA"]
    )
    app.include_router(status.router, prefix="/api", tags=["Status"])
    app.include_router(etude_astro.router, prefix="/api", tags=["Étude Astro"])
    app.include_router(nouvelle_roue.router, prefix="/api", tags=["Génération SVG"])
    app.include_router(
        prompt_generation.router, prefix="/api", tags=["Génération Prompts IA"]
    )

    app.include_router(galerie_categories.router, prefix="/api", tags=["Galerie"])
    app.include_router(downloads_router)

    # Event handlers
    @app.on_event("startup")
    async def startup_event():
        """Actions à effectuer au démarrage de l'application"""
        logger.info("🚀 Démarrage d'AstroSource Pro API")
        logger.info(f"📊 Mode debug: {settings.DEBUG}")
        logger.info(f"📁 Répertoire de données: {settings.DATA_DIR}")
        logger.info(f"🌐 Hosts autorisés: {settings.ALLOWED_HOSTS}")

        # Validation des chemins
        settings.validate_paths()
        logger.info("✅ Validation des chemins terminée")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Actions à effectuer à l'arrêt de l'application"""
        logger.info("🛑 Arrêt d'AstroSource Pro API")

    return app


# Création de l'instance de l'application
app = create_app()

if __name__ == "__main__":
    logger.info(f"🌟 Lancement d'AstroSource Pro sur {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )
