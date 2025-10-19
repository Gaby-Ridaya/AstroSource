"""
Configuration du système de logging pour AstroSource
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging() -> logging.Logger:
    """
    Configure le système de logging pour l'application

    Returns:
        Logger configuré
    """
    # Configuration du format de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configuration du niveau de log
    log_level = logging.INFO

    # Configuration du handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)

    # Configuration du handler fichier (si possible)
    try:
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "astrosource.log"

        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10 MB
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)
    except Exception:
        file_handler = None

    # Configuration du logger racine
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Éviter la duplication des handlers
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        if file_handler:
            root_logger.addHandler(file_handler)

    # Logger spécifique pour AstroSource
    logger = logging.getLogger("astrosource")
    logger.setLevel(log_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Récupère un logger avec le nom spécifié"""
    return logging.getLogger(f"astrosource.{name}")


import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging() -> logging.Logger:
    """
    Configure le système de logging pour l'application

    Returns:
        Logger configuré
    """
    # Configuration du format de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configuration du niveau de log
    log_level = logging.INFO

    # Configuration du handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)

    # Configuration du handler fichier (si possible)
    try:
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "astrosource.log"

        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10 MB
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)
    except Exception:
        file_handler = None

    # Configuration du logger racine
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Éviter la duplication des handlers
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        if file_handler:
            root_logger.addHandler(file_handler)

    # Logger spécifique pour AstroSource
    logger = logging.getLogger("astrosource")
    logger.setLevel(log_level)

    return logger
    logger = logging.getLogger(name)

    # Éviter la duplication si déjà configuré
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)

    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Handler pour fichier avec rotation
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        log_dir / "astrosource.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Handler pour les erreurs
    error_handler = RotatingFileHandler(
        log_dir / "errors.log", maxBytes=5 * 1024 * 1024, backupCount=3  # 5MB
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    # Ajouter les handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger


# Logger principal de l'application
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """Récupère un logger enfant avec le nom spécifié"""
    return logger.getChild(name)
