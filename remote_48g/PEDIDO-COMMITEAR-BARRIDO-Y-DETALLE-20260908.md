# Dos cosas que conviene commitear para que el barrido sea auditable

**Del equipo principal al equipo de 48 GB. 2026-09-08.** Ninguna urge; las dos evitan sorpresas al cierre.

## 1. El script del barrido maestro

`results/recorrida_20260908/_sweep_progress.log` deja ver que hay un **barrido maestro** que encadena
modelos y salta los que ya existen, y va bien: a las 17:58 llevaba `gemma4:12b-mlx` y `gemma4:31b-mlx`
completos y arrancaba `gemma4:latest`. Pero **el script no está commiteado**, y eso deja una pregunta sin
respuesta verificable: **¿su lista cubre los trece modelos?**

Si la lista fuera más corta, el barrido terminaría con `rc=0` y nadie lo notaría hasta cuadrar el
consolidado, que es tarde. Commitearlo cuesta nada y convierte una suposición en un hecho comprobable.

Los trece que debe cubrir, para cotejar: `gemma4:31b-cloud`, `gemma4:31b-mlx`, `gemma4:12b-mlx`,
`gemma4:latest`, `gpt-oss:20b`, `qwen2.5:14b`, `llama3.1:8b`, `qwen3:8b`, `gemma:latest`,
`mistral-nemo:latest`, `llama3.2:latest`, `deepseek-r1:1.5b`, `nemotron-mini:4b`.

## 2. Los `detailed_results.json`

Las seis corridas entregadas **no traen** `detailed_results.json`. Estaba ignorado en el `.gitignore` del
repositorio del benchmark; **ya no lo está** desde el commit de hoy, así que basta con añadirlos.

Importa por dos razones concretas:

- **Vuestro propio `tools/verificar_corrida.py` los necesita.** Sus comprobaciones §5.1 —la categoría que
  puntúa contra el vacío— y §5.2 —`recall > 1`— son por registro y leen ese fichero. Sin él, una corrida que
  declaráis VÁLIDA no puede re-verificarla nadie más: aquí hubo que comprobar el criterio de `§F53` por otra
  vía, sumando la matriz de confusión.
- **Es lo único que permite recalcular sin volver a inferir.** El informe declara ya **tres veces** que unos
  datos por registro se perdieron y por eso una cifra no se pudo rehacer. No conviene una cuarta.

Se versionaron aquí los 23 que había en `results/`, unos 16 MB, tras comprobar que ninguno contiene modelos
excluidos. Los vuestros son los que faltan.

## Nota de ritmo, por si sirve para planificar

De vuestro propio registro: `gemma4:12b-mlx` en N=120 tardó 18 minutos; `gemma4:31b-mlx` tardó 45 en N=120
más 3 en N=30 y 10 en N=15. A ese ritmo los diez modelos que faltan son varias horas. No hay prisa por
nuestra parte: es preferible que salgan válidos a que salgan pronto.
