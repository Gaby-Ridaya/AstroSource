"""
Module de routage pour l'étude astrologique
Gère les interprétations des planètes, maisons et aspects
"""

from fastapi import APIRouter, HTTPException
import logging

# Import du service d'interprétations
from app.services.interpretation import interpretation_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/interpretations/planets")
async def get_planet_interpretations():
    """
    Retourne toutes les interprétations des planètes
    """
    try:
        interpretations = await interpretation_service.get_planet_interpretations()

        if not interpretations:
            raise HTTPException(
                status_code=404, detail="Aucune interprétation de planète trouvée"
            )

        logger.info(f"✅ {len(interpretations)} interprétations de planètes retournées")
        return interpretations

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du chargement des interprétations: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de chargement: {str(e)}")


@router.get("/interpretations/houses")
async def get_house_interpretations():
    """
    Retourne toutes les interprétations des maisons
    """
    try:
        interpretations = await interpretation_service.get_house_interpretations()

        if not interpretations:
            raise HTTPException(
                status_code=404, detail="Aucune interprétation de maison trouvée"
            )

        logger.info(f"✅ {len(interpretations)} interprétations de maisons retournées")
        return interpretations

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du chargement des interprétations: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de chargement: {str(e)}")


@router.get("/interpretations/aspects")
async def get_aspect_interpretations():
    """
    Retourne toutes les interprétations des aspects
    """
    try:
        interpretations = await interpretation_service.get_aspect_interpretations()

        if not interpretations:
            logger.warning("Aucune interprétation d'aspect trouvée")
            return {"message": "Interprétations des aspects non disponibles"}

        logger.info(f"✅ {len(interpretations)} interprétations d'aspects retournées")
        return interpretations

    except Exception as e:
        logger.error(f"Erreur lors du chargement des interprétations: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de chargement: {str(e)}")


@router.get("/interpretations/signs")
async def get_sign_interpretations():
    """
    Retourne toutes les interprétations des signes
    """
    try:
        interpretations = await interpretation_service.get_sign_interpretations()

        if not interpretations:
            logger.warning("Aucune interprétation de signe trouvée")
            return {"message": "Interprétations des signes non disponibles"}

        logger.info(f"✅ {len(interpretations)} interprétations de signes retournées")
        return interpretations

    except Exception as e:
        logger.error(f"Erreur lors du chargement des interprétations: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de chargement: {str(e)}")


@router.get("/celebrities")
async def get_celebrities():
    """
    Retourne la liste des célébrités disponibles pour l'étude
    """
    try:
        celebrities = await interpretation_service.get_celebrities()

        logger.info(f"✅ {len(celebrities)} célébrités retournées")
        return celebrities

    except Exception as e:
        logger.error(f"Erreur lors du chargement des célébrités: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de chargement: {str(e)}")


@router.get("/interpretations/summary")
async def get_interpretation_summary():
    """
    Retourne un résumé des interprétations disponibles
    """
    try:
        summary = await interpretation_service.get_interpretation_summary()

        logger.info("✅ Résumé des interprétations généré")
        return {"status": "success", "summary": summary, "total": sum(summary.values())}

    except Exception as e:
        logger.error(f"Erreur lors de la génération du résumé: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de résumé: {str(e)}")
