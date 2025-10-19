from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import glob

router = APIRouter()


@router.get("/galerie-categories")
def get_galerie_categories():
    import logging

    logger = logging.getLogger("galerie_categories")
    # Correction du chemin pour servir les images
    from app.core.config import settings

    base_dir = str(settings.DATA_DIR / "images")
    logger.info(f"Chemin utilisé pour les images: {base_dir}")
    if not os.path.exists(base_dir):
        logger.error(f"Dossier images introuvable: {base_dir}")
        return JSONResponse(content={"galerie": {}})
    # Liste tous les sous-dossiers (catégories)
    galerie = {}
    for entry in os.scandir(base_dir):
        if entry.is_dir():
            cat_name = entry.name
            img_list = []
            img_list += [
                os.path.basename(f)
                for f in glob.glob(os.path.join(entry.path, "*.png"))
            ]
            img_list += [
                os.path.basename(f)
                for f in glob.glob(os.path.join(entry.path, "*.jpg"))
            ]
            galerie[cat_name] = img_list
    logger.info(f"Catégories trouvées: {galerie}")
    return JSONResponse(content={"galerie": galerie})
