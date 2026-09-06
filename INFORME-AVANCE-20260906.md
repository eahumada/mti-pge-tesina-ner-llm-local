# Informe de avance — 2026-09-06

**Para:** equipo de desarrollo principal
**Corte:** 2026-09-06, tras integrar los resultados parciales del equipo remoto de 48 GB
**Rama:** `sesion/revision-final-20260905`

---

## 1. Titular

Ya existe un **ANOVA conjunto sobre 9 modelos** en el corpus real N=120, con un efecto mucho más fuerte
que el que sostiene hoy la tesina:

| | Antes (§5.3.5 vigente) | **Ahora (preliminar)** |
|:---|:---|:---|
| Modelos | 5 | **9** |
| Filas | 1 200 | **2 160** |
| F-statistic | 10,2096 | **64,0586** |
| p-value | 2,87 × 10⁻¹⁵ | **7,26 × 10⁻¹⁷⁷** |

Salida en `repos/ner-llm-entity-benchmark/results/merged_preliminar_20260906/`.

> Se llama **preliminar** a propósito: faltan `nuextract` (93/120), `gpt-oss:20b` y la corrida principal del
> equipo remoto. Las cifras cambiarán al incorporarlos.

---

## 2. Ranking (F1, N=120)

| # | Modelo y condición | F1 |
|--:|:---|--:|
| 1 | `sonct988/gemma4-26b-a4b-it-q4km-256k` · kb_rag | **0,5964** |
| 2 | `gemma4:31b-mlx` · baseline | 0,5925 |
| 3 | `gemma4:31b-mlx` · kb_rag | 0,5907 |
| 4 | `qwen2.5:14b` · kb_rag | 0,5651 |
| 5 | `sonct988/…` · baseline | 0,5627 |
| … | | |
| 17 | `gemma4:12b-mlx` · baseline | 0,0987 |
| 18 | `gemma4:12b-mlx` · kb_rag | 0,0392 |

**El primer puesto lo ocupa un modelo que habíamos excluido** por no caber en 16 GB de RAM. Lo recuperó el
equipo remoto; sin esa corrida, ese resultado no existiría en el estudio.

---

## 3. Hallazgo: el KB RAG no beneficia a todos por igual

| Modelo | Δ F1 con RAG |
|:---|--:|
| `llama3.2:latest` (3B) | **+0,0999** |
| `gemma:latest` | +0,0569 |
| `qwen2.5:14b` | +0,0462 |
| `sonct988/…` (26B) | +0,0338 |
| `mistral-nemo` (12B) | +0,0250 |
| `gemma4:31b-mlx` (31B) | −0,0018 |
| `gemma4:latest` (9B) | −0,0034 |
| `qwen3:8b` | −0,0229 |
| `gemma4:12b-mlx` | −0,0595 |

**Cinco mejoran, cuatro empeoran**, y el patrón es interpretable: **los modelos pequeños son los que más
ganan** (`llama3.2` 3B encabeza con +10 puntos), mientras los grandes no ganan nada o pierden. El RAG
compensa capacidad limitada, pero estorba a los modelos que ya tienen conocimiento propio suficiente.

Tres de las cuatro caídas están dentro del umbral de 0,02 que `CLAUDE.md` declara tolerable y relevante
para el estudio comparativo.

---

## 4. Anomalía investigada: `gemma4:12b-mlx`

Su F1 de 0,0987 es un orden de magnitud peor que el resto. **No es ruido ni un fallo de comprensión: es un
fallo de formato de salida.**

| Métrica | `gemma4:12b-mlx` | `gemma4:31b-mlx` (control) |
|:---|--:|--:|
| Precisión | **0,9301** | 0,5373 |
| Recall | **0,1365** | 0,7569 |
| `parse_method: fallback` | **104 / 120** | 1 / 120 |
| Registros con recall = 0 | **101 / 120** | — |
| Reintentos | 0 | 0 |
| Alucinación | 0,00 % | — |

El modelo **no emite JSON válido en el 87 % de los casos**; el parser de respaldo por regex rescata solo una
fracción. Cuando extrae algo, casi siempre acierta —precisión del 93 %— pero extrae casi nada.

Es coherente con su histórico de julio (F1 0,1206 con precisión 0,9019), así que el comportamiento es
**reproducible**, no un artefacto de esta corrida.

> **Es un resultado publicable**, no un dato a descartar: documenta que el seguimiento de instrucciones de
> formato es un factor limitante independiente de la capacidad de extracción. Conviene reportarlo con la
> tasa de `fallback` al lado, o la cifra parecerá un error.

---

## 5. Entrega del equipo remoto — verificada

| Tarea | Estado | Filas | Tasa de fallo |
|:---|:---|--:|--:|
| P1 `gemma4:31b` N=15 | ✅ Completada | 30/30 | **0** |
| P2 `sonct988` N=120 | ✅ Completada | 240/240 | **0** |
| P2 `gpt-oss:20b` | ⏳ Encolado, con fix aplicado | 0 | — |
| P3 Principal N=120 | ▶️ En curso (192/1680) | — | 0 |
| P4 Ablación | ⏳ En cola | 0 | — |

**Verificaciones hechas antes de aceptar sus cifras:**
- Tasa de fallo **0 %** en ambas entregas completas.
- Protocolo: los **9 parámetros coinciden**, incluido el `--rag-mode` correcto en cada corpus.
- Consistencia aritmética: ninguna fila viola la cota `F1 ≤ (P+R)/2`.
- Sus cifras se recalcularon **de forma independiente** antes de leer su informe: coinciden.

### Bloqueante principal resuelto
`gemma4:31b` sobre N=15 da **F1 = 0,6912 · P 0,5883 · R 0,8680**, a 1,3 puntos del 0,6783 que la Tabla 2
afirmaba **sin ningún dato crudo**. La cifra de la tabla era correcta; ahora tiene medición detrás.

### Bug que encontraron
`gpt-oss:20b` no fallaba por RAM sino por **enrutado**: `factory.py` mandaba todo `gpt-*` a `OpenAIProvider`,
y `gpt-oss:20b` es Ollama local. Su fix excluye los nombres con `:`, que los modelos OpenAI reales no llevan.

---

## 6. Instrucciones de avance

### 6.1 Inmediato
- [ ] **Revisar el ranking y el hallazgo del RAG diferencial** (§3). Es material nuevo para la tesina y no
      está en ninguna sección actual del informe.
- [ ] **Decidir cómo presentar `gemma4:12b-mlx`** (§4): con su tasa de `fallback` al lado, o el F1 de 0,04
      parecerá un error de cálculo.
- [ ] **No actualizar §5.3.5 todavía.** Las cifras son preliminares; al incorporar los modelos que faltan,
      F y p cambiarán.

### 6.2 Cuando el equipo remoto cierre
- [ ] Re-ejecutar `src/merge_and_analyze.py` con todas las fuentes, incluidas las suyas.
- [ ] Verificar **siempre** la tasa de fallo antes de aceptar cifras nuevas: `parse_method='failed'`
      contamina los promedios con recall 0 y ya nos convirtió un F1 real de 0,66 en un 0,40 aparente.
- [ ] Actualizar §5.3.5 con el ANOVA definitivo y el número final de modelos.

### 6.3 Sigue esperando decisión del autor
Detalle en `TODO-INFORME-FINAL.md §10`:
1. Dos filas con **F1 aritméticamente imposible** (superan la cota `(P+R)/2`) y cuyos valores **no existen
   en ningún archivo de datos**. Retirar o marcar como no verificables.
2. Tabla de ablación: sus 4 cifras tampoco existen en datos. La tarea P4 del remoto las regenera.
3. Cifras de mercado de §1.1 con el marcador `[referencia KPMG 2024]`. Aparcado hasta el final.

---

## 7. Estado de la corrida local

**Completos:** `gemma4:12b-mlx`, `mistral-nemo`, `qwen3:8b` (los tres con baseline y kb_rag).
**En curso:** `nuextract` (93/120).

Tras desactivar la suspensión del equipo, las latencias contaminadas quedaron **congeladas en 36** y su
proporción cayó del 22 % al 10 %. Las nuevas mediciones son limpias.

> La proyección local para lo que falta era de **~518 h (21 días)** con latencias medidas. Por eso se delegó
> la corrida principal al equipo remoto; la local continúa como red de seguridad.
