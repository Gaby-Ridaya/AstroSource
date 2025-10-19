import openai
import os
from dotenv import load_dotenv
from fusion_complte import create_final_prompt
import sys

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_image_astrologique(prompt, taille="1024x1024"):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=taille,
            quality="standard",
            n=1,
            response_format="url"
        )
        return response.data[0].url
    except Exception as e:
        print("❌ Erreur lors de la génération de l'image :", e)
        print("Vérifie ta connexion internet, ta clé API, ou le contenu du prompt.")
        return None

if __name__ == "__main__":
    prompt_final = "Theme test sans accent"

    image_url = generer_image_astrologique(prompt_final)
    if image_url:
        print("🎉 Image disponible ici :", image_url)
    else:
        print("Aucune image n'a pu être générée. Merci de vérifier les messages d'erreur ci-dessus.")
