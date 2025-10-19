"""
Test simple de l'API AstroSource Pro
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import de notre configuration
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import status, prompt_generation

# Configuration du logging
setup_logging()

# Création de l'application
app = FastAPI(
    title="AstroSource Pro API - Test",
    description="Version de test de l'API professionnelle",
    version="2.0.0-test",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Point d'entrée racine"""
    return {
        "message": "🌟 AstroSource Pro API - Version Test",
        "version": "2.0.0-test",
        "status": "operational",
    }


@app.get("/api/status")
async def get_status():
    """Status de l'API"""
    return {
        "status": "operational",
        "message": "API AstroSource Pro fonctionnelle",
        "config": {
            "data_dir": str(settings.DATA_DIR),
            "interpretations_dir": str(settings.INTERPRETATIONS_DIR),
            "data_exists": settings.DATA_DIR.exists(),
            "interpretations_exist": settings.INTERPRETATIONS_DIR.exists(),
        },
    }


# Ajout des routes de test
app.include_router(status.router, prefix="/api", tags=["Status"])
app.include_router(prompt_generation.router, prefix="/api", tags=["Prompts IA"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    print(f"🚀 Lancement du test AstroSource Pro sur http://localhost:{port}")
    uvicorn.run(
        "test_api_pro:app",
        host="localhost",
        port=port,
        reload=False,  # Pas de reload pour éviter les conflits
    )
