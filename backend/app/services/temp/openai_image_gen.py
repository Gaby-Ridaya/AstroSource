import os, re, json, glob, base64, time, logging, zipfile
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from openai import OpenAI
from app.services.astro_prompt_fusion import PromptFusion
from app.services.prompt_generation import prompt_generation_service

# ============================================================
# Config & logging
# ============================================================
PROMPT_DIR = "/home/gaby/AstroSource/backend/app/prompts"
UTILISATEURS_DIR = "/home/gaby/AstroSource/data/Utilisateurs"
MAX_RETRIES = 4

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("openai_image_gen")

# ============================================================
# Tables et helpers métier
# ============================================================
SIGNE_FR = {
    "Aries": "Bélier",
    "Taurus": "Taureau",
    "Gemini": "Gémeaux",
    "Cancer": "Cancer",
    "Leo": "Lion",
    "Virgo": "Vierge",
    "Libra": "Balance",
    "Scorpio": "Scorpion",
    "Sagittarius": "Sagittaire",
    "Capricorn": "Capricorne",
    "Aquarius": "Verseau",
    "Pisces": "Poissons",
}
SIGNS_EN = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

SIGNE_TO_ELEMENT = {
    "Aries": "Feu",
    "Leo": "Feu",
    "Sagittarius": "Feu",
    "Taurus": "Terre",
    "Virgo": "Terre",
    "Capricorn": "Terre",
    "Gemini": "Air",
    "Libra": "Air",
    "Aquarius": "Air",
    "Cancer": "Eau",
    "Scorpio": "Eau",
    "Pisces": "Eau",
}
ELEMENT_PALETTE = {
    # Tu peux ajuster ces palettes si tu veux (noms ou HEX)
    "Feu": ["deep amber", "warm gold", "crimson glow"],
    "Terre": ["moss green", "aged ochre", "stone gray"],
    "Air": ["sapphire blue", "silver mist", "pale cyan"],
    "Eau": ["indigo", "turquoise haze", "pearl white"],
}
ASC_RULER = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Pluto",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Uranus",
    "Pisces": "Neptune",
}
PLANETE_TO_ARTISTE = {
    "Mars": "bold surrealism of Zdzisław Beksiński (but without figures)",
    "Venus": "romantic impressionism of Claude Monet",
    "Mercury": "intricate symbolic art of M.C. Escher",
    "Jupiter": "grand renaissance landscapes of Claude Lorrain",
    "Saturn": "mystical chiaroscuro of Rembrandt landscapes",
    "Uranus": "futuristic geometry of Syd Mead",
    "Neptune": "dreamlike seascapes of Ivan Aivazovsky",
    "Pluto": "cosmic abstract of Hilma af Klint",
    "Moon": "poetic nocturnes of James McNeill Whistler",
    "Sun": "luminous classicism of J. M. W. Turner",
}


def deg_to_sign(deg: float) -> str:
    return SIGNS_EN[int(deg // 30) % 12]


def _sign_fr_from_deg(deg):
    if deg is None:
        return None
    try:
        return SIGNE_FR[deg_to_sign(float(deg))]
    except Exception:
        return None


def detecter_signes(theme_json: dict) -> Tuple[str, str]:
    sun_deg = theme_json.get("planetes", {}).get("Sun")
    asc_deg = theme_json.get("ascendant")
    sun_sign = deg_to_sign(float(sun_deg)) if sun_deg is not None else "Aries"
    asc_sign = deg_to_sign(float(asc_deg)) if asc_deg is not None else "Aries"
    return sun_sign, asc_sign


def planete_dominante_depuis_asc(asc_sign: str) -> str:
    return ASC_RULER.get(asc_sign, "Sun")


# ============================================================
# OpenAI client
# ============================================================
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        dotenv_path = "/home/gaby/AstroSource/.env"
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path=dotenv_path)
            api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY manquante. Mets-la dans .env ou exporte-la.")
    return OpenAI(api_key=api_key)


# ============================================================
# Fichiers & utilitaires
# ============================================================
def _find_last_image(user_dir: str):
    imgs = []
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        imgs.extend(glob.glob(os.path.join(user_dir, ext)))
    if not imgs:
        return None
    imgs.sort(key=os.path.getmtime, reverse=True)
    return imgs[0]


def _make_placeholder(path: str, w: int, h: int, msg: str):
    try:
        from PIL import Image, ImageDraw

        img = Image.new("RGB", (w, h), (30, 30, 30))
        d = ImageDraw.Draw(img)
        tw = d.textlength(msg)
        d.text(((w - tw) / 2, h / 2 - 8), msg, fill=(220, 220, 220))
        img.save(path)
    except Exception:
        # Pillow pas dispo
        open(path, "wb").write(b"")


def _extract_meta_for_pdf(theme_json: dict, json_path: str) -> dict:
    meta = {"nom": "—", "ville": "—", "date": "—", "heure": "—"}
    if isinstance(theme_json, dict):
        m = theme_json.get("meta") or {}
        meta["nom"] = m.get("nom") or m.get("name") or meta["nom"]
        meta["ville"] = (
            m.get("ville") or m.get("city") or m.get("lieu") or meta["ville"]
        )
        meta["date"] = m.get("date") or m.get("date_naissance") or meta["date"]
        meta["heure"] = m.get("heure") or m.get("heure_naissance") or meta["heure"]
    user_dir = os.path.dirname(json_path)
    if meta["nom"] == "—":
        meta["nom"] = os.path.basename(user_dir) if user_dir else meta["nom"]
    return meta


# ============================================================
# Interprétations (style Max Heindel) + brief image
# ============================================================
def _interprete_aspects_heindel(theme_json: dict) -> str:
    plan = theme_json.get("planetes", {})
    sun_fr = _sign_fr_from_deg(plan.get("Sun"))
    moon_fr = _sign_fr_from_deg(plan.get("Moon"))
    asc_fr = _sign_fr_from_deg(theme_json.get("ascendant"))

    lines = []
    lines.append("Tableau d’influences — Lecture spirituelle du thème")

    if sun_fr:
        lines.append(
            f"Le Soleil en {sun_fr} éclaire la conscience d’une lumière intérieure qui appelle à la transformation. "
            f"C’est une invitation à transmuer les épreuves en clarté, comme l’alchimiste tirant l’or du plomb."
        )
    if moon_fr:
        lines.append(
            f"La Lune en {moon_fr} façonne la mémoire et le rythme intime. "
            f"Elle enseigne la maîtrise paisible des émotions, érigeant des fondations sûres pour l’édifice de l’âme."
        )
    if asc_fr:
        lines.append(
            f"L’Ascendant en {asc_fr} ouvre un portail de destinée : il oriente l’expression du soi vers un service plus vaste, "
            f"où la compassion et la discipline se rencontrent."
        )

    aspects = theme_json.get("aspects_text")
    forces, affinites, oppositions = [], [], []
    pat = re.compile(
        r"^\s*([A-Za-z ]+)\s+([☌□△✶☍])\s+([A-Za-z ]+)\s+\(orbe:\s*([\d.]+)°\)"
    )
    if isinstance(aspects, list):
        for raw in aspects:
            m = pat.match(raw)
            if not m:
                continue
            p1, sym, p2, orb = (
                m.group(1).strip(),
                m.group(2),
                m.group(3).strip(),
                m.group(4),
            )
            if sym == "□":
                forces.append(f"{p1} {sym} {p2} (orbe {orb}°)")
            elif sym in ("△", "✶", "☌"):
                affinites.append(f"{p1} {sym} {p2} (orbe {orb}°)")
            elif sym == "☍":
                oppositions.append(f"{p1} {sym} {p2} (orbe {orb}°)")

    if forces:
        lines.append(
            "Les angles de crise révèlent la force latente : par l’effort conscient, l’obstacle devient un degré d’ascension. "
            + "Exemples : "
            + ", ".join(forces)
            + "."
        )
    if affinites:
        lines.append(
            "Les affinités naturelles indiquent les voies de grâce où l’âme circule sans heurt : cultiver ces courants élève sans forcer. "
            + "Exemples : "
            + ", ".join(affinites)
            + "."
        )
    if oppositions:
        lines.append(
            "Les oppositions enseignent l’art de la mesure : au centre des contraires se tient une paix active, fondée sur l’équilibre. "
            + "Exemples : "
            + ", ".join(oppositions)
            + "."
        )

    lines.append(
        "Ainsi, chaque influence devient un instrument d’élévation : en cultivant la vigilance, la bonne volonté et la constance, "
        "l’être ajuste son pas au rythme des lois divines et progresse vers une conscience plus lumineuse."
    )

    return "\n\n".join(lines).strip()


def _brief_image_depuis_interpretations(interpretations: str, theme_json: dict) -> str:
    sun_sign, asc_sign = detecter_signes(theme_json)
    element = SIGNE_TO_ELEMENT.get(sun_sign, "Air")
    palette = ", ".join(ELEMENT_PALETTE[element])
    planete_dom = planete_dominante_depuis_asc(asc_sign)
    artiste = PLANETE_TO_ARTISTE.get(planete_dom, "cosmic abstract minimalism")

    motifs = []
    if "angles de crise" in interpretations:
        motifs.append("angles of crisis forging inner strength")
    if "affinités naturelles" in interpretations:
        motifs.append("natural affinities and flowing currents")
    if "oppositions" in interpretations:
        motifs.append("oppositions teaching equilibrium")
    if not motifs:
        motifs = ["balanced harmonies and tensions"]
    motifs_txt = ", ".join(motifs[:2])

    return (
        f"Astrological abstract landscape (landscape orientation). "
        f"Inspired by Sun in {sun_sign}, Ascendant ruled by {planete_dom}. "
        f"Element: {element} — colors: {palette}. "
        f"Art style: {artiste}. "
        f"Focus on symbolism from: {motifs_txt}. "
        f"No humans/animals/faces, only landscapes, sacred geometry, cosmic patterns. "
        f"High detail, HDR, elegant composition, natural depth, clean edges."
    ).strip()


# ============================================================
# OpenAI images
# ============================================================
def _generate_with_retries(model: str, prompt: str, size: str = "1024x1024"):
    delay = 1.5
    client = get_openai_client()
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return client.images.generate(model=model, prompt=prompt, size=size)
        except Exception as e:
            last_error = e
            if attempt == MAX_RETRIES:
                raise
            log.warning(
                f"[try {attempt}/{MAX_RETRIES}] images.generate a échoué: {e} — retry dans {delay:.1f}s"
            )
            time.sleep(delay)
            delay *= 2
    if last_error:
        raise last_error


# ============================================================
# PDF (délégué à pdf_builder)
# ============================================================
from app.services.pdf_builder import make_pdf_pro


# ============================================================
# API
# ============================================================
def get_image_model_default():
    return os.getenv("ASTRO_IMAGE_MODEL") or "gpt-image-1"


def run_from_json(json_path: str, **kwargs):
    return generer_image_openai(json_path, **kwargs)


def generer_image_openai(
    json_path: str, *, size=None, force_regen_prompt: bool = False, **kwargs
):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Theme JSON introuvable: {json_path}")

    user_dir = os.path.dirname(json_path)
    stem = os.path.splitext(os.path.basename(json_path))[0]
    os.makedirs(user_dir, exist_ok=True)

    svg_path = os.path.join(user_dir, f"{stem}.svg")
    interpret_path = os.path.join(user_dir, f"{stem}_interpretations.txt")
    image_prompt_path = os.path.join(user_dir, f"{stem}_image_prompt.txt")
    image_path = os.path.join(user_dir, f"{stem}_image.png")
    pack_path = os.path.join(user_dir, f"{stem}_pack.zip")
    pdf_path = os.path.join(user_dir, f"{stem}_interpretations.pdf")

    theme_json = json.load(open(json_path, "r", encoding="utf-8"))

    # --- Interprétations (Heindel)
    regen_interpret = force_regen_prompt or (not os.path.exists(interpret_path))
    if regen_interpret:
        interpretations = _interprete_aspects_heindel(theme_json).strip()
        open(interpret_path, "w", encoding="utf-8").write(interpretations + "\n")
        log.info(f"📝 Interprétations (Heindel) générées dans {interpret_path}")
    else:
        interpretations = open(interpret_path, "r", encoding="utf-8").read().strip()
        log.info(f"📝 Interprétations réutilisées (cache) depuis {interpret_path}")

    # --- Brief image (lisible dans le .txt, compact pour l'IA)
    # --- Brief image via PromptGenerationService (paysage + style)
    regen_img_prompt = force_regen_prompt or (not os.path.exists(image_prompt_path))
    if regen_img_prompt:
        # 👇 Choisis le style par défaut ici (change le texte si tu veux)
        style_defaut = "Fusion des astres"

        # 1) prompt compact (fait par prompt_generation.py)
        compact = prompt_generation_service.generate_prompt_from_theme(
            theme_json, style_poetique=style_defaut
        ).strip()

        # 2) on force "paysage" une fois pour toutes
        compact = (
            "Landscape orientation, vast natural vistas, atmospheric perspective, depth of field. "
            + compact
        ).strip()

        # 3) version lisible multi-lignes (pour le .txt)
        readable = (compact.replace(". ", ".\n").replace(", ", ",\n- ")).strip()

        with open(image_prompt_path, "w", encoding="utf-8") as f:
            f.write(readable + "\n")
        log.info(f"📝 Brief image écrit : {image_prompt_path}")
    else:
        readable = open(image_prompt_path, "r", encoding="utf-8").read().strip()
        compact = " ".join(readable.split())
        log.info(f"📝 Brief image réutilisé (cache) depuis {image_prompt_path}")

    # --- Image IA
    width, height = 1536, 1024
    size_str = f"{width}x{height}"
    if os.getenv("ASTRO_IMAGE_MOCK") == "1":
        log.warning("🧪 MOCK MODE actif — création d'un placeholder local.")
        _make_placeholder(image_path, width, height, "MOCK MODE")
    else:
        model = get_image_model_default()
        log.info(f"🎨 Génération image via {model} taille={size_str}")
        try:
            resp = _generate_with_retries(model=model, prompt=compact, size=size_str)
            b64 = None
            if hasattr(resp, "data") and resp.data:
                datum = resp.data[0]
                if hasattr(datum, "b64_json"):
                    b64 = datum.b64_json
                elif isinstance(datum, dict) and "b64_json" in datum:
                    b64 = datum["b64_json"]
            if not b64:
                raise RuntimeError("Réponse images.generate sans b64_json.")
            open(image_path, "wb").write(base64.b64decode(b64))
            log.info(f"🖼️ Image sauvegardée dans {image_path}")
        except Exception as e:
            if "billing_hard_limit" in str(e).lower():
                log.warning("💸 Quota OpenAI atteint — fallback local.")
                last = _find_last_image(user_dir)
                if last:
                    image_path = last
                    log.info(f"🔁 Réutilisation de la dernière image: {image_path}")
                else:
                    _make_placeholder(image_path, width, height, "Quota épuisé")
                    log.info("🧱 Placeholder généré.")
            else:
                raise

    # --- PDF (texte seul, pas d’images, pas de SVG)
    meta_for_pdf = _extract_meta_for_pdf(theme_json, json_path)
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    except Exception:
        pass

    make_pdf_pro(
        theme_json=theme_json,
        txt_path=interpret_path,
        pdf_path=pdf_path,
        json_path=json_path,
        title="Interprétations astrologiques",
        subtitle="AstroSource",
        options={
            "font_main": "Times-Roman",
            "font_bold": "Times-Bold",
            "font_small": "Times-Roman",
            "title_size": 24,
            "subtitle_size": 13,
            "text_size": 11,
            "small_size": 9,
            "margin_x_cm": 2.2,
            "margin_y_cm": 2.2,
            "header_h_cm": 1.8,
            "footer_h_cm": 1.2,
            "line_h": 16,
            "max_chars": 96,
            "bullet_indent_cm": 0.7,
        },
    )
    log.info(f"📄 PDF des interprétations (pro) créé: {pdf_path}")

    # --- ZIP (on garde le SVG dans le pack, mais pas dans le PDF)
    with zipfile.ZipFile(pack_path, "w", zipfile.ZIP_DEFLATED) as z:
        if os.path.exists(svg_path):
            z.write(svg_path, arcname=f"{stem}.svg")
        if os.path.exists(image_path):
            z.write(image_path, arcname=os.path.basename(image_path))
        z.write(interpret_path, arcname=f"{stem}_interpretations.txt")
        if os.path.exists(pdf_path):
            z.write(pdf_path, arcname=f"{stem}_interpretations.pdf")
        if os.path.exists(image_prompt_path):
            z.write(image_prompt_path, arcname=f"{stem}_image_prompt.txt")

    return {
        "image": image_path,
        "prompt_file": image_prompt_path,
        "interpretations": interpret_path,
        "image_prompt": image_prompt_path,
        "svg": svg_path,
        "pdf": pdf_path,
        "pack": pack_path,
    }


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python openai_image_gen.py /chemin/vers/theme_user.json")
        raise SystemExit(1)
    print(generer_image_openai(sys.argv[1], size="1536x1024", force_regen_prompt=True))
