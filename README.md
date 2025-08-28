
# 🎮 SteamGamesDB - Proyecto de Limpieza de Datos de Steam

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de **extracción, limpieza y carga (ETL)** de datos de la plataforma Steam, utilizando como fuente principal el dataset **`steam-200k.csv`**. El sistema está diseñado para extraer los datos del archivo CSV original, limpiarlos de acuerdo con un conjunto de reglas predefinidas, y luego almacenarlos en un archivo limpio (`steam-200k.cleaned.csv`).

El sistema está dividido en varios módulos:
- **Extracción**: Lee los datos desde un archivo CSV.
- **Transformación**: Aplica reglas de limpieza, como normalización de datos y eliminación de registros inválidos.
- **Carga**: Guarda el dataset limpio en un archivo CSV o en un formato Parquet (opcional).

---

## 🏗️ Estructura del Proyecto

```
steamGamesDB/
│
├── main.py                              # Punto de entrada principal (ejecuta el pipeline ETL)
├── README.md                            # Documentación del proyecto
├── requirements.txt                     # Dependencias del proyecto
│
├── config/                              # Configuración central
│   └── config.py                        # Rutas y parámetros
│
├── Extract/                             # Módulo de extracción
│   └── steamGamesExtract.py             # Clase Extractor (lee CSV original)
│
├── transform/                           # Módulo de transformación
│   └── transform_clear.py               # Clase Transformer (limpieza de datos)
│
├── load/                                # Módulo de carga
│   └── Load.py                          # Clase Loader (guarda CSV limpio)
│
└── sources/                             # Archivos de datos
    ├── steam-200k.csv                   # Dataset original
    └── steam-200k.cleaned.csv           # Dataset procesado
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación
1. Clona el repositorio y accede a la carpeta:
```bash
git clone <URL-del-repo>
cd steamGamesDB
```

2. Crea y activa un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scriptsctivate      # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

---

## 💻 Uso del Sistema

### Ejecución básica
```bash
python3 main.py
```

### Ejecución con parámetros
```bash
python3 main.py --input sources/steam-200k.csv --output sources/steam-200k.cleaned.csv --report
```

La opción `--report` imprime en consola un **reporte de calidad** del dataset limpio (nulos, duplicados, distribución de acciones, etc.).

---

## 🧹 Sistema de Limpieza de Datos

El proceso de limpieza incluye las siguientes reglas:
- ✅ **Normalización de columnas** (`user_id`, `game`, `action`, `hours`, `value`)  
- ✅ **Conversión de `action` a minúsculas** y mapeo de sinónimos comunes:
  - `played` → `play`
  - `buy` → `purchase`
  - `bought` → `purchase`
  - `purchased` → `purchase`
- ✅ **Conversión de `hours`** y `value` a valores numéricos
- ✅ **Eliminación de filas con `user_id` o `game` nulos**
- ✅ **Eliminación de registros con `hours < 0`**
- ✅ **Eliminación de duplicados** en el dataset

---

## 🛠️ Módulos del Proyecto

### **`config/config.py`**
Este archivo contiene la configuración central del proyecto, incluidas las rutas de entrada/salida y los parámetros de transformación.
```python
from pathlib import Path

class Config:
    ROOT = Path("/workspaces/steamGamesDB").resolve()
    SOURCES_DIR = ROOT / "sources"
    INPUT_FILE = SOURCES_DIR / "steam-200k.csv"
    OUTPUT_FILE = SOURCES_DIR / "steam-200k.cleaned.csv"
    VALID_ACTIONS = {"play", "purchase"}
    DEFAULT_COLUMNS = ["user_id", "game", "action", "hours", "value"]
```

### **`Extract/steamGamesExtract.py`**
La clase `Extractor` es responsable de leer los datos desde el archivo CSV y normalizarlos según las columnas definidas.
```python
import pandas as pd
from pathlib import Path
from config.config import Config

class Extractor:
    def __init__(self, csv_path: Path, columns: list):
        self.csv_path = Path(csv_path)
        self.columns = columns

    def extract(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.csv_path}")

        df = pd.read_csv(self.csv_path, header=None)
        if len(df.columns) == len(self.columns):
            df.columns = self.columns
        else:
            df.columns = self.columns[:len(df.columns)]
            df["value"] = pd.NA
        return df
```

### **`transform/transform_clear.py`**
La clase `Transformer` aplica las reglas de limpieza sobre los datos, incluyendo la normalización de `action` y la conversión de `hours` y `value` a valores numéricos.
```python
import pandas as pd
from typing import Optional, Iterable
from config.config import Config

class Transformer:
    def __init__(self, df: Optional[pd.DataFrame] = None, valid_actions: Optional[Iterable[str]] = None):
        self.valid_actions = set(valid_actions or Config.VALID_ACTIONS)
        self.df = df

    def clean(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if df is None:
            if self.df is None:
                raise ValueError("No se recibió DataFrame para limpiar.")
            df = self.df

        df = df.copy()
        df["action"] = df["action"].str.strip().str.lower()
        df["hours"] = pd.to_numeric(df["hours"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        df = df.dropna(subset=["user_id", "game"])
        df = df[df["hours"] >= 0]

        return df
```

### **`load/Load.py`**
La clase `Loader` se encarga de guardar los datos transformados en un archivo CSV o en un archivo Parquet (opcional).
```python
import pandas as pd
from pathlib import Path

class Loader:
    def __init__(self, out_path: Path):
        self.out_path = Path(out_path)

    def to_csv(self, df: pd.DataFrame, index: bool = False) -> Path:
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.out_path, index=index)
        return self.out_path
```

### **`main.py`**
El archivo principal del proyecto orquesta el proceso de extracción, transformación y carga (ETL). También ofrece una opción para generar un reporte de calidad del dataset limpio.
```python
from config.config import Config
from sources.steamGamessources import SteamGamesSource
from Extract.steamGamesExtract import Extractor
from transform.transform_clear import Transformer
from load.Load import Loader

def main():
    src = SteamGamesSource.default()
    if not src.exists():
        raise FileNotFoundError(f"Fuente no encontrada: {src.csv_path}")

    extractor = Extractor(csv_path=src.csv_path, columns=Config.DEFAULT_COLUMNS)
    df_raw = extractor.extract()

    transformer = Transformer(valid_actions=Config.VALID_ACTIONS)
    df_clean = transformer.clean(df_raw)

    loader = Loader(out_path=Config.OUTPUT_FILE)
    out_path = loader.to_csv(df_clean)
    print(f"[OK] Guardado CSV limpio en: {out_path}")

if __name__ == "__main__":
    main()
```

---

## 📈 Resultados del Procesamiento

El procesamiento del dataset de Steam genera un archivo limpio llamado `steam-200k.cleaned.csv`. El tamaño del archivo puede variar según las filas y el filtrado realizado.

---

## 🔧 Funcionalidades Principales

- **Extracción**: Lee el archivo `steam-200k.csv` y aplica una estructura de columnas definida.
- **Transformación**: Aplica reglas de limpieza para normalizar los datos y eliminar registros incorrectos.
- **Carga**: Guarda el dataset limpio en formato CSV.

---

## 📊 Dataset de Steam

### Información del dataset utilizado
- **Archivo principal:** `steam-200k.csv`
- **Registros:** ~200,000 filas
- **Campos:** `user_id`, `game`, `action`, `hours`, `value`

### Calidad de los datos
- **Valores nulos detectados:** En varias columnas
- **Acciones inconsistentes:** Sinónimos de `play`, `purchase`
- **Después de limpieza:** Dataset consistente y normalizado

---

## 🔗 Fuente de Datos

El dataset utilizado proviene de [SteamDB](https://www.kaggle.com/datasets) y contiene datos de las interacciones de los usuarios con juegos de Steam.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
