# transform/transform_clear.py
import pandas as pd
from typing import Optional, Iterable

class Transformer:
    """
    Limpieza para steam-200k:
    - Normaliza columnas y tipos
    - action en minúsculas + sinónimos comunes
    - hours/value a numérico
    - Filtra acciones válidas
    - hours >= 0
    - Elimina duplicados y nulos críticos
    """

    def __init__(self, df: Optional[pd.DataFrame] = None,
                 valid_actions: Optional[Iterable[str]] = None):
        try:
            from config.config import Config
            self.valid_actions = set(valid_actions or Config.VALID_ACTIONS)
        except Exception:
            self.valid_actions = set(valid_actions or {"play", "purchase"})
        self.df = df

    def _prepare(self, df: pd.DataFrame) -> pd.DataFrame:
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

        # Normalizar
        df["user_id"] = df["user_id"].astype(str).str.strip()
        df["game"]    = df["game"].astype(str).str.strip()
        df["action"]  = df["action"].astype(str).str.strip().str.lower()

        # 🔹 Normalización de sinónimos
        action_map = {
            "played": "play",
            "playtime": "play",
            "buy": "purchase",
            "bought": "purchase",
            "purchased": "purchase"
        }
        df["action"] = df["action"].replace(action_map)

        df["hours"] = pd.to_numeric(df["hours"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        # Filtrar acciones válidas
        if self.valid_actions:
            df = df[df["action"].isin(self.valid_actions)]

        # Eliminar filas inválidas
        df = df.dropna(subset=["user_id", "game"]).copy()
        df["hours"] = df["hours"].fillna(0)
        df = df[df["hours"] >= 0]

        # Duplicados
        df = df.drop_duplicates().reset_index(drop=True)
        return df

    # Alias
    def transform(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        return self.clean(df)

    def run(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        return self.clean(df)
