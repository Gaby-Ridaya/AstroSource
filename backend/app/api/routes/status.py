"""
Module de routage pour le status de l'API
"""

from fastapi import APIRouter
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/status")
async def get_status():
    """
    Retourne le statut de l'API avec informations système
    """
    logger.info("Vérification du statut de l'API")

    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "AstroSource Pro API est opérationnelle",
        "version": "2.0.0",
        "services": {
            "svg_generation": "active",
            "astro_calculations": "active",
            "interpretations": "active",
        },
    }
