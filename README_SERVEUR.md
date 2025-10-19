# AstroSource — Démarrage et Arrêt du Serveur

## Démarrer l'application

Pour lancer le backend, le frontend et Chromium :

```bash
./start_astrosource.sh
```

- Le backend (API) démarre sur le port 8000.
- Le frontend démarre sur le port 5173.
- Chromium s'ouvre automatiquement sur l'interface utilisateur.

## Arrêter l'application

Pour arrêter tous les services AstroSource (backend, frontend, Chromium) :

```bash
./stop_astrosource.sh
```

- Le backend est stoppé (port 8000 libéré).
- Le frontend (Vite/npm) est stoppé.
- Chromium est fermé.

## Conseils

- Aucun service ne se lance automatiquement à l'ouverture de VS Code.
- Utilisez ces scripts pour garder le contrôle total sur le démarrage et l'arrêt de votre application.
- Si un port est occupé, relancez le script d'arrêt puis le script de démarrage.

---

AstroSource — Workflow professionnel, simple et efficace.
