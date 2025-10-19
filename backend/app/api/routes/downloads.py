# app/api/routes/downloads.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/api", tags=["downloads"])

BASE_DIR = "/home/gaby/AstroSource/data/Utilisateurs"


def _paths_for_user(user: str):
    # Construit les chemins attendus
    user_dir = os.path.join(BASE_DIR, user)
    stem = f"theme_{user}"
    return {
        "pack": os.path.join(user_dir, f"{stem}_pack.zip"),
        "image": os.path.join(user_dir, f"{stem}_image.png"),
        "interpretations": os.path.join(user_dir, f"{stem}_interpretations.txt"),
        "pdf": os.path.join(user_dir, f"{stem}_interpretations.pdf"),  # <--- nouveau
        "svg": os.path.join(user_dir, f"{stem}.svg"),
    }


@router.get("/download/{user}/{kind}")
def download(user: str, kind: str):
    paths = _paths_for_user(user)
    if kind not in paths:
        raise HTTPException(status_code=404, detail="Type de fichier inconnu")
    path = paths[kind]
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    filename = os.path.basename(path)
    return FileResponse(path, filename=filename)
