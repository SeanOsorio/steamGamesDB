# sources/steamGamessources.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os

@dataclass
class SteamGamesSource:
    """
    Localiza y valida la fuente steam-200k.csv.
    """
    csv_path: Path

    @classmethod
    def default(cls) -> "SteamGamesSource":
        # Import local para evitar dependencia circular si config importa esto
        from config.config import Config
        return cls(csv_path=Config.INPUT_FILE)

    def exists(self) -> bool:
        return self.csv_path.exists() and self.csv_path.is_file()

    def size_bytes(self) -> Optional[int]:
        try:
            return os.path.getsize(self.csv_path)
        except OSError:
            return None
