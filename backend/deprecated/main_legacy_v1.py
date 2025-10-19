from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from websocket_manager import websocket_manager
from app.services.astro_calcule import generate_theme
from routers import etude_astro

load_dotenv()

app = FastAPI(title="AstroSource API Pro", version="2.0.0")

# Inclure les routers
app.include_router(etude_astro.router, prefix="/api", tags=["Étude Astrologique"])

# CORS pour autoriser le frontend React (localhost et 127.0.0.1)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*",  # Temporaire pour le développement
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket endpoint pour le Control Panel Pro
@app.websocket("/ws/control-panel")
async def websocket_control_panel(websocket: WebSocket):
    """WebSocket spécialement pour le Control Panel avec fonctionnalités avancées"""
    await manager.connect(websocket)

    try:
        # Envoyer le statut initial
        await websocket.send_text(
            json.dumps(
                {
                    "type": "server_status",
                    "status": "connected",
                    "timestamp": datetime.now().isoformat(),
                    "details": {
                        "connections": len(manager.active_connections),
                        "uptime": "00:00:00",  # TODO: calculer l'uptime réel
                        "version": "1.0.0",
                    },
                }
            )
        )

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "ping":
                await websocket.send_text(
                    json.dumps(
                        {"type": "pong", "timestamp": datetime.now().isoformat()}
                    )
                )
            elif message.get("type") == "get_status":
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "server_status",
                            "status": "running",
                            "timestamp": datetime.now().isoformat(),
                            "details": {
                                "connections": len(manager.active_connections),
                                "themes_generated": 0,  # TODO: compter les thèmes
                                "uptime": "00:00:00",
                            },
                        }
                    )
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/api/status")
async def get_status():
    """API pour récupérer le statut du serveur"""
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "connections": len(websocket_manager.active_connections),
        "version": "1.0.0",
        "uptime": "00:00:00",  # TODO: calculer l'uptime réel
    }


# Route pour le statut temps réel
@app.get("/api/status")
async def get_status():
    return {
        "status": "running",
        "connections": len(websocket_manager.active_connections),
        "timestamp": time.time(),
        "version": "2.0.0 Pro",
    }


# Route pour lister tous les fichiers générés
@app.get("/api/files")
async def list_generated_files():
    files_info = {}
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "Utilisateurs"
    )

    if os.path.exists(data_dir):
        for user_folder in os.listdir(data_dir):
            user_path = os.path.join(data_dir, user_folder)
            if os.path.isdir(user_path):
                files_info[user_folder] = []
                for file in os.listdir(user_path):
                    file_path = os.path.join(user_path, file)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        files_info[user_folder].append(
                            {
                                "name": file,
                                "path": file_path,
                                "size": stat.st_size,
                                "modified": stat.st_mtime,
                            }
                        )

    return files_info


# Route pour lister les images de la galerie AI
@app.get("/api/galerie-images")
async def list_galerie_images():
    images_info = {}
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, "data", "images")

    if os.path.exists(images_dir):
        for theme_folder in os.listdir(images_dir):
            theme_path = os.path.join(images_dir, theme_folder)
            if os.path.isdir(theme_path):
                images_info[theme_folder] = []
                for file in os.listdir(theme_path):
                    file_path = os.path.join(theme_path, file)
                    if os.path.isfile(file_path) and file.lower().endswith(
                        (".png", ".jpg", ".jpeg")
                    ):
                        stat = os.stat(file_path)
                        images_info[theme_folder].append(
                            {
                                "name": file,
                                "path": f"/api/images/{theme_folder}/{file}",
                                "size": stat.st_size,
                                "modified": stat.st_mtime,
                            }
                        )

    return images_info


# Route pour servir les images de la galerie
@app.get("/api/images/{theme}/{filename}")
async def serve_galerie_image(theme: str, filename: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(base_dir, "data", "images", theme, filename)
    print(f"Trying to serve image from: {image_path}")  # Debug
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": f"Image not found: {image_path}"}


# Inclusion des routes

import pathlib


# Route pour servir le favicon.ico du frontend/public côté backend
@app.get("/favicon.ico")
def favicon():
    favicon_path = (
        pathlib.Path(__file__).parent.parent / "frontend" / "public" / "favicon.ico"
    )
    if favicon_path.exists():
        return FileResponse(str(favicon_path), media_type="image/x-icon")
    return {"detail": "Favicon not found"}


# Route professionnelle pour servir les fichiers générés dans data/Utilisateurs/<Nom>/
from fastapi.responses import FileResponse
from fastapi import Query
import os


@app.get("/api/fichier")
def get_fichier(user: str = Query(...), filename: str = Query(...)):
    # Si user commence par 'images/', on sert depuis data/images
    if user.startswith("images/"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images_dir = os.path.join(base_dir, "data", "images")
        rel_path = user[7:]  # retire 'images/'
        file_path = os.path.join(images_dir, rel_path, filename)
        if not file_path.startswith(images_dir) or not os.path.isfile(file_path):
            return {"error": "Fichier non trouvé"}
        # Déterminer le type MIME approprié
        media_type = "image/svg+xml" if filename.endswith(".svg") else None
        return FileResponse(file_path, media_type=media_type)
    # Sinon, comportement standard (data/Utilisateurs)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    users_dir = os.path.join(base_dir, "data", "Utilisateurs")
    user_dir = os.path.join(users_dir, user.replace("..", ""))
    file_path = os.path.join(user_dir, filename)
    if not file_path.startswith(users_dir) or not os.path.isfile(file_path):
        return {"error": "Fichier non trouvé"}
    # Déterminer le type MIME approprié pour les fichiers SVG
    media_type = "image/svg+xml" if filename.endswith(".svg") else None
    return FileResponse(file_path, media_type=media_type)


# Route API simple pour générer uniquement le SVG du thème astral
from astro_calcule import generate_theme
from app.services.nouvelle_roue import AstroChartSVG
import json


@app.post("/api/generer-svg")
async def generer_svg_simple(request: Request):
    data = await request.json()
    nom = data.get("nom")
    date_naissance = data.get("date_naissance")
    heure_naissance = data.get("heure_naissance")
    ville_naissance = data.get("ville_naissance")
    pays = data.get("pays", "France")

    print(
        f"[API] Données reçues: nom={nom}, date={date_naissance}, heure={heure_naissance}, ville={ville_naissance}"
    )

    try:
        # Créer un nom de dossier sécurisé
        nom_dossier = nom.replace(" ", "_").replace("/", "_").replace("\\", "_")
        user_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "Utilisateurs",
            nom_dossier,
        )
        os.makedirs(user_dir, exist_ok=True)

        theme_json_path = os.path.join(user_dir, "theme_simple.json")

        # Générer le thème astral avec les bonnes données du formulaire
        print(f"[API] Génération du thème pour {nom}")

        # Notifier via WebSocket - Début génération
        await websocket_manager.notify_server_status(
            "generating", {"user": nom, "action": "theme_generation_started"}
        )

        generate_theme(
            nom, date_naissance, heure_naissance, ville_naissance, pays, theme_json_path
        )

        # Ajouter les couleurs des signes depuis theme_data.json
        theme_config_path = os.path.join(
            os.path.dirname(__file__), "..", "theme_data.json"
        )
        if os.path.exists(theme_config_path):
            with open(theme_config_path, "r", encoding="utf-8") as f:
                theme_config = json.load(f)
            if (
                "theme" in theme_config
                and "signs_glyphs_colors" in theme_config["theme"]
            ):
                # Lire le thème généré
                with open(theme_json_path, "r", encoding="utf-8") as f:
                    theme_data = json.load(f)
                # Ajouter les couleurs au niveau racine
                theme_data["signs_glyphs_colors"] = theme_config["theme"][
                    "signs_glyphs_colors"
                ]
                # Réécrire le fichier avec les couleurs
                with open(theme_json_path, "w", encoding="utf-8") as f:
                    json.dump(theme_data, f, ensure_ascii=False, indent=2)
                print(
                    f"[API] Couleurs des signes ajoutées: {list(theme_config['theme']['signs_glyphs_colors'].keys())}"
                )

        # Créer le SVG avec les couleurs
        svg_path = os.path.join(user_dir, "theme_simple.svg")
        print(f"[API] Création du SVG dans {svg_path}")
        chart = AstroChartSVG(svg_path, theme_json_path)
        chart.make_svg()

        # Lire le contenu SVG pour l'inclure dans la réponse
        svg_content = ""
        if os.path.exists(svg_path):
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            print(f"[API] SVG lu avec succès, taille: {len(svg_content)} caractères")

            # Ajouter un timestamp pour éviter le cache
            import time

            timestamp = str(int(time.time()))
            svg_content = svg_content.replace(
                "<svg", f'<svg data-timestamp="{timestamp}"'
            )

            # Vérifier que les couleurs sont présentes
            if 'fill="#ff0000"' in svg_content or 'fill="#00ff00"' in svg_content:
                print("[API] ✅ Couleurs détectées dans le SVG généré")
            else:
                print("[API] ⚠️ Aucune couleur détectée dans le SVG")

        # Notifier via WebSocket - Génération terminée
        await websocket_manager.notify_theme_generated(
            {"nom": nom, "ville": ville_naissance, "date": date_naissance},
            {
                "svg_file": f"Utilisateurs/{nom_dossier}/theme_simple.svg",
                "json_file": f"Utilisateurs/{nom_dossier}/theme_simple.json",
                "svg_size": len(svg_content),
            },
        )

        return {
            "message": f"Thème astral généré avec succès pour {nom}",
            "svg_file": f"Utilisateurs/{nom_dossier}/theme_simple.svg",
            "svg_content": svg_content,
            "timestamp": timestamp,
        }
    except Exception as e:
        print(f"[API] Erreur: {str(e)}")
        return {
            "message": f"Erreur lors de la génération: {str(e)}",
            "svg_content": "",
            "error": True,
        }


# Route API pour la galerie d'images classées par catégorie (data/images/<categorie>/<image>)
from fastapi import Response


@app.get("/api/galerie-categories")
def galerie_categories():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, "data", "images")
    galerie = {}
    if not os.path.isdir(images_dir):
        return galerie
    for categorie in os.listdir(images_dir):
        cat_path = os.path.join(images_dir, categorie)
        if os.path.isdir(cat_path):
            images = []
            for file in os.listdir(cat_path):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    # On encode le chemin pour la route /api/fichier
                    images.append(
                        f"/api/fichier?user=images/{categorie}&filename={file}"
                    )
            if images:
                galerie[categorie] = images
    return galerie


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API AstroSource!"}


# Sert le dossier images en statique sous /api/images/
images_path = os.path.abspath("data/images")
app.mount("/api/images", StaticFiles(directory=images_path), name="images")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
