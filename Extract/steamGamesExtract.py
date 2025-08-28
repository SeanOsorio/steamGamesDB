# Extract/steamGamesExtract.py
import pandas as pd
from typing import List
from pathlib import Path

class Extractor:
    """
    Lee el CSV de steam-200k en un DataFrame.
    Soporta archivos sin encabezado (común en este dataset).
    """

    def __init__(self, csv_path: Path, columns: List[str]):
        self.csv_path = Path(csv_path)
        self.columns = columns

    def extract(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.csv_path}")

        # Intentar con header None y asignar columnas por defecto (muchos dumps vienen sin encabezado)
        try:
            df = pd.read_csv(self.csv_path, header=None)
            # Si el número de columnas coincide, renombrar
            if len(df.columns) == len(self.columns):
                df.columns = self.columns
            # Si trae 4 columnas, completa 'value' como NaN
            elif len(df.columns) == 4 and len(self.columns) == 5:
                df.columns = self.columns[:4]
                df["value"] = pd.NA
            else:
                # Si por alguna razón ya trae encabezados correctos, reintenta leyendo con header=0
                df2 = pd.read_csv(self.csv_path)
                df = df2
                # Asegura columnas esperadas si están presentes
                for c in self.columns:
                    if c not in df.columns:
                        df[c] = pd.NA
                df = df[self.columns]
        except Exception:
            # Último intento: leer normal y alinear columnas
            df = pd.read_csv(self.csv_path)
            for c in self.columns:
                if c not in df.columns:
                    df[c] = pd.NA
            df = df[self.columns]

        return df
