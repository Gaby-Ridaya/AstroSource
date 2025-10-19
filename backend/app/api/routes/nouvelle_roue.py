"""
Module de routage pour la génération de roues astrales SVG
Gère la génération des thèmes astraux en format SVG
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import logging

# Import du service de génération
from app.services.astro_generation import astro_service

logger = logging.getLogger(__name__)

router = APIRouter()


class ThemeRequest(BaseModel):
    """Modèle de données pour la requête de génération de thème"""

    nom: str
    ville_naissance: str
    date_naissance: str  # Format: DD/MM/YYYY
    heure_naissance: str  # Format: HH:MM


from fastapi import Response
from app.services.astro_calcule import generate_theme
import os


@router.post("/generer-svg")
async def generer_svg(request: ThemeRequest):
    """
    Génère un thème astral SVG et retourne le contenu SVG brut
    """
    try:
        nom = request.nom
        ville = request.ville_naissance
        date = request.date_naissance
        heure = request.heure_naissance
        pays = getattr(request, "pays", None)
        export_path = generate_theme(nom, date, heure, ville, pays)
        if not export_path:
            return Response(
                content="Erreur lors de la génération du thème.", status_code=500
            )
        svg_path = os.path.splitext(export_path)[0] + ".svg"
        if not os.path.exists(svg_path):
            return Response(content="SVG non généré.", status_code=500)
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        return Response(content=svg_content, media_type="image/svg+xml")
    except Exception as e:
        logger.error(f"❌ Erreur inattendue lors de la génération SVG: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")


@router.get("/files")
async def list_generated_files():
    """
    Liste tous les fichiers générés pour chaque utilisateur (JSON, SVG, prompts, images)
    """
    try:
        data_dir = Path(__file__).parent.parent.parent.parent / "data" / "Utilisateurs"
        if not data_dir.exists():
            logger.warning(f"⚠️ Dossier Utilisateurs non trouvé: {data_dir}")
            return {"files": [], "message": "Aucun utilisateur ou fichier généré"}

        all_files = []
        for user_dir in data_dir.iterdir():
            if user_dir.is_dir():
                user_files = []
                for file_path in user_dir.glob("*"):
                    if file_path.is_file():
                        user_files.append(
                            {
                                "user": user_dir.name,
                                "name": file_path.name,
                                "path": str(file_path),
                                "size": file_path.stat().st_size,
                                "created": file_path.stat().st_ctime,
                            }
                        )
                # Tri par date de création (plus récent en premier)
                user_files.sort(key=lambda x: x["created"], reverse=True)
                all_files.extend(user_files)

        # Tri global par date de création
        all_files.sort(key=lambda x: x["created"], reverse=True)

        logger.info(f"✅ {len(all_files)} fichiers trouvés pour tous les utilisateurs")
        return {"status": "success", "files": all_files, "total": len(all_files)}

    except Exception as e:
        logger.error(f"❌ Erreur lors de la liste des fichiers: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de listage: {str(e)}")
