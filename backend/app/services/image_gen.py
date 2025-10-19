# /home/gaby/AstroSource/backend/app/services/image_gen.py
import os, logging

logger = logging.getLogger(__name__)

def generate_astro_image(theme_json_path: str, output_path: str | None = None, **kwargs) -> str:
    """
    Point d'entrée unique pour générer une image astro.
    - theme_json_path: chemin du JSON de thème.
    - output_path: chemin de sortie souhaité (si supporté par le backend).
    Retourne le chemin du fichier image généré.
    """
    backend = os.getenv("IMAGE_BACKEND", "openai").lower()
    logger.info(f"[image_gen] Backend sélectionné: {backend}")

    if backend == "openai":
        # DALL·E 3 (ton implémentation actuelle)
        try:
            from app.services.temp.openai_image_gen import run_from_json
        except Exception as e:
            logger.error("[image_gen] Impossible d'importer openai_image_gen.run_from_json", exc_info=True)
            raise

        try:
            # Essai avec signature la plus complète
            return run_from_json(theme_json_path, output_path=output_path, **kwargs)
        except TypeError:
            # Compat rétro si la signature ne supporte pas output_path/kwargs
            return run_from_json(theme_json_path)

    elif backend == "sdxl":
        # Ancien pipeline SDXL (fallback)
        try:
            from app.services.archive.image_gen import generate_astro_image as sdxl_generate
        except Exception as e:
            logger.error("[image_gen] Impossible d'importer archive.image_gen.generate_astro_image", exc_info=True)
            raise
        return sdxl_generate(theme_json_path, output_path=output_path, **kwargs)

    else:
        raise ValueError(f"[image_gen] IMAGE_BACKEND inconnu: {backend} (attendu: 'openai' ou 'sdxl')")
