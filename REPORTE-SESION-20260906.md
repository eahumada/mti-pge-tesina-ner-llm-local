# Reporte de sesión — 2026-09-03 a 2026-09-06

**Rama:** `sesion/revision-final-20260905` · **14 commits** sobre `main` (`bb79279`)
**Veredicto general:** ✅ **Correcto**, con salvedades acotadas en §5.

---

## 1. Qué se pedía y qué se logró

El encargo inicial era completar el benchmark N=120 para los 11 modelos que faltaban. **Ese objetivo no se
cumplió tal cual**, y con razón: el diagnóstico reveló que el plan no era ejecutable en el hardware
disponible y que varios datos existentes no eran válidos.

Lo que sí se logró:

| Resultado | Estado |
|:---|:---|
| ANOVA conjunto sobre **9 modelos**, N=120 | ✅ `F=64,06 · p=7,26e-177` (antes: 5 modelos, F=10,21) |
| Bloqueante principal de la Tabla 2 | ✅ Resuelto — `gemma4:31b` con dato propio |
| Modelo cloud con medición limpia | ✅ `gemma4:31b-cloud` F1 0,6699, 0 fallos |
| Modelo recuperado de los excluidos | ✅ `sonct988` — **lidera el ranking** |
| Bugs de código corregidos | ✅ 4 (ver §3) |
| Trabajo delegado y en marcha | ✅ Equipo remoto al 62 % de P3 |

---

## 2. Verificación: ¿fue correcto?

### 2.1 Lo que se verificó antes de aceptar cada cifra

| Comprobación | Resultado |
|:---|:---|
| Tasa de fallo en las entregas remotas | **0 %** en ambas corridas completas |
| Protocolo de las corridas remotas (9 parámetros) | **Coinciden**, incluido `--rag-mode` |
| Consistencia aritmética `F1 ≤ (P+R)/2` | Ninguna fila nueva la viola |
| Cifras remotas recalculadas de forma independiente | **Coinciden** con su informe |
| Script de fusión `merge_and_analyze.py` | Reproduce `F=10,2096 · p=2,8730e-15` exactos |
| Secretos en los commits | **0** en los 14 |
| `.setenv.sh` en el remoto | **Ausente**, verificado contra GitHub |

### 2.2 Errores que se cometieron y se corrigieron dentro de la sesión

Se documentan porque la trazabilidad importa más que la apariencia:

| Error | Cómo se detectó | Estado |
|:---|:---|:---|
| Afirmar que Ollama no ejecuta MLX | Auditoría del registro | ✅ Corregido |
| Concluir que el enlace estaba saturado con **una sola** medición | Test de escalado (1→4 streams) | ✅ Corregido |
| Buscar solo el código 402 y perder 720 fallos con 429 | Recuento por categoría | ✅ Corregido |
| Lanzar el benchmark sin `--rag-mode kb_combined` | Comparación de nombres de grupo | ✅ Detenido a los 20 min |
| Lanzar con `num_workers=2` en vez de 9 | Lectura del `run_config` de referencia | ✅ Corregido |
| Declarar «cero ocurrencias» del modelo retirado sin mirar los datos | Auditoría de coherencia | ✅ Corregido |
| Excluir los diccionarios por «regenerables» | **Pregunta del autor** | ✅ Corregido |
| Interpretar el F1 de 0,0987 como límite del modelo | **Pregunta del autor** | ✅ Corregido |
| Comentarios en línea en `.gitignore` (git no los soporta) | 1,7 MB colándose en el staging | ✅ Corregido |

**Tres de los hallazgos más importantes salieron de preguntas del autor**, no del análisis automático:
la contaminación por cuota, la irreproducibilidad de los diccionarios y el F1 anómalo.

---

## 3. Bugs de código corregidos

| # | Bug | Impacto |
|--:|:---|:---|
| 1 | `--resume` inoperante sin `--results-dir` | Una corrida interrumpida **reiniciaba desde cero en silencio** |
| 2 | Sin guardarraíl contra escribir en `results/` raíz | Causó la **pérdida permanente** de los datos por registro de N=30 |
| 3 | `think` dentro de `options` en vez de primer nivel | El modo thinking de Qwen3 **nunca se activó**, pese a que código y documentación lo afirmaban |
| 4 | `gemma4:12b-mlx` sin `think=False` | Respuestas **vacías** en artículos largos: 101 de 120 con recall 0 |

El #4 producía un F1 aparente de 0,0987 que se interpretó primero como limitación del modelo. Con el fix,
el mismo artículo que devolvía nada extrae 14 personas, 6 organizaciones y 16 ubicaciones.

Los bugs 3 y 4 llevaban **meses latentes**.

---

## 4. Hallazgos con valor para la tesina

1. **El KB RAG no beneficia a todos por igual.** Cinco modelos mejoran y cuatro empeoran, con un patrón
   interpretable: los pequeños ganan (`llama3.2` 3B: **+0,0999**) y los grandes no ganan o pierden
   (`gemma4:31b-mlx`: −0,0018). Material nuevo, no presente en ninguna sección del informe.
2. **`gemma4:31b` verificado:** F1 0,6912 frente al 0,6783 que la Tabla 2 afirmaba **sin dato crudo**.
   La cifra era correcta; ahora tiene respaldo.
3. **Contaminación por fallos de cuota:** un F1 real de 0,66 aparecía como 0,40 porque las extracciones
   fallidas puntúan recall 0. Aplica a los modelos cloud del corpus N=15.
4. **41 hallazgos** y **32 lecciones** documentados con evidencia reproducible.

---

## 5. Salvedades — lo que NO está cerrado

| Pendiente | Bloquea |
|:---|:---|
| Dos filas con **F1 aritméticamente imposible**, cuyos valores no existen en dato alguno | Decisión del autor: retirar o marcar |
| Tabla de ablación: 4 cifras sin respaldo en datos | La regenera P4 del equipo remoto |
| Cifras de mercado con marcador `[referencia KPMG 2024]` | Requiere la fuente real |
| `gemma4:12b-mlx` y `qwen3:8b` | Datos inválidos por el bug #4 — re-corrida encolada en el remoto |
| Corrida local | **Detenida a propósito** para no duplicar el esfuerzo remoto |

> **§5.3.5 de la tesina NO debe actualizarse todavía.** El ANOVA de 9 modelos es preliminar: dos de esos
> modelos hay que rehacerlos y faltan `gpt-oss` y la ablación.

---

## 6. Estado del equipo remoto

Respondieron a la alerta el 2026-09-06 09:04 y adoptaron la alternativa propuesta:

- **P1** `gemma4:31b` N=15 — ✅ completada, 0 fallos
- **P2** `sonct988` N=120 — ✅ completada, 0 fallos
- **P3** principal N=120 — ▶️ 62 % (1047/1680); 5 modelos válidos, 2 afectados por el bug
- **P4**, `gpt-oss` y re-corrida de afectados — ⏳ encoladas con serialidad correcta

Encontraron por su cuenta un **bug de enrutado** (`gpt-oss:20b` iba a `OpenAIProvider` por su prefijo
`gpt-`), ya integrado.

---

## 7. Veredicto

**El trabajo es correcto y está respaldado.** Ninguna cifra entró en la documentación sin verificación
independiente, y los errores cometidos se detectaron y corrigieron dentro de la propia sesión, quedando
documentados.

El objetivo literal —16 modelos sobre N=120— **no se alcanzó**, y no debía alcanzarse tal como estaba
planteado: el hardware no daba, dos modelos cloud no son ejecutables, y varios datos que se iban a usar
resultaron inválidos. Lo que sí hay es un estudio de **9 modelos con estadística sólida**, un camino claro
para llegar a 13-14 con el trabajo remoto en curso, y un registro de por qué cada número es defendible.
