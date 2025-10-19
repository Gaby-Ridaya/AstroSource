# -*- coding: utf-8 -*-
"""
astro_prompt_fusion.py
Modulaire : fusionne plusieurs bibliothèques de prompts (tes JSON) pour générer
un prompt SDXL riche à partir d'un thème astro (JSON produit par astro_calcule.py).

Usage rapide :
    from astro_prompt_fusion import PromptFusion, load_json, sha_seed_from_planets
    theme = load_json("theme_amadeo.json")
    libs = PromptFusion.load_libs({
        "astro_peinter": "astro_peinter.json",
        "nombre_dor": "enriched_nombre_dor.json",
        "nombre_dor_abstrait": "enriched_nombre_dor_abstrait.json",
        "symbolique_maisons": "enriched_symbolique_abstraite.json",
        "filippo": "Filippo.json",
        "palette_couleurs": "palette_couleurs.json",
        "impressionniste": "impressionniste_associe.json",
        "planete_peintre": "planete_peintre.json",
        "mystical_4k": "mystical_4k.json"
    })
    pf = PromptFusion(theme, **libs)
    prompt = pf.build_prompt(mode="figuratif")  # "abstrait", "architectural", "mystique"
"""

from typing import Dict, Any, List, Optional, Tuple
import json, hashlib, random


# ---------- IO ----------
def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Seed & petites analyses ----------
def sha_seed_from_planets(theme: Dict[str, Any]) -> int:
    s = "|".join(f"{k}:{v:.5f}" for k, v in sorted(theme.get("planetes", {}).items()))
    h = hashlib.sha256(s.encode()).hexdigest()
    return int(h[:8], 16)


def dominant_houses(planetes_maison: Dict[str, int], k: int = 3) -> List[int]:
    counts = {}
    for _, m in planetes_maison.items():
        counts[m] = counts.get(m, 0) + 1
    return sorted(counts, key=lambda x: counts[x], reverse=True)[:k]


def aspects_mood(aspects: List[Dict[str, Any]]) -> List[str]:
    mood = []
    for a in aspects:
        t = a.get("aspect", "")
        if t in ("☌", "☍"):
            mood.append("polar tension and union of opposites")
        elif t in ("△", "✶"):
            mood.append("harmonious flow and grace")
        elif t in ("□",):
            mood.append("creative friction, crackling energy")
    # Dédupliquer et limiter
    out = []
    for m in mood:
        if m not in out:
            out.append(m)
    return out[:4] or ["mysterious equilibrium"]


def palette_words_from_theme(style_theme: Dict[str, Any]) -> List[str]:
    words = []

    def pick(hexcol):
        if not isinstance(hexcol, str) or not hexcol.startswith("#"):
            return
        r = int(hexcol[1:3], 16)
        g = int(hexcol[3:5], 16)
        b = int(hexcol[5:7], 16)
        if r > 200 and g > 160 and b < 90:
            words.append("warm gold")
        elif b > 180 and r < 120:
            words.append("deep sapphire")
        elif g > 180 and r < 120:
            words.append("emerald green")
        elif r > 200 and b > 180:
            words.append("magenta-violet")
        elif r > 180 and g < 110:
            words.append("crimson")

    for k in ["background", "band_color", "deco2_color", "title_color"]:
        pick(style_theme.get(k))
    if not words:
        words = ["deep blue", "crimson", "antique gold"]
    # dédoublonnage en conservant l'ordre
    out = []
    for w in words:
        if w not in out:
            out.append(w)
    return out


# ---------- Classe principale ----------
class PromptFusion:
    @staticmethod
    def load_libs(paths: Dict[str, str]) -> Dict[str, Any]:
        out = {}
        for key, p in paths.items():
            try:
                out[key] = load_json(p)
            except Exception:
                out[key] = None
        return out

    def __init__(
        self,
        theme: Dict[str, Any],
        astro_peinter: Optional[Dict[str, Any]] = None,
        nombre_dor: Optional[Dict[str, Any]] = None,
        nombre_dor_abstrait: Optional[Dict[str, Any]] = None,
        symbolique_maisons: Optional[Dict[str, Any]] = None,
        filippo: Optional[Dict[str, Any]] = None,
        palette_couleurs: Optional[Dict[str, Any]] = None,
        impressionniste: Optional[Dict[str, Any]] = None,
        planete_peintre: Optional[Dict[str, Any]] = None,
        mystical_4k: Optional[Dict[str, Any]] = None,
    ):
        self.theme = theme
        self.libs = {
            "astro_peinter": astro_peinter,
            "nombre_dor": nombre_dor,
            "nombre_dor_abstrait": nombre_dor_abstrait,
            "symbolique_maisons": symbolique_maisons,
            "filippo": filippo,
            "palette_couleurs": palette_couleurs,
            "impressionniste": impressionniste,
            "planete_peintre": planete_peintre,
            "mystical_4k": mystical_4k,
        }
        self.seed = sha_seed_from_planets(theme)
        random.seed(self.seed)

    # --- Sélection style pictural (peintres/écoles) ---
    def pick_style_peintre(self) -> str:
        parts = []
        # Biais Botticelli subtil si astro_peinter présent
        if self.libs.get("astro_peinter"):
            parts.append("byzantine grace, Botticelli-like elegance")
        # Palette-couleurs / impressionnistes / planete_peintre peuvent affiner
        if self.libs.get("planete_peintre") or self.libs.get("impressionniste"):
            parts.append(
                "pre-Raphaelite softness, sacred light, delicate mythic atmosphere"
            )
        # Fallback
        if not parts:
            parts.append("symbolist painting, visionary and sacred light")
        return ", ".join(parts)

    # --- Motifs depuis maisons dominantes ---
    def motifs_from_houses(self) -> List[str]:
        pm = self.theme.get("planetes_maison", {})
        dom = dominant_houses(pm)
        motifs = []
        sm = self.libs.get("symbolique_maisons") or {}
        table = sm.get("maison_animaux_mythiques") if sm else None
        if table:
            for h in dom:
                node = table.get(str(h))
                if node:
                    motifs.append(node.get("description abstraite", ""))
        else:
            motifs += ["mystic geometry", "sacred mandala", "cosmic lattice"]
        # Limiter et nettoyer
        motifs = [m for m in motifs if m]
        return motifs[:6]

    # --- Géométrie φ : florale figurative ou abstraction pure ---
    def floral_or_abstrait(self, mode: str = "figuratif") -> str:
        text = ""
        if mode == "figuratif" and self.libs.get("nombre_dor"):
            text = "sacred floral geometry guided by the golden ratio (φ), rosace patterns, spirals of life"
        elif mode == "abstrait" and self.libs.get("nombre_dor_abstrait"):
            text = "pure abstract geometry based on φ, spiral lattices, no figurative elements"
        return text

    # --- Architecture Brunelleschi (Filippo) ---
    def architecture_perspective(self) -> str:
        if self.libs.get("filippo"):
            return "Brunelleschi-inspired perspective, vanishing lines, radial symmetry, sacred architectural depth"
        return ""

    # --- Humeur des aspects + palette du thème ---
    def aspects_palette(self) -> Tuple[str, str]:
        mood = ", ".join(aspects_mood(self.theme.get("aspects", [])))
        palette = ", ".join(palette_words_from_theme(self.theme.get("theme", {})))
        return mood, palette

    # --- Choix du mode ---
    def choose_mode(self, mode: str = None) -> str:
        modes = ["figuratif", "abstrait", "architectural", "mystique"]
        if not mode:
            return modes[self.seed % len(modes)]
        return mode if mode in modes else "figuratif"

    # --- Construction du prompt final ---
    def build_prompt(self, mode: str = None) -> str:
        mode = self.choose_mode(mode)
        pm = self.theme.get("planetes_maison", {})
        sun_h = pm.get("Sun", "?")
        moon_h = pm.get("Moon", "?")

        style = self.pick_style_peintre()
        motifs = self.motifs_from_houses()
        floral = self.floral_or_abstrait(
            "abstrait" if mode == "abstrait" else "figuratif"
        )
        archi = (
            self.architecture_perspective()
            if mode in ("figuratif", "architectural")
            else ""
        )
        mood, palette = self.aspects_palette()

        lines = [
            f"Visionary symbolic painting from natal chart; Sun house {sun_h}, Moon house {moon_h}.",
            f"Style: {style}.",
            f"Motifs from dominant houses: {', '.join(motifs)}." if motifs else "",
            f"{floral}.",
            f"{archi}.",
            f"Emotional tone: {mood}.",
            f"Color palette: {palette}.",
            "Painterly textures, masterful composition, rich gradients, chiaroscuro depth, 8k, masterpiece.",
        ]

        # Option “mystique” : injecter une saveur si lib fournie
        if mode == "mystique" and self.libs.get("mystical_4k"):
            arr = self.libs["mystical_4k"].get("prompts", [])
            if arr:
                # court fragment pour donner la saveur sans noyer SDXL
                lines.append(arr[0][:300])

        elif mode == "paysage":
            lines.append(
                "landscape orientation, vast natural vistas, atmospheric perspective, depth of field, inspired by nature, skies, and the four elements"
            )

        return " ".join([l for l in lines if l]).strip()
