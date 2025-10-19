import openai

openai.api_key = "TA_CLÉ_API_OPENAI"

def generer_image_astrologique(prompt, taille="1024x1024"):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size=taille,
            quality="standard",
            n=1,
        )
        image_url = response['data'][0]['url']
        print("✅ Image générée avec succès:", image_url)
        return image_url

    except Exception as e:
        print("⚠️ Erreur lors de la génération d'image :", e)
        return None

# Exemple d'utilisation :
if __name__ == "__main__":
    with open("/home/gaby/AstroSource/data/Gaby/prompt_final.txt", "r", encoding="utf-8") as f:
        prompt_final = f.read()
    
    generer_image_astrologique(prompt_final)
