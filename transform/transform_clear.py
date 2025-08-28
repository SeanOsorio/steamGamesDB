# transform/transform_clear.py
import pandas as pd
from typing import Optional, Iterable

class Transformer:
    """
    Limpieza mínima para steam-200k:
    - Normaliza nombres de columnas y tipos
    - Recorta espacios, pone minúsculas en 'action'
    - Convierte 'hours' a numérico
    - Filtra acciones válidas (play/purchase por defecto)
    - Elimina duplicados y filas vacías críticas
    """

    def __init__(self, df: Optional[pd.DataFrame] = None,
                 valid_actions: Optional[Iterable[str]] = None):
        # Import local para evitar dependencias cíclicas
        try:
            from config.config import Config
            self.valid_actions = set(valid_actions or Config.VALID_ACTIONS)
        except Exception:
            self.valid_actions = set(valid_actions or {"play", "purchase"})

        self.df = df

    def _prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        # Alinear columnas esperadas si faltan
        expected = ["user_id", "game", "action", "hours", "value"]
        for c in expected:
            if c not in df.columns:
                df[c] = pd.NA
        return df[expected]

    def clean(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if df is None:
            if self.df is None:
                raise ValueError("No se recibió DataFrame para limpiar.")
            df = self.df

        df = self._prepare(df).copy()

        # Normalizaciones
        df["user_id"] = df["user_id"].astype(str).str.strip()
        df["game"] = df["game"].astype(str).str.strip()

        # Acción a minúsculas y sin espacios
        df["action"] = df["action"].astype(str).str.strip().str.lower()

        # Horas a numérico
        df["hours"] = pd.to_numeric(df["hours"], errors="coerce")

        # value a numérico si existe (algunos dumps tienen 0/1 o NaN)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        # Filtrar acciones válidas si aplica
        if self.valid_actions:
            df = df[df["action"].isin(self.valid_actions)]

        # Eliminar filas con user_id o game vacíos
        df = df.dropna(subset=["user_id", "game"]).copy()

        # Duplicados exactos
        df = df.drop_duplicates()

        # Índice limpio
        df = df.reset_index(drop=True)
        return df

    # Alias por compatibilidad con main.py flexible
    def transform(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        return self.clean(df)

    def run(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        return self.clean(df)
