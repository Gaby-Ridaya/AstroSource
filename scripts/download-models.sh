#!/bin/bash

echo "🤖 Script de téléchargement des modèles IA pour AstroSource"
echo "=================================================="

# Créer le dossier models s'il n'existe pas
mkdir -p models/ip_adapter/clip-vit-h

echo ""
echo "📋 Modèles requis pour AstroSource :"
echo "- SDXL Base Model (~6 GB)"
echo "- IP Adapter (~1.2 GB)"
echo "- ComfyUI Models (~200 MB)"
echo ""

read -p "🤔 Voulez-vous télécharger les modèles maintenant ? (y/N): " response

if [[ $response =~ ^[Yy]$ ]]; then
    echo ""
    echo "⬇️ Téléchargement en cours..."

    # Exemple - URLs à adapter selon vos modèles réels
    echo "📦 Téléchargement du modèle IP Adapter..."
    # wget -O models/ip_adapter/clip-vit-h/model.safetensors "URL_DU_MODELE"
    # wget -O models/ip_adapter/clip-vit-h/config.json "URL_DU_CONFIG"

    echo "📦 Téléchargement des modèles SDXL..."
    # wget -O models/sdxl_base.safetensors "URL_SDXL_BASE"

    echo "✅ Téléchargement terminé !"
    echo ""
    echo "🎯 Prochaines étapes :"
    echo "1. Vérifiez que ComfyUI est installé"
    echo "2. Lancez: ./start_astrosource.sh"
    echo "3. Ouvrez: http://localhost:5173"

else
    echo ""
    echo "ℹ️ Téléchargement annulé."
    echo ""
    echo "💡 Pour télécharger manuellement :"
    echo "1. Modèles SDXL: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"
    echo "2. IP Adapter: https://huggingface.co/h94/IP-Adapter"
    echo "3. Placez les fichiers dans le dossier models/"
    echo ""
    echo "🚀 AstroSource peut fonctionner sans IA en mode démonstration"
fi

echo ""
echo "📚 Documentation complète: README.md"
echo "🐛 Problèmes: https://github.com/Gaby-Ridaya/AstroSource/issues"
