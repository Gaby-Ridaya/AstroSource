from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.pipeline import process_user_theme
import os

router = APIRouter()


# Route POST existante conservée
@router.post("/generate-astro-image/")
async def generate_astro_image(theme_json: UploadFile = File(...)):
    temp_path = f"temp_{theme_json.filename}"
    with open(temp_path, "wb") as f:
        f.write(await theme_json.read())
    result = process_user_theme(temp_path)
    return {
        "user_id": result["user_id"],
        "signs": result["signs"],
        "prompt": result["prompt"],
        "image": result["image"],
        "moodboard": result["moodboard"],
    }


# Nouvelle route GET pour générer et servir l'image à partir du nom utilisateur
@router.get("/astro-image/{username}")
async def get_astro_image(username: str):
    # Chemin du JSON utilisateur
    json_path = (
        f"/home/gaby/AstroSource/data/Utilisateurs/{username}/theme_{username}.json"
    )
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="JSON utilisateur non trouvé")

    # Générer l'image (ou la retrouver si déjà générée)
    result = process_user_theme(json_path)
    image_path = result["image"]
    if not os.path.exists(image_path):
        raise HTTPException(status_code=500, detail="Image non générée")

    def iterfile():
        with open(image_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="image/png")
