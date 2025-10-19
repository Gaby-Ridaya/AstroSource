# 🚀 AstroSource - Démarrage Automatique

## ✅ Configuration VS Code terminée !

Votre projet est maintenant configuré pour démarrer automatiquement le backend et le frontend.

## 🎯 Comment utiliser :

### **Option 1 : Démarrage automatique complet**

```bash
./auto-start.sh
```

Lance backend + frontend + Chromium automatiquement

### **Option 2 : Démarrage manuel séparé**

```bash
# Terminal 1 - Backend
source Boogy/bin/activate && cd backend && python main.py

# Terminal 2 - Frontend
cd frontend && npm run dev

# Terminal 3 - Chromium
./start-chrome.sh
```

### **Option 3 : Via VS Code**

- Utilisez les tâches VS Code configurées
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Choisir "🚀 Start Backend" ou "🎨 Start Frontend"

## 🔧 Problème actuel à résoudre :

Le backend a un problème d'import :

```
ImportError: cannot import name 'generate_theme' from 'astro_calcule'
```

### **Solutions possibles :**

1. **Vérifier les imports dans `backend/main.py`**
2. **Utiliser le backend professionnel migré**
3. **Corriger la fonction manquante dans `astro_calcule.py`**

## 📁 Fichiers configurés :

- ✅ `.vscode/tasks.json` - Tâches automatiques
- ✅ `.vscode/launch.json` - Configurations de démarrage
- ✅ `auto-start.sh` - Script de démarrage complet
- ✅ `start-chrome.sh` - Ouverture Chromium optimisée

## 🌐 URLs une fois démarré :

- **Frontend** : http://localhost:5173/
- **Backend** : http://localhost:8000/
- **Navigation** : Toutes les pages disponibles via le menu

---

_Une fois le problème d'import résolu, tout démarrera automatiquement !_ 🎉
