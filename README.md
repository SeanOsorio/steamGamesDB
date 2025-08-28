# 🎮 SteamGamesDB - ETL de Steam (Rama `features`)

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de **extracción, limpieza y carga (ETL)** de datos de la plataforma Steam, usando como fuente principal el dataset **`steam-200k.csv`**.  

En la rama **`features`**, el proyecto evoluciona respecto a la rama `realice` con **mejoras en la limpieza y en la robustez del sistema de extracción**, asegurando que los datos estén en condiciones óptimas para análisis avanzados.

---

## 🏗️ Estructura del Proyecto

```
steamGamesDB/
│
├── main.py                              # Orquestador ETL (entrada principal)
├── README.md                            # Documentación de esta rama
├── requirements.txt                     # Dependencias
│
├── config/                              # Configuración
│   └── config.py
│
├── Extract/                             # Extracción de datos
│   └── steamGamesExtract.py             # Lectura robusta (dtype=str, on_bad_lines=skip)
│
├── transform/                           # Transformación y limpieza
│   └── transform_clear.py               # Validaciones extra (hours >= 0, normalización)
│
├── load/                                # Carga de datos
│   └── Load.py
│
└── sources/                             # Datos
    ├── steam-200k.csv                   # Dataset original
    └── steam-200k.cleaned.csv           # Dataset procesado
```

---

## 🚀 Instalación y Configuración

1. Crea y activa entorno virtual (opcional, recomendado):  
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

2. Instala dependencias:  
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

---

## 🧹 Mejoras de Limpieza en esta Rama (`features`)

Comparado con la rama `realice`, ahora se incluyen:
- ✅ **Lectura robusta del CSV** → `dtype=str` y `on_bad_lines="skip"` para evitar errores por líneas corruptas.  
- ✅ **Validación de `hours`** → se descartan registros con horas negativas.  
- ✅ **Normalización de acciones** → `Played`, `Buy`, `Purchased` se transforman a `play` o `purchase`.  
- ✅ **Reporte QA** más claro en consola.  

---

## 📊 Dataset de Steam

- **Archivo:** `steam-200k.csv`  
- **Registros:** ~200,000  
- **Campos esperados:**
  - `user_id`
  - `game`
  - `action`
  - `hours`
  - `value`

---

## 📈 Ejemplo de Resultados

Ejemplo de salida de `--report` en esta rama:

```
Total filas: 200000
Nulos en user_id: 0
Nulos en game: 0
Duplicados exactos: 132
Distribución acciones: {'play': 150321, 'purchase': 49789}
```

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue antes de proponer cambios significativos.  

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.  
