#  SteamGamesDB - Proyecto de Limpieza de Datos de Steam

##  Descripción del Proyecto

Este proyecto implementa un sistema de **extracción, limpieza y carga (ETL)** de datos de la plataforma Steam, utilizando como fuente principal el dataset **`steam-200k.csv`**.  

El sistema está diseñado con una arquitectura modular que permite:
- La **extracción** de datos desde el CSV original.  
- La **limpieza automática** mediante reglas de normalización y validación.  
- La **generación de un dataset limpio** listo para análisis posteriores.  

---

## Estructura del Proyecto

```
steamGamesDB/
│
├── main.py                              # Punto de entrada principal (ejecuta el pipeline)
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

## Instalación y Configuración

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
venv\Scripts\activate      # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

---

##  Uso del Sistema

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
- Normalización de columnas (`user_id`, `game`, `action`, `hours`, `value`)  
- Conversión de `action` a minúsculas y mapeo de sinónimos (`played → play`, `buy → purchase`)  
- Conversión de `hours` y `value` a valores numéricos  
- Eliminación de filas con `user_id` o `game` nulos  
- Eliminación de registros con `hours < 0`  
- Eliminación de duplicados  

---

## Dataset de Steam

### Información del dataset utilizado
- **Archivo principal:** `steam-200k.csv`
- **Registros:** 200,000 filas aproximadas
- **Campos esperados:**
  - `user_id` → Identificador del usuario
  - `game` → Nombre del juego
  - `action` → Acción del usuario (`play`, `purchase`)
  - `hours` → Horas jugadas
  - `value` → Indicador de compra (0/1)

### Calidad de los datos
- **Valores nulos detectados:** Sí, en varias columnas
- **Acciones inconsistentes:** Variantes como `Played`, `Buy`  
- **Después de limpieza:** dataset consistente y normalizado

---

## Funcionalidades Principales

### Clase `Extractor`
- Lee el CSV original.  
- Detecta columnas faltantes y las completa con valores nulos.  

### Clase `Transformer`
- Aplica reglas de limpieza y validación.  
- Normaliza `action` y asegura que `hours` ≥ 0.  

### Clase `Loader`
- Exporta el dataset limpio a CSV.  
- Opción de exportar también en otros formatos (ej. Parquet en ramas posteriores).  

---

## Resultados del Procesamiento

Ejemplo de salida de `--report`:
```
Total filas: 200000
Nulos en user_id: 0
Nulos en game: 0
Duplicados exactos: 145
Distribución acciones: {'play': 150123, 'purchase': 49877}
```
'  

---

## Licencia

Este proyecto está bajo la Licencia MIT.  
