"""
PromptGenerationService — DALL·E friendly
=========================================

Version simple et robuste pour générer un *prompt texte* à partir d'un
JSON de thème astro (celui produit par astro_calcule).

• Zéro dépendance aux anciens fichiers de prompts.
• Renvoie une chaîne compacte et optimisée pour DALL·E / OpenAI Images.
• Fournit une instance globale `prompt_generation_service` importable par l'API.

Intégration attendue côté API:
from app.services.prompt_generation import prompt_generation_service
text_prompt = prompt_generation_service.generate_prompt(path_to_theme_json)

Auteur: vous :)
"""

from __future__ import annotations

import json
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class PromptGenerationService:
    """Génère un prompt unique et compact pour DALL·E/OpenAI Images.

    Entrée: chemin vers un JSON de thème contenant au minimum:
      - "planetes" (dict: Sun/Moon/Mercury/... -> degré 0..360)
      - "ascendant" (float, optionnel)
      - "mc" (float, optionnel)
    """

    SIGNS_FR = [
        "Bélier",
        "Taureau",
        "Gémeaux",
        "Cancer",
        "Lion",
        "Vierge",
        "Balance",
        "Scorpion",
        "Sagittaire",
        "Capricorne",
        "Verseau",
        "Poissons",
    ]

    ELEMENTS = {
        "Bélier": "Feu",
        "Lion": "Feu",
        "Sagittaire": "Feu",
        "Taureau": "Terre",
        "Vierge": "Terre",
        "Capricorne": "Terre",
        "Gémeaux": "Air",
        "Balance": "Air",
        "Verseau": "Air",
        "Cancer": "Eau",
        "Scorpion": "Eau",
        "Poissons": "Eau",
    }

    # Palettes rapides par élément (pour orienter les couleurs, reste souple)
    ELEMENT_PALETTES = {
        "Feu": ["or solaire", "ambre", "rouge carmin", "orange incandescent"],
        "Terre": ["ocre", "vert sauge", "brun antique", "pierre calcaire"],
        "Air": ["bleu aube", "argent clair", "blanc lumineux", "bleu azur"],
        "Eau": ["bleu indigo", "turquoise", "nacré", "violet mystique"],
    }

    # Styles poétiques (libres, aucun autre fichier requis)
    STYLES = {
        "Lumière des Anciens": {
            "ambiance": "sublime, serein, halo doré, composition harmonieuse",
            "références": "Botticelli, Raphaël, Vermeer (inspirations, pas de copie)",
        },
        "Brume romantique divine": {
            "ambiance": "vaporeux, contemplatif, brume douce, lumière diffuse",
            "références": "Turner, Caspar David Friedrich (inspirations)",
        },
        "Mystères Symboliques": {
            "ambiance": "mystique, onirique, symboles subtils, profondeur",
            "références": "Redon, Moreau (inspirations)",
        },
        "Fusion des astres": {
            "ambiance": "abstrait cosmique, spirales, géométrie sacrée, énergie",
            "références": "Kandinsky, Hilma af Klint (inspirations)",
        },
    }

    PLANET_LABELS_FR = {
        "Sun": "Soleil",
        "Moon": "Lune",
        "Mercury": "Mercure",
        "Venus": "Vénus",
        "Mars": "Mars",
        "Jupiter": "Jupiter",
        "Saturn": "Saturne",
        "Uranus": "Uranus",
        "Neptune": "Neptune",
        "Pluto": "Pluton",
        "Chiron": "Chiron",
        "North Node": "Nœud Nord",
    }

    def __init__(self) -> None:
        logger.info("🎨 PromptGenerationService (DALL·E) initialisé")

    # --- Utils -------------------------------------------------------------
    def deg_to_sign(self, deg: float) -> str:
        try:
            return self.SIGNS_FR[int(deg // 30) % 12]
        except Exception:
            return "?"

    def dominant_elements(self, planetes: Dict[str, float]) -> Dict[str, int]:
        count = {"Feu": 0, "Terre": 0, "Air": 0, "Eau": 0}
        for _, lon in (planetes or {}).items():
            sign = self.deg_to_sign(lon)
            elem = self.ELEMENTS.get(sign)
            if elem:
                count[elem] += 1
        return count

    def _format_deg(self, lon: Optional[float]) -> str:
        if lon is None:
            return "—"
        d = lon % 30
        return f"{int(d):02d}°{int((d % 1)*60):02d}'"

    # --- Public API --------------------------------------------------------
    def generate_prompt(
        self, theme_path: str, style_poetique: Optional[str] = None
    ) -> str:
        """Charge le JSON du thème et renvoie un prompt texte concis pour DALL·E.

        :param theme_path: chemin vers le JSON du thème
        :param style_poetique: nom de style facultatif (clé de STYLES)
        """
        if not theme_path or not os.path.exists(theme_path):
            msg = f"404: Fichier thème non trouvé: {theme_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        with open(theme_path, "r", encoding="utf-8") as f:
            theme = json.load(f)

        return self.generate_prompt_from_theme(theme, style_poetique)

    def generate_prompt_from_theme(
        self, theme: Dict[str, Any], style_poetique: Optional[str] = None
    ) -> str:
        planetes: Dict[str, float] = theme.get("planetes", {})
        asc: Optional[float] = theme.get("ascendant")
        mc: Optional[float] = theme.get("mc")

        # Signes principaux
        sun_sign, moon_sign = None, None
        if "Sun" in planetes:
            sun_sign = self.deg_to_sign(planetes["Sun"])
        if "Moon" in planetes:
            moon_sign = self.deg_to_sign(planetes["Moon"])
        asc_sign = self.deg_to_sign(asc) if isinstance(asc, (int, float)) else None

        # Éléments dominants & palette suggérée
        elems = self.dominant_elements(planetes)
        dominant = sorted(elems.items(), key=lambda x: x[1], reverse=True)
        top_elem = dominant[0][0] if dominant else None
        palette = self.ELEMENT_PALETTES.get(top_elem or "Air", [])

        # Choix du style
        style_name = (
            style_poetique if style_poetique in self.STYLES else "Fusion des astres"
        )
        style_info = self.STYLES[style_name]

        # Mini résumé astro (compact)
        parts: List[str] = []
        if sun_sign:
            parts.append(f"Soleil {sun_sign}")
        if moon_sign:
            parts.append(f"Lune {moon_sign}")
        if asc_sign:
            parts.append(f"Ascendant {asc_sign}")
        resume = ", ".join(parts) if parts else "profil cosmique"

        # Motifs géométriques selon l'élément dominant
        motif = {
            "Feu": "rayonnement solaire, spirales dynamiques, éclats lumineux",
            "Terre": "structures minérales, textures pierre/bois, géométrie stable",
            "Air": "arabesques aériennes, fines lignes, réseau éthéré",
            "Eau": "ondes fluides, volutes brumeuses, profondeur nacrée",
        }.get(top_elem or "Air")

        # Interdictions et balises utiles pour TTI
        safety = (
            "no text, no watermark, clean composition, ultra-detailed, high quality, "
            "tasteful, refined, single artwork"
        )

        # Construction du prompt final (1 seul bloc concis)
        prompt = (
            f"Astrological abstract artwork about {resume}; "
            f"style: {style_name} ({style_info['ambiance']}); "
            f"visual language: sacred geometry, {motif}; "
            f"color palette hint: {', '.join(palette)}; "
            f"subtle zodiac cues only (no glyphs text), harmonious lighting; {safety}."
        )

        # Ajout d'indices optionnels (positions résumées)
        if sun_sign or moon_sign or asc_sign:
            extra_bits: List[str] = []
            if "Sun" in planetes:
                extra_bits.append(
                    f"Sun in {sun_sign} @ {self._format_deg(planetes['Sun'])}"
                )
            if "Moon" in planetes:
                extra_bits.append(
                    f"Moon in {moon_sign} @ {self._format_deg(planetes['Moon'])}"
                )
            if isinstance(asc, (int, float)):
                extra_bits.append(f"Ascendant {asc_sign} @ {self._format_deg(asc)}")
            if isinstance(mc, (int, float)):
                extra_bits.append(f"MC {self.deg_to_sign(mc)} @ {self._format_deg(mc)}")
            prompt += " " + "; ".join(extra_bits) + "."

        return prompt


# Instance globale importable par l'API
prompt_generation_service = PromptGenerationService()


if __name__ == "__main__":
    # Petit test manuel (ne lira rien si vous ne donnez pas de chemin)
    import sys

    if len(sys.argv) > 1:
        p = PromptGenerationService()
        print(p.generate_prompt(sys.argv[1]))
    else:
        print("Usage: python prompt_generation.py /chemin/vers/theme.json")
