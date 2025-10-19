# README – Installation et configuration AstroSource (local GPU)

## Prérequis matériels

- Carte graphique NVIDIA compatible CUDA (ex : RTX 3050)
- Au moins 8 Go de RAM recommandés

## Environnement logiciel

- OS : Linux (testé sur Ubuntu)
- Python 3.11 (utilisation d’un venv nommé Boogy)
- Drivers NVIDIA à jour (testé avec CUDA 12.8)

# (ComfyUI n'est plus utilisé)

- AstroSource (ton projet principal)

## Étapes d’installation

### 1. Drivers NVIDIA et CUDA

- Vérifier l’installation :
  ```bash
  nvidia-smi
  # Doit afficher ta carte et la version CUDA
  ```
- (Optionnel) Installer le toolkit CUDA :
  ```bash
  sudo apt install nvidia-cuda-toolkit
  ```

### 2. Environnement Python

- Créer et activer un venv Python 3.11 :
  ```bash
  python3.11 -m venv ~/AstroSource/Boogy
  source ~/AstroSource/Boogy/bin/activate
  ```
- Installer les dépendances AstroSource :
  ```bash
  pip install -r requirements.txt
  ```

# ComfyUI n'est plus utilisé dans ce projet.

```bash
python main.py
# Interface sur http://localhost:8188
```

### 5. Utilisation avec AstroSource

- Modifier l’URL dans `comfy_sender.py` :
  ```python
  base_url="http://localhost:8188"
  ```
- Lancer tes scripts AstroSource en ajoutant le PYTHONPATH :
  ```bash
  cd ~/AstroSource
  PYTHONPATH=backend python test_comfy_sender.py
  ```

### 6. Exporter un workflow compatible

- Créer un workflow dans l’UI ComfyUI
- Exporter via le bouton "Save (Export)"
- Remplacer le fichier `resin/workflows/base_img2img_sdxl.workflow.json` par ce nouveau fichier

---

## Résumé des commandes utiles

- Activer le venv :
  ```bash
  source ~/AstroSource/Boogy/bin/activate
  ```
- Lancer ComfyUI :
  ```bash
  cd ~/ComfyUI && python main.py
  ```
- Lancer un script AstroSource :
  ```bash
  cd ~/AstroSource
  PYTHONPATH=backend python test_comfy_sender.py
  ```

---

## Notes

- Les images générées sont enregistrées dans `app/data/`.
- Pour ajouter d’autres modèles à ComfyUI, voir la documentation officielle.
- Pour déboguer, vérifier les logs dans le terminal ComfyUI et dans AstroSource.

---

**Dernière mise à jour : 07/08/2025**
