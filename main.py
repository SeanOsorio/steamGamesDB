# main.py (alternativo usando las clases)
from config.config import Config
from sources.steamGamessources import SteamGamesSource
from Extract.steamGamesExtract import Extractor
from transform.transform_clear import Transformer
from load.Load import Loader

def main():
    # Source
    src = SteamGamesSource.default()
    if not src.exists():
        raise FileNotFoundError(f"Fuente no encontrada: {src.csv_path}")

    # Extract
    extractor = Extractor(csv_path=src.csv_path, columns=Config.DEFAULT_COLUMNS)
    df_raw = extractor.extract()

    # Transform
    transformer = Transformer(valid_actions=Config.VALID_ACTIONS)
    df_clean = transformer.clean(df_raw)

    # Load
    loader = Loader(out_path=Config.OUTPUT_FILE)
    out_path = loader.to_csv(df_clean)
    print(f"[OK] Guardado CSV limpio en: {out_path}")

if __name__ == "__main__":
    main()
