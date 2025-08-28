# load/Load.py
import pandas as pd
from pathlib import Path

class Loader:
    """
    Escribe el DataFrame a CSV (y opcionalmente a Parquet).
    """

    def __init__(self, out_path: Path):
        self.out_path = Path(out_path)

    def to_csv(self, df: pd.DataFrame, index: bool = False) -> Path:
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.out_path, index=index)
        return self.out_path

    def to_parquet(self, df: pd.DataFrame, compression: str = "snappy") -> Path:
        """
        Requiere 'pyarrow' o 'fastparquet' si quieres exportar parquet.
        """
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        parquet_path = self.out_path.with_suffix(".parquet")
        df.to_parquet(parquet_path, compression=compression, index=False)
        return parquet_path
