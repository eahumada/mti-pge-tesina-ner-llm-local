# Procedencia de los diccionarios RAG

> ⚠️ **Estos archivos son un *snapshot* irreproducible. No los regeneréis.**

| Archivo | Entradas | Creado |
|:---|---:|:---|
| `persons.json` | 3.605 | 2026-07-27 00:30 |
| `organizations.json` | 1.848 | 2026-07-27 00:30 |
| `augmented_persons.json` | 12.000 | 2026-07-27 08:51 |

## Por qué se versionan pese a existir scripts que los generan

Los scripts `fetch_dictionaries.py`, `download_ofac.py` y `generate_metadata_dicts.py` los construyen a
partir de **fuentes vivas**:

| Fuente | Estabilidad |
|:---|:---|
| `treasury.gov/ofac/downloads/sdn.csv` | ❌ La lista SDN cambia **cada pocos días**: las designaciones de sanciones se añaden y retiran de forma continua |
| `github.com/datasets/s-and-p-500-companies` (`master`) | ❌ Rama móvil |
| `github.com/jvalhondo/spanish-names-surnames` (`master`) | ❌ Rama móvil |
| `github.com/rfordatascience/tidytuesday` (`master`) | ❌ Rama móvil |

Ninguno de los scripts fija fecha, versión ni commit. **Ejecutarlos hoy produce un conjunto distinto del
que se usó en los experimentos**, y los archivos generados no llevan metadata que permita detectarlo.

Como el RAG en modo `entities` inyecta estas entradas en el prompt, un diccionario distinto cambia el
contexto que ve el modelo y, por tanto, **los resultados**. Son **entrada experimental**, no un artefacto
regenerable.

## Consecuencia práctica

- Para reproducir cualquier corrida con `--rag-mode entities`, usad **estos** archivos tal cual.
- Si necesitáis actualizarlos, hacedlo en una **copia fechada** (`dictionaries_YYYYMMDD/`) y declarad
  explícitamente qué corridas usaron cuál.

Ver `FINDINGS.md §F39`.
