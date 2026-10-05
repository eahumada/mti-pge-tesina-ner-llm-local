# 🔴 ALERTA para el equipo remoto 48 GB — bug que invalida dos modelos

**Fecha:** 2026-09-06
**De:** equipo de desarrollo principal
**Urgencia:** alta — **afecta a la corrida P3 que tenéis en marcha**

---

## Resumen en una línea

`gemma4:12b-mlx` devuelve **respuestas vacías** en artículos largos por un bug del arnés, no del modelo.
Y de paso descubrimos que **el modo *thinking* de Qwen3 nunca llegó a activarse**. Ambos afectan a vuestra
corrida P3 en curso. **Hay fix, ya commiteado.**

---

## 1. El bug principal

`gemma4:12b-mlx` declara capacidad `thinking`, y Ollama la activa por defecto. En artículos largos el
razonamiento **agota el presupuesto de `num_predict` (2048) antes de emitir la respuesta**, de modo que
`message.content` llega vacío y el pipeline registra cero entidades.

### Evidencia medida (N=120, `gemma4:12b-mlx_baseline`)

| Indicador | Valor |
|:---|--:|
| Registros con recall = 0 | **101 / 120** |
| `parse_method: fallback` | **104 / 120** |
| Respuestas crudas vacías | **272 de 273** |
| F1 aparente | **0,0987** |
| Errores HTTP | 0 |
| Reintentos | 0 |

**Los artículos que fallan son 1,36× más largos** que los que sobreviven (1976 vs 1453 chars de mediana):
más texto ⇒ más razonamiento ⇒ se agota el presupuesto.

### Reproducción en el peor caso (artículo de 8813 chars)

| Configuración | `content` | `thinking` | `eval_count` | Resultado |
|:---|--:|--:|--:|:---|
| Actual | **0** | 7 651 | **2 048** ← tope exacto | ❌ vacío |
| `think=False` | **918** | 0 | 311 | ✅ extracción correcta |

**No es una limitación del modelo.** Con el razonamiento desactivado extrae correctamente: 14 personas,
6 organizaciones y 16 ubicaciones en ese mismo artículo.

---

## 2. El segundo bug, descubierto al arreglar el primero

`think` es **parámetro de primer nivel** de `Client.chat()`, no una clave de `options`. El código lo metía
dentro de `options`, donde **Ollama lo ignora en silencio**.

Consecuencia: `options["think"] = True` para Qwen3 **nunca se aplicó**. Las cifras de `qwen3:8b` del estudio
se midieron con el modo thinking **desactivado**, pese a que el código creía activarlo.

---

## 3. Qué hemos corregido

Commit en `sesion/revision-final-20260905`, archivo `src/providers/ollama_provider.py`:

1. `think` pasa como **parámetro de primer nivel** a `client.chat()`.
2. Nuevo `_THINKING_DISABLED_MODELS` con las variantes MLX de gemma4, que reciben `think=False` para que
   todo su presupuesto de tokens vaya a la respuesta, en igualdad con el resto de modelos del estudio.
3. Qwen3 mantiene `think=True`, **ahora sí efectivo**.

---

## 4. 🔴 Lo que necesitamos de vosotros

### 4.1 Antes de seguir: actualizad el código

```bash
git pull origin sesion/revision-final-20260905
```

Sin esto, cualquier corrida que incluya `gemma4:12b-mlx` seguirá produciendo datos inválidos.

### 4.2 Vuestra corrida P3 está afectada

La corrida principal N=120 incluye **`gemma4:12b-mlx`** (bug 1) y **`qwen3:8b`** (bug 2). Sus resultados en
esa corrida **no son válidos** tal como están.

**Recomendación:** parad P3, aplicad el pull, y **re-lanzadla desde cero para esos dos modelos**. Los otros
cinco no están afectados y su checkpoint es aprovechable.

Si preferís no perder el avance, una alternativa aceptable es dejar P3 terminar y re-ejecutar **solo**
`gemma4:12b-mlx` y `qwen3:8b` después, en un directorio aparte. Nosotros nos encargamos de fusionar.

### 4.3 Verificación obligatoria tras el fix

Antes de dar por buena cualquier corrida con estos modelos:

```bash
python3 -c "
import csv, collections
r = list(csv.DictReader(open('results/<DIR>/benchmark_results.csv')))
for m in ['gemma4:12b-mlx_baseline','qwen3:8b_baseline']:
    g = [x for x in r if x['model'] == m]
    if not g: continue
    ceros = sum(1 for x in g if float(x.get('recall') or 0) == 0)
    pm = collections.Counter(x.get('parse_method') for x in g)
    print(f'{m}: recall=0 en {ceros}/{len(g)} · parse={dict(pm)}')"
```

**Criterio de aceptación:** `recall=0` debe ser **residual** (unos pocos de 120, no 101), y `fallback` debe
ser minoritario frente a `direct_json`. Si volvéis a ver 100+ ceros, **parad y avisadnos**.

---

## 5. Cómo lo detectamos, por si os sirve el método

El F1 de 0,0987 parecía un modelo simplemente malo. Tres pistas lo desmintieron:

1. **La precisión era 0,93** — sospechosamente alta para un modelo «malo». Resultó ser el caso degenerado:
   con `tp=0` y `fp=0`, la precisión se define como 1,0. **Un modelo que no extrae nada tiene precisión
   perfecta.**
2. **`tokens_per_sec` × latencia daba ~24 000 tokens generados** — más que modelos que sí funcionaban. El
   modelo *estaba* trabajando; los tokens iban a otro sitio.
3. **Cero errores HTTP y cero reintentos.** No era la red.

La lección: **una métrica agregada no distingue «el modelo es malo» de «el arnés no lee su salida»**. La
metadata por fila (`parse_method`, `retries`, `recall=0`) sí.

---

## 6. Lo que sí sigue siendo válido de vuestra entrega

Nada de esto invalida lo que ya nos disteis:

- ✅ **P1 `gemma4:31b` N=15** — F1 0,6912, tasa de fallo 0. Resolvió el bloqueante principal de la tesina.
- ✅ Vuestro fix de enrutado de `gpt-oss:20b` está integrado.

Ninguno de esos modelos tiene capacidad `thinking`, así que no les afecta.

Gracias por el rigor del reporte anterior: las verificaciones previas que documentasteis (conteos de corpus
y diccionarios) son las que nos permitieron descartar rápido que el problema estuviera en los datos.
