# 🚨 Guide : Repository trop volumineux pour GitHub

## 💡 Le problème

Votre projet AstroSource fait **11 GB**, mais GitHub limite à :

- **100 MB** par fichier
- **1 GB** recommandé par repository
- **Timeout** si push > 2 GB

## 📊 Répartition actuelle

- `Boogy/` : 7.4 GB (environnement Python)
- `models/` : 2.4 GB (modèles IA)
- `resin/` : 108 MB (images)
- Code source : ~200 MB

## ✅ Solutions

### Option 1 : Repository léger (RECOMMANDÉ)

Créer une version GitHub avec uniquement le code source :

```bash
# 1. Sauvegarder le projet complet
cp -r AstroSource AstroSource-COMPLET

# 2. Créer version GitHub allégée
mkdir AstroSource-GitHub
cd AstroSource-GitHub

# 3. Copier seulement les fichiers essentiels
cp -r ../AstroSource/frontend .
cp -r ../AstroSource/backend .
cp -r ../AstroSource/docs .
cp ../AstroSource/*.md .
cp ../AstroSource/LICENSE .
cp ../AstroSource/.gitignore .
cp -r ../AstroSource/scripts .

# 4. Quelques exemples d'images (pas toutes)
mkdir -p data/images/examples
cp ../AstroSource/data/images/*/exemple_*.png data/images/examples/ 2>/dev/null || true

# 5. Initialiser Git propre
git init
git add .
git commit -m "🎨 Initial commit: AstroSource - Code source optimisé GitHub"
git branch -M main
git remote add origin https://github.com/Gaby-Ridaya/AstroSource.git
git push -u origin main
```

### Option 2 : Git LFS pour gros fichiers

```bash
# Installer Git LFS
git lfs install
git lfs track "*.safetensors"
git lfs track "*.ckpt"
git lfs track "models/**"
git add .gitattributes
git commit -m "Configure Git LFS"
```

### Option 3 : Plusieurs repositories

- `AstroSource` : Code source principal
- `AstroSource-Models` : Modèles IA
- `AstroSource-Assets` : Images et ressources

## 🎯 Recommandation

**Utilisez l'Option 1** - Repository léger avec :

- ✅ Code source complet
- ✅ Documentation
- ✅ Quelques images d'exemple
- ✅ Scripts d'installation
- ❌ Pas de modèles IA volumineux
- ❌ Pas d'environnements Python

## 📝 Instructions dans le README

Ajoutez dans votre README :

````markdown
## 📦 Installation des modèles IA

Les modèles IA ne sont pas inclus dans ce repository pour des raisons de taille.

### Installation automatique :

```bash
./scripts/download-models.sh
```
````

### Installation manuelle :

1. Télécharger les modèles depuis [releases](../../releases)
2. Les placer dans le dossier `models/`

```

Voulez-vous que je vous aide à créer cette version allégée ?
```
