"""
Service de génération de thèmes astraux
Encapsule la logique de génération SVG
"""

from pathlib import Path
import logging
import sys
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AstroGenerationService:
    """Service pour la génération de thèmes astraux"""

    def __init__(self):
        self.backend_path = Path(__file__).parent.parent.parent
        self._setup_imports()

    def _setup_imports(self):
        """Configure les imports pour les modules de génération"""
        try:
            # Import direct depuis le service de génération SVG
            from .nouvelle_roue import AstroChartSVG
            from .astro_calcule import generate_theme

            self.AstroChartSVG = AstroChartSVG
            self.generate_theme = generate_theme
            logger.info("✅ Modules de génération SVG chargés")
        except ImportError as e:
            logger.error(f"❌ Impossible de charger les modules de génération: {e}")
            self.AstroChartSVG = None
            self.generate_theme = None

    async def generate_astral_chart(
        self, nom: str, ville_naissance: str, date_naissance: str, heure_naissance: str
    ) -> Dict[str, Any]:
        """
        Génère un thème astral complet

        Args:
            nom: Nom de la personne
            ville_naissance: Ville de naissance
            date_naissance: Date au format DD/MM/YYYY
            heure_naissance: Heure au format HH:MM

        Returns:
            Dictionnaire avec les données du thème généré
        """
        if self.generate_theme is None or self.AstroChartSVG is None:
            raise RuntimeError("Modules de génération non disponibles")

        logger.info(f"🎯 Génération du thème pour {nom}")

        try:
            # 1. Générer le JSON du thème astrologique
            json_path = self.generate_theme(
                nom, date_naissance, heure_naissance, ville_naissance
            )

            if not json_path:
                raise Exception("Impossible de générer le thème JSON")

            # 2. Générer le SVG à partir du JSON
            svg_path = json_path.replace(".json", ".svg")
            chart = self.AstroChartSVG(svg_path, json_path)
            chart.make_svg()

            # 3. Lire le contenu SVG généré
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            logger.info(f"✅ Thème généré avec succès pour {nom}")

            return {
                "status": "success",
                "personne": nom,
                "lieu": ville_naissance,
                "date": date_naissance,
                "heure": heure_naissance,
                "svg_content": svg_content,
                "json_path": json_path,
                "svg_path": svg_path,
            }

        except Exception as e:
            logger.error(f"❌ Erreur lors de la génération pour {nom}: {e}")
            raise RuntimeError(f"Erreur de génération: {str(e)}")


# Instance globale du service
astro_service = AstroGenerationService()
from app.services.image_gen import generate_astro_image
import os
import glob

def generer_image_artistique_auto(base_dir_utilisateur: str, mode: str = "figuratif"):
    """
    Cherche automatiquement le fichier theme_*.json dans le dossier utilisateur,
    puis génère l'image artistique correspondante dans le même dossier.
    """
    # Chercher le JSON du thème
    json_files = glob.glob(os.path.join(base_dir_utilisateur, "theme_*.json"))
    if not json_files:
        print(f"[image_gen_auto] Aucun fichier theme_*.json trouvé dans {base_dir_utilisateur}")
        return

    # On prend le premier trouvé (ou le plus récent)
    theme_json_path = max(json_files, key=os.path.getmtime)

    # Construire le chemin de sortie PNG
    base_name = os.path.splitext(os.path.basename(theme_json_path))[0]
    output_path = os.path.join(base_dir_utilisateur, f"{base_name}.png")

    try:
        generate_astro_image(theme_json_path, output_path, mode=mode)
        print(f"[image_gen_auto] Image générée : {output_path}")
    except Exception as e:
        print(f"[image_gen_auto][ERREUR] {e}")
