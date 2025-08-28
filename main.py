# main.py
import argparse
from config.config import Config
from sources.steamGamessources import SteamGamesSource
from Extract.steamGamesExtract import Extractor
from transform.transform_clear import Transformer
from load.Load import Loader

def quick_quality_report(df):
    """Reporte sencillo de calidad de datos (impreso en consola)."""
    total = len(df)
    null_user = df["user_id"].isna().sum()
    null_game = df["game"].isna().sum()
    dup = df.duplicated().sum()
    actions = df["action"].value_counts(dropna=False).to_dict()

    lines = [
        f"Total filas: {total}",
        f"Nulos en user_id: {null_user}",
        f"Nulos en game: {null_game}",
        f"Duplicados exactos: {dup}",
        f"Distribución acciones: {actions}"
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="ETL para steam-200k")
    parser.add_argument("--input", "-i", default=Config.INPUT_FILE, help="CSV de entrada")
    parser.add_argument("--output", "-o", default=Config.OUTPUT_FILE, help="CSV de salida")
    parser.add_argument("--report", action="store_true", help="Imprime reporte QA del CSV limpio")
    args = parser.parse_args()

    # Source
    src = SteamGamesSource(csv_path=args.input)
    if not src.exists():
        raise FileNotFoundError(f"No se encontró la fuente: {args.input}")

    # Extract
    extractor = Extractor(csv_path=src.csv_path, columns=Config.DEFAULT_COLUMNS)
    df_raw = extractor.extract()
    print(f"[INFO] Filas extraídas: {len(df_raw)}")

    # Transform
    transformer = Transformer(valid_actions=Config.VALID_ACTIONS)
    df_clean = transformer.clean(df_raw)
    print(f"[INFO] Filas tras limpieza: {len(df_clean)}")

    # Load
    loader = Loader(out_path=args.output)
    out_path = loader.to_csv(df_clean)
    print(f"[OK] Guardado en: {out_path}")

    # Reporte QA
    if args.report:
        print("\n=== QA DEL CSV LIMPIO ===")
        print(quick_quality_report(df_clean))

if __name__ == "__main__":
    main()
