# config/config.py
from pathlib import Path

class Config:
    """
    Configuración central del proyecto.
    Ajusta rutas si cambias la estructura.
    """
    # Raíz del proyecto (ajústala si no coincide)
    ROOT = Path("/workspaces/steamGamesDB").resolve()

    # Rutas de entrada/salida
    SOURCES_DIR = ROOT / "sources"
    INPUT_FILE = SOURCES_DIR / "steam-200k.csv"
    OUTPUT_FILE = SOURCES_DIR / "steam-200k.cleaned.csv"

    # Parámetros de transformación
    # Filtrar por acciones válidas del dataset steam-200k
    VALID_ACTIONS = {"play", "purchase"}  # puedes ajustar

    # Columnas esperadas (el CSV suele traer 4 o 5 columnas sin header)
    # user_id, game, action, hours, value(optional)
    DEFAULT_COLUMNS = ["user_id", "game", "action", "hours", "value"]
