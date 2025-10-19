# -*- coding: utf-8 -*-
"""
sdxl_astro_modulaire.py
Usage (local) :
    python sdxl_astro_modulaire.py \
        --theme theme_amadeo.json \
        --libs astro_peinter.json enriched_nombre_dor.json enriched_nombre_dor_abstrait.json \
              enriched_symbolique_abstraite.json Filippo.json palette_couleurs.json \
              impressionniste_associe.json planete_peintre.json mystical_4k.json \
        --mode figuratif \
        --model stabilityai/stable-diffusion-xl-base-1.0 \
        --out out.png

En Colab :
 - Uploade ce script + astro_prompt_fusion.py
 - Uploade ton thème et tes libs JSON
 - !pip install ... (voir dépendances)
 - !python sdxl_astro_modulaire.py --theme theme_X.json --libs ... --mode mystique
"""

import argparse, os, sys
from datetime import datetime

# Dépendances IA
import torch
from PIL import Image
from diffusers import StableDiffusionXLPipeline
from compel import Compel

# Notre module
from astro_prompt_fusion import PromptFusion, load_json, sha_seed_from_planets


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--theme", required=True, help="Chemin vers le JSON de thème (astro_calcule.py)"
    )
    ap.add_argument(
        "--libs",
        nargs="+",
        default=[],
        help="Liste de fichiers JSON (bibliothèques de prompt)",
    )
    ap.add_argument(
        "--mode",
        default="figuratif",
        choices=["figuratif", "abstrait", "architectural", "mystique"],
    )
    ap.add_argument(
        "--model",
        default="stabilityai/stable-diffusion-xl-base-1.0",
        help="ID modèle SDXL (HF Hub)",
    )
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--guidance", type=float, default=6.5)
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--height", type=int, default=1024)
    ap.add_argument("--out", default=None, help="Chemin du PNG de sortie")
    return ap.parse_args()


def map_lib_names(paths):
    # Tente d'associer automatiquement les clés attendues selon le nom de fichier
    mapping = {
        "astro_peinter": None,
        "nombre_dor": None,
        "nombre_dor_abstrait": None,
        "symbolique_maisons": None,
        "filippo": None,
        "palette_couleurs": None,
        "impressionniste": None,
        "planete_peintre": None,
        "mystical_4k": None,
    }
    for p in paths:
        low = os.path.basename(p).lower()
        if "astro_peinter" in low or "peinter" in low:
            mapping["astro_peinter"] = p
        elif "nombre_dor_abstrait" in low or "abstrait" in low:
            mapping["nombre_dor_abstrait"] = p
        elif "nombre_dor" in low:
            mapping["nombre_dor"] = p
        elif "symbolique" in low:
            mapping["symbolique_maisons"] = p
        elif "filippo" in low:
            mapping["filippo"] = p
        elif "palette" in low:
            mapping["palette_couleurs"] = p
        elif "impressionniste" in low:
            mapping["impressionniste"] = p
        elif "planete_peintre" in low:
            mapping["planete_peintre"] = p
        elif "mystical_4k" in low or "mystique" in low:
            mapping["mystical_4k"] = p
    return mapping


def main():
    args = parse_args()

    # 1) Charger thème
    theme = load_json(args.theme)

    # 2) Charger libs
    mapping = map_lib_names(args.libs)
    libs = PromptFusion.load_libs({k: v for k, v in mapping.items() if v})

    # 3) Construire prompt
    pf = PromptFusion(theme, **libs)
    prompt = pf.build_prompt(mode=args.mode)
    seed = pf.seed
    print("\n=== PROMPT GÉNÉRÉ ===\n")
    print(prompt)
    print("\nSeed (stable):", seed)

    # 4) Charger pipeline SDXL
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionXLPipeline.from_pretrained(
        args.model,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        use_safetensors=True,
        add_watermarker=False,
    ).to(device)

    compel = Compel(
        tokenizer=pipe.tokenizer,
        text_encoder=pipe.text_encoder,
        tokenizer_2=pipe.tokenizer_2,
        text_encoder_2=pipe.text_encoder_2,
    )

    # 5) Génération
    torch.manual_seed(seed)
    embeds, pooled = compel(prompt)
    image = pipe(
        prompt_embeds=embeds,
        pooled_prompt_embeds=pooled,
        negative_prompt="low quality, text, watermark, flat lighting, oversaturated, bad anatomy",
        guidance_scale=args.guidance,
        num_inference_steps=args.steps,
        width=args.width,
        height=args.height,
    ).images[0]

    # 6) Sauvegarde
    if not args.out:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.out = f"SDXL_{args.mode}_{ts}.png"
    image.save(args.out)
    print("Image ->", args.out)


if __name__ == "__main__":
    main()
