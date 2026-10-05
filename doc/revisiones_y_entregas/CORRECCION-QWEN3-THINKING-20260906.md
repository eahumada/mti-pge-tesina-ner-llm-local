# 🟠 CORRECCIÓN para el equipo remoto 48 GB — el hallazgo de qwen3 tiene la evidencia invertida

**Fecha:** 2026-09-06 · **De:** equipo de desarrollo principal
**Sobre:** `remote_48g/HALLAZGO-QWEN3-THINKING.md` (commit `2f6ea3d`)
**Urgencia:** media-alta — la decisión que tomasteis es correcta, pero **el razonamiento no puede ir así al
informe**, y hay consecuencias que el documento no contempla.

---

## Resumen en una línea

**Mantened `think=False` para `qwen3:8b`: está bien decidido.** Pero P3 **no** era *think OFF* — era *think
ON*. Las dos corridas que comparasteis tenían el mismo estado de thinking, así que el «F1 idéntico» no
demuestra que el razonamiento sea irrelevante: demuestra que **comparasteis la misma configuración consigo
misma**. El efecto real de apagar el thinking es **grande y favorable**, no nulo.

---

## 1. Lo que dice el documento

> «P3 = qwen3 think OFF (bug previo) vs run limpio = qwen3 think ON (fix)» → F1 baseline idéntico 0.4483
> → «el razonamiento no cambia la extracción final».

## 2. Lo que dicen los datos

Verificación fila a fila sobre `benchmark_n120_REMOTO` (P3) y `qwen3_clean_n120_REMOTO`:

| Comprobación | Resultado |
|:---|:---|
| Filas con `(F1, P, R)` idénticos | **120 / 120** |
| Filas con latencia idéntica | **0 / 120** |
| Ventana de ejecución de P3 (hora local) | **05:07 – 06:19** |
| Fix del thinking `743054d` | **09:08** — es decir, **3 h después de que P3 terminara** |
| Latencia mediana | P3 **789 s** · limpia **517 s** · nothink **67 s** |
| Log de `qwen3_nothink_n120_REMOTO` | `Thinking DISABLED for 'qwen3:8b'` ✅ |

120 de 120 artículos con métricas idénticas al último decimal, pero con latencias todas distintas y
`data_provenance` de 11 h después: el modelo **volvió a ejecutarse de verdad** y produjo **exactamente la
misma extracción**. Eso solo ocurre si ambas corridas tenían el mismo estado de thinking.

**Y lo tenían.** Antes del fix, `think` viajaba dentro de `options` y Ollama lo **descartaba en silencio**;
la corrida no quedaba con thinking apagado, sino **con el comportamiento por defecto de Ollama, que para un
modelo con capacidad `thinking` es activarlo** (es exactamente el mecanismo que documentamos en
`ALERTA-EQUIPO-REMOTO-20260906.md §1` para `gemma4:12b-mlx`). P3 corrió, por tanto, **con thinking ON**.

> **Señal que se pasó por alto.** La propia tabla del hallazgo da *think ON* **más rápido** que *think OFF*
> (517 s vs 789 s). El razonamiento genera tokens: no puede acelerar. Esa inversión era el aviso de que las
> etiquetas estaban cambiadas. **Cuando la latencia contradice la hipótesis, la hipótesis es lo que falla.**

## 3. La comparación correcta

Único par válido: P3 (*think ON*) contra `qwen3_nothink_n120_REMOTO` (*think OFF* verificado en log), sobre
los **78 artículos que ambas comparten**:

| `qwen3:8b` baseline | think ON (P3) | think OFF (nothink) | Δ |
|:---|--:|--:|--:|
| **F1** | 0.4606 | **0.5122** | **+5,2 pp** |
| `recall = 0` | 10 | **1** | −9 |
| Latencia media | 688 s | **66,5 s** | **10,3×** |

Apagar el thinking **no es neutro**: sube F1 unos 5 puntos, elimina casi todas las extracciones vacías y
acelera diez veces. Vuestra decisión queda **mejor respaldada** de lo que la justificasteis.

---

## 4. Qué os pedimos

1. **Mantener `think=False` para `qwen3:8b`.** Confirmado. No hay que revertir nada del código.

2. **Añadir una nota de corrección** al final de `HALLAZGO-QWEN3-THINKING.md` — **de forma aditiva, sin
   borrar ni reescribir lo ya escrito** — recogiendo que P3 era *think ON* y que el efecto medido es
   +5,2 pp / 10,3×. El argumento del «F1 idéntico» **no puede citarse en el informe**: es un artefacto de
   comparar una configuración consigo misma.

3. **Terminar `qwen3_nothink_n120_REMOTO`** (al momento de escribir: 90/120 del baseline; faltan los 120 de
   `kb_rag`). **De ahí sale el dato de qwen3 para el estudio.**

4. **Marcar como inválidas las filas qwen3 de P3 y de la corrida limpia.** Todo lo que hoy figura en el
   estudio para `qwen3:8b` (0.4483 baseline / 0.4425 kb_rag) es *think ON* y **subestima al modelo ~5 pp**.
   No borréis nada: quedan como registro histórico, igual que se hizo con `gemma4:12b-mlx`.

5. **Publicar el `run_config.json`** de las dos corridas qwen3. **Ahora mismo no existe en ninguna de las
   dos**, y sin él no podemos verificar el protocolo. Debe confirmar `rag_mode=kb_combined` y
   `num_workers=9`. Dejad constancia de la desviación ya conocida: `afectados_thinking_n120_REMOTO` usó
   **`num_workers=6`**, no 9.

6. **Revisar el resto de la familia Qwen3.** `qwen3:14b`, `qwen3:32b` y `qwen3:latest` siguen en
   `_QWEN3_THINKING_MODELS`, es decir con thinking ON. Si alguno participa en el estudio, arrastra la misma
   penalización. Decidnos cuáles participan y, salvo evidencia en contra, aplicadles `think=False`.

7. **Enumerar los modelos del estudio con capacidad `thinking`** (`ollama show <modelo>`). Toda corrida
   anterior al fix `743054d` los ejecutó con **thinking ON por defecto**, no apagado. Necesitamos saber a
   cuántos modelos alcanza esto antes de consolidar el ANOVA.

8. **No tocar la fila `real_mixed_64`** de la corrida nothink (`P=R=0` con `F1=1.0`): es el defecto de
   scoring que vosotros mismos documentasteis en `HALLAZGO-SCORING-F1.md`. **La decisión es del autor.**
   Limitaos a reportar cuántas filas así hay por modelo.

---

## 5. Reglas que siguen vigentes

- **Política estrictamente aditiva:** si un conteo no cuadra, se corrige el conteo, **nunca los datos**.
- **Backup previo** a toda modificación de un documento compartido.
- **Releer `CURRENT-TASKS.md` justo antes de escribir**, y escribir siempre por *append* en vuestra sección.
- Un hallazgo de auditoría es una **hipótesis**, no un hecho, hasta contrastarlo con la fuente primaria.
  Esta corrección es precisamente ese contraste, y por eso llega como documento aparte y no como una
  reescritura del vuestro.

---

## 6. Actualización 17:55 — el baseline *think OFF* ya cerró 120/120

`qwen3_nothink_n120_REMOTO` completó el baseline mientras se redactaba esta corrección. Cifra definitiva
sobre los **120 artículos completos**, que sustituye a la del §3 (aquella era sobre los 78 comunes
disponibles en ese momento):

| `qwen3:8b` | think ON (P3, n=120) | think OFF (nothink, n=120) | Δ |
|:---|--:|--:|--:|
| **baseline F1** | 0.4483 | **0.4904** | **+4,2 pp** |
| `recall = 0` | 15 | **1** | −14 |
| `parse_method='failed'` | 0 | **0** | — |

`kb_rag` va por 96/120 con F1 **0.5528** (P3 think ON: 0.4425). Provisional hasta que cierre: **no citar
todavía**, por la misma razón por la que el baseline pasó de 0.5147 (parcial) a 0.4904 (completo) — **un
subconjunto parcial no es representativo**.

Conclusión reforzada: apagar el thinking en `qwen3:8b` sube el F1 del baseline **+4,2 pp** y reduce las
extracciones vacías de **15 a 1**, con 0 fallos de parseo.
