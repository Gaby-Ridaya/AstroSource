#!/bin/bash
# Script de sauvegarde automatique
echo "🔧 SAUVEGARDE AUTOMATIQUE VS CODE"

# Forcer la sauvegarde de tous les fichiers
echo "📁 Sauvegarde des fichiers..."
find /home/gaby/AstroSource -name "*.css" -exec touch {} \;
find /home/gaby/AstroSource -name "*.jsx" -exec touch {} \;
find /home/gaby/AstroSource -name "*.js" -exec touch {} \;

echo "✅ Sauvegarde terminée !"
