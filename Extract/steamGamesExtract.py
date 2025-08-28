# Extract/steamGamesExtract.py
import pandas as pd
from typing import List
from pathlib import Path

class Extractor:
    """
    Lee el CSV de steam-200k en un DataFrame.
    - Soporta archivos sin encabezado (común en este dataset)
    - dtype=str para evitar cast accidentales
    - on_bad_lines='skip' para saltar líneas corruptas
    """

    def __init__(self, csv_path: Path, columns: List[str]):
        self.csv_path = Path(csv_path)
        self.columns = columns

    def extract(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.csv_path}")

        try:
            # Intento 1: sin encabezado, tipos como str, saltando líneas malas
            df = pd.read_csv(
                self.csv_path,
                header=None,
                dtype=str,
                on_bad_lines="skip"
            )
            if len(df.columns) == len(self.columns):
                df.columns = self.columns
            elif len(df.columns) == 4 and len(self.columns) == 5:
                df.columns = self.columns[:4]
                df["value"] = pd.NA
            else:
                # Intento 2: con encabezado y alineación a columnas esperadas
                df2 = pd.read_csv(self.csv_path, dtype=str, on_bad_lines="skip")
                for c in self.columns:
                    if c not in df2.columns:
                        df2[c] = pd.NA
                df = df2[self.columns]
        except Exception:
            # Último intento: leer normal y alinear
            df = pd.read_csv(self.csv_path, dtype=str, on_bad_lines="skip")
            for c in self.columns:
                if c not in df.columns:
                    df[c] = pd.NA
            df = df[self.columns]

        return df
