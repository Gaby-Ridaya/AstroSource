from fastapi import APIRouter, HTTPException
import json
import os
from pathlib import Path

router = APIRouter()

# Chemin vers les données d'interprétation
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "interpretations_json"
SVG_PATH = Path(__file__).parent.parent.parent / "frontend" / "public" / "data" / "svg"


@router.get("/interpretations/planets")
async def get_planets_interpretations():
    """Récupère les interprétations des planètes"""
    try:
        planets_file = DATA_PATH / "planets.json"
        if planets_file.exists():
            with open(planets_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        else:
            return {}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du chargement des planètes: {str(e)}"
        )


@router.get("/interpretations/houses")
async def get_houses_interpretations():
    """Récupère les interprétations des maisons"""
    try:
        houses_file = DATA_PATH / "houses.json"
        if houses_file.exists():
            with open(houses_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        else:
            return {}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du chargement des maisons: {str(e)}"
        )


@router.get("/celebrities")
async def get_celebrities():
    """Récupère la liste des célébrités avec leurs SVG"""
    try:
        celebrities = []

        # Vérifier si le dossier SVG existe
        if SVG_PATH.exists():
            # Parcourir tous les fichiers SVG
            for svg_file in SVG_PATH.glob("*.svg"):
                celebrity_name = svg_file.stem.replace("_", " ").title()
                celebrities.append(
                    {
                        "name": celebrity_name,
                        "svgPath": f"/data/svg/{svg_file.name}",
                        "fileName": svg_file.name,
                    }
                )

        # Trier par nom
        celebrities.sort(key=lambda x: x["name"])

        return celebrities

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du chargement des célébrités: {str(e)}",
        )


@router.get("/celebrity/{filename}")
async def get_celebrity_svg(filename: str):
    """Récupère le SVG d'une célébrité spécifique"""
    try:
        svg_file = SVG_PATH / filename
        if svg_file.exists():
            with open(svg_file, "r", encoding="utf-8") as f:
                svg_content = f.read()
            return {"svg_content": svg_content}
        else:
            raise HTTPException(status_code=404, detail="Fichier SVG non trouvé")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du chargement du SVG: {str(e)}"
        )
