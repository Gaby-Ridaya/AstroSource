"""
Service de gestion des interprétations astrologiques
Gère le chargement et la distribution des interprétations
"""

from pathlib import Path
import json
import logging
from typing import Dict, List, Any
from functools import lru_cache

logger = logging.getLogger(__name__)


class InterpretationService:
    """Service pour la gestion des interprétations astrologiques"""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        self.interpretations_dir = self.data_dir / "interpretations_json"
        logger.info(
            f"📚 Service d'interprétations initialisé: {self.interpretations_dir}"
        )

    @lru_cache(maxsize=10)
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """
        Charge un fichier JSON avec mise en cache

        Args:
            filename: Nom du fichier JSON (sans extension)

        Returns:
            Contenu du fichier JSON
        """
        file_path = self.interpretations_dir / f"{filename}.json"

        if not file_path.exists():
            logger.warning(f"⚠️ Fichier non trouvé: {file_path}")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            logger.info(f"✅ Fichier {filename}.json chargé: {len(data)} entrées")
            return data

        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement de {filename}.json: {e}")
            return {}

    async def get_planet_interpretations(self) -> Dict[str, Any]:
        """Retourne toutes les interprétations des planètes"""
        return self._load_json_file("planets")

    async def get_house_interpretations(self) -> Dict[str, Any]:
        """Retourne toutes les interprétations des maisons"""
        return self._load_json_file("houses")

    async def get_aspect_interpretations(self) -> Dict[str, Any]:
        """Retourne toutes les interprétations des aspects"""
        return self._load_json_file("aspects")

    async def get_sign_interpretations(self) -> Dict[str, Any]:
        """Retourne toutes les interprétations des signes"""
        return self._load_json_file("signs")

    async def get_celebrities(self) -> List[Dict[str, Any]]:
        """
        Retourne la liste des célébrités pour l'étude

        Returns:
            Liste des célébrités avec leurs informations
        """
        celebrities = self._load_json_file("celebrities")

        if not celebrities:
            # Données par défaut si le fichier n'existe pas
            return [
                {
                    "nom": "Albert Einstein",
                    "profession": "Physicien",
                    "date_naissance": "14/03/1879",
                    "lieu_naissance": "Ulm, Allemagne",
                },
                {
                    "nom": "Marie Curie",
                    "profession": "Physicienne",
                    "date_naissance": "07/11/1867",
                    "lieu_naissance": "Varsovie, Pologne",
                },
                {
                    "nom": "Leonardo da Vinci",
                    "profession": "Artiste",
                    "date_naissance": "15/04/1452",
                    "lieu_naissance": "Vinci, Italie",
                },
                {
                    "nom": "Mozart",
                    "profession": "Compositeur",
                    "date_naissance": "27/01/1756",
                    "lieu_naissance": "Salzbourg, Autriche",
                },
            ]

        return (
            celebrities if isinstance(celebrities, list) else list(celebrities.values())
        )

    async def get_interpretation_summary(self) -> Dict[str, int]:
        """
        Retourne un résumé du nombre d'interprétations disponibles

        Returns:
            Dictionnaire avec le nombre d'interprétations par catégorie
        """
        summary = {}

        for category in ["planets", "houses", "aspects", "signs"]:
            data = self._load_json_file(category)
            summary[category] = len(data) if data else 0

        celebrities = await self.get_celebrities()
        summary["celebrities"] = len(celebrities)

        logger.info(f"📊 Résumé des interprétations: {summary}")
        return summary


# Instance globale du service
interpretation_service = InterpretationService()
