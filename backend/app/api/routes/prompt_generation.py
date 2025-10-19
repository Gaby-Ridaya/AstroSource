"""
Module de routage pour la génération de prompts artistiques IA
Gère la création de prompts basés sur les thèmes astrologiques
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import logging
from typing import Optional

# Import du service de génération de prompts
from app.services.prompt_generation import prompt_generation_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class PromptRequest(BaseModel):
    """Modèle de données pour la requête de génération de prompt"""

    theme_file: str  # Chemin vers le fichier theme JSON
    style_poetique: Optional[str] = None  # Style poétique à appliquer
    output_name: Optional[str] = None  # Nom du fichier de sortie (optionnel)


@router.post("/generer-prompt")
async def generer_prompt_artistique(request: PromptRequest):
    """
    Génère un prompt artistique pour l'IA basé sur un thème astrologique
    """
    try:
        logger.info(f"🎨 Demande de génération de prompt pour: {request.theme_file}")
        logger.info(f"📁 DATA_DIR configuré: {settings.DATA_DIR}")

        # Validation du fichier thème
        theme_path = Path(request.theme_file)
        if not theme_path.is_absolute():
            # Utilisation de la configuration pour trouver le bon chemin
            theme_path = settings.DATA_DIR / request.theme_file

        logger.info(f"🔍 Chemin final du thème: {theme_path}")
        logger.info(f"📂 Fichier existe: {theme_path.exists()}")

        if not theme_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Fichier thème non trouvé: {theme_path}"
            )

        # Définition du chemin de sortie
        if request.output_name:
            output_path = theme_path.parent / request.output_name
        else:
            output_path = theme_path.parent / "prompt_final.txt"

        # Génération du prompt
        resultat = await prompt_generation_service.generate_artistic_prompt(
            theme_path=str(theme_path),
            output_path=str(output_path),
            style_poetique_choisi=request.style_poetique,
        )

        logger.info(f"✅ Prompt généré avec succès: {output_path}")

        return {
            "status": "success",
            "message": f"Prompt artistique généré avec succès",
            "data": resultat,
            "output_file": str(output_path),
        }

    except FileNotFoundError as e:
        logger.error(f"❌ Fichier non trouvé: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        logger.error(f"❌ Erreur de génération: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Erreur inattendue lors de la génération de prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")


@router.get("/styles-poetiques")
async def get_styles_poetiques():
    """
    Retourne la liste des styles poétiques disponibles
    """
    try:
        styles = prompt_generation_service.STYLE_POETIQUE

        logger.info(f"✅ {len(styles)} styles poétiques disponibles")

        return {"status": "success", "styles": styles, "count": len(styles)}

    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des styles: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de récupération: {str(e)}")


@router.get("/prompt-data-summary")
async def get_prompt_data_summary():
    """
    Retourne un résumé des données de prompts disponibles
    """
    try:
        # Chargement des données pour obtenir le résumé
        prompt_data = prompt_generation_service._load_prompt_data()

        summary = {}
        for key, data in prompt_data.items():
            if isinstance(data, dict):
                summary[key] = len(data)
            elif isinstance(data, list):
                summary[key] = len(data)
            else:
                summary[key] = 1

        logger.info(f"✅ Résumé des données de prompts généré")

        return {
            "status": "success",
            "summary": summary,
            "total_files": len(prompt_data),
            "prompt_art_dir": str(prompt_generation_service.prompt_art_dir),
        }

    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération du résumé: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de résumé: {str(e)}")
