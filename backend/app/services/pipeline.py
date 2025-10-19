# /home/gaby/AstroSource/backend/app/services/pipeline.py
import os, glob
from app.services.temp.openai_image_gen import run_from_json
from app.delivery.archiver import archive_results
from app.delivery.logger import log_generation


def process_user_theme(
    json_path: str | None = None, *, force_regen_prompt: bool = False
):
    # 1) Choix du JSON
    if not json_path:
        utilisateurs_dir = "/home/gaby/AstroSource/data/Utilisateurs"
        candidates = glob.glob(os.path.join(utilisateurs_dir, "*", "theme_*.json"))
        if not candidates:
            raise FileNotFoundError("[pipeline] Aucun fichier theme_*.json trouvé.")
        json_path = max(candidates, key=os.path.getmtime)

    # 2) Génération DALL·E 3
    result = run_from_json(
    json_path, size="1536x1024", force_regen_prompt=force_regen_prompt
)


    # 3) Archivage + logs
    user_dir = os.path.dirname(json_path)
    username = os.path.basename(user_dir)
    prompt_text = open(result["prompt_file"], "r", encoding="utf-8").read().strip()
    archive_results(username, json_path, result["image"], result["image"], prompt_text)
    log_generation(username, ["dalle3"], result["image"])

    return result
