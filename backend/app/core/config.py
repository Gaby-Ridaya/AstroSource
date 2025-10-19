"""
Configuration principale pour AstroSource Backend
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application avec validation Pydantic"""

    # Configuration API
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True

    # Chemins - backend/app/core/config.py -> /home/gaby/AstroSource/backend -> /home/gaby/AstroSource
    BASE_DIR: Path = Path(
        __file__
    ).parent.parent.parent  # /home/gaby/AstroSource/backend
    PROJECT_ROOT: Path = BASE_DIR.parent  # /home/gaby/AstroSource
    DATA_DIR: Path = PROJECT_ROOT / "data"  # /home/gaby/AstroSource/data
    TEMP_DIR: Path = BASE_DIR / "temp"
    SVG_OUTPUT_DIR: Path = DATA_DIR / "roue.svg"
    INTERPRETATIONS_DIR: Path = DATA_DIR / "interpretations_json"

    # Sécurité
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = BASE_DIR / "logs" / "astrosource.log"

    # CORS
    FRONTEND_URL: str = "http://localhost:5174"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def validate_paths(self):
        """Valide que tous les chemins requis existent"""
        required_paths = [
            self.DATA_DIR,
            self.INTERPRETATIONS_DIR,
        ]

        missing_paths = []
        for path in required_paths:
            if not path.exists():
                missing_paths.append(str(path))

        if missing_paths:
            paths_str = ", ".join(missing_paths)
            raise FileNotFoundError(f"Chemin requis manquant: {paths_str}")

        # Créer les dossiers temporaires si nécessaire
        self.TEMP_DIR.mkdir(exist_ok=True)
        self.SVG_OUTPUT_DIR.mkdir(exist_ok=True)
        self.LOG_FILE.parent.mkdir(exist_ok=True)


# Instance globale des paramètres
settings = Settings()

# Auto-validation à l'import
try:
    settings.validate_paths()
except FileNotFoundError as e:
    print(f"⚠️  Attention: {e}")
