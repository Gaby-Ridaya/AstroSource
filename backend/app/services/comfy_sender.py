import os
import json
import requests
import os
import json
import requests
import time
from .image_selector import select_reference_images, create_moodboard


def send_to_comfy(prompt, sign, user_id, base_url="http://localhost:8188"):

    # 1. Sélectionner 4 images (une par type) pour le signe donné
    image_paths = select_reference_images([sign], count=4)
    if len(image_paths) < 2:
        raise RuntimeError("Pas assez d'images pour composer un moodboard.")

    # 2. Créer le moodboard
    output_dir = os.path.abspath("app/data")
    os.makedirs(output_dir, exist_ok=True)
    moodboard_path = os.path.join(output_dir, f"{user_id}_moodboard.png")
    create_moodboard(image_paths, moodboard_path)

    # 3. Charger le workflow
    workflow_path = os.path.abspath("resin/workflows/base_img2img_sdxl.workflow.json")
    if not os.path.exists(workflow_path):
        raise FileNotFoundError(f"Workflow non trouvé : {workflow_path}")

    with open(workflow_path, "r") as f:
        workflow = json.load(f)

    # Injecter le prompt texte et l'image
    for node in workflow["nodes"]:
        if node.get("class_type") == "CLIPTextEncode":
            node["inputs"]["text"] = prompt
        if node.get("class_type") == "LoadImage":
            node["inputs"]["image"] = moodboard_path

    # Envoyer le workflow
    try:
        response = requests.post(f"{base_url}/prompt", json=workflow)
        response.raise_for_status()
        data = response.json()
        prompt_id = data["prompt_id"]
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'envoi du workflow : {e}")

    # Attendre l'image générée
    output_filename = None
    for _ in range(30):
        try:
            history = requests.get(f"{base_url}/history/{prompt_id}").json()
            if "outputs" in history and history["outputs"]:
                output_filename = history["outputs"][0]["filename"]
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise TimeoutError("Image non générée à temps.")

    # Télécharger l’image depuis ComfyUI
    image_url = f"{base_url}/view?filename={output_filename}"
    try:
        image_data = requests.get(image_url).content
    except Exception as e:
        raise RuntimeError(f"Erreur lors du téléchargement de l'image : {e}")

    # Chemin absolu pour la sauvegarde
    output_dir = os.path.abspath("app/data")
    os.makedirs(output_dir, exist_ok=True)
    print(
        f"📂 Vérif dossier : output_dir = {output_dir} (existe: {os.path.exists(output_dir)})"
    )

    output_path = os.path.join(output_dir, f"{user_id}_output.png")
    print(f"💾 Image finale sera enregistrée ici : {output_path}")
    with open(output_path, "wb") as f:
        f.write(image_data)

    return output_path
