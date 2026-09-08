# Procedimiento de cierre de la re-corrida

**2026-09-08.** Qué hacer cuando el equipo de 48 GB termine los trece modelos. Las cuatro herramientas
mecánicas están escritas y validadas contra los datos actuales; esto es el orden en que se usan y qué mirar
entre paso y paso.

**El orden importa.** Cada paso deja el repositorio en un estado que el siguiente da por bueno, y saltarse
uno produce un resultado que parece correcto.

---

## 0. Antes de empezar: comprobar que están los trece

```sh
python3 tools/estado_recorrida.py | head -20
```

Debe decir **13 de 13 modelos** en N=120. Si dice menos, no se sigue: falta corrida. Comprobar también que el
barrido terminó de verdad, mirando el final de `_sweep_progress.log` en su rama.

---

## 1. Fusionar su rama

```sh
git fetch origin
git merge origin/fix/recorrida-correcciones-20260908
```

Su rama trae además `data/knowledge_base/contaminated_exemplar_articles.json`, que **hoy no está en `main`** y
que el paso 2 necesita. Sin fusionar, la fusión de datos se para (así está diseñada).

**Comprobar tras el merge:** que llegan los `detailed_results.json` de sus corridas. Se les pidieron en
`remote_48g/PEDIDO-COMMITEAR-BARRIDO-Y-DETALLE-20260908.md`; sin ellos no se puede recalcular nada sin
volver a inferir, y `tools/composicion_fp.py` del paso 4 no funcionará.

---

## 2. Consolidar y rehacer el ANOVA

```sh
cd repos/ner-llm-entity-benchmark
./venv/bin/python -m src.merge_and_analyze \
    results/recorrida_20260908/*__N120 \
    --output-dir results/ANALISIS_CONJUNTO_<fecha>
```

La herramienta **se para sola** en dos casos, y en ambos hay que mirar antes de forzar:

- si falta el manifiesto de artículos contaminados: sin él, el ANOVA incluiría los siete artículos que son a
  la vez ejemplares del RAG y sobrevaloraría el efecto (`FINDINGS §F65`);
- si el número de grupos no es **26**: un modelo que no se pasa no produce ningún síntoma (`§1.31`).

**Comprobar:** 26 grupos, 113 registros por grupo, 2 938 filas.

---

## 3. Rehacer la Tabla 7

```sh
python3 tools/generar_tabla7.py results/ANALISIS_CONJUNTO_<fecha>
```

Produce las trece filas listas para pegar, con la columna de significancia leída del post-hoc. Antes de
usarlo conviene ejecutarlo con `--validar` sobre el consolidado **antiguo**: debe reproducir la Tabla 7
vigente sin discrepancias. Si no lo hace, algo cambió en el formato y el generador no es de fiar.

Después hay que actualizar a mano `TABLA7` en `tools/generar_figuras_informe.py` y regenerar las figuras. El
verificador comprueba que la Figura 2 concuerda con la Tabla 7, así que un olvido se detecta solo.

---

## 4. Rehacer la composición de los falsos positivos

```sh
python3 tools/composicion_fp.py results/ANALISIS_CONJUNTO_<fecha> --resumen
```

**Aquí hay que leer la salida, no solo copiar la cifra.** Con el corpus corregido, `Locations` deja de tener
`tp+fn = 0`: sus falsos positivos pasan de ser **aciertos imposibles** a **errores reales del modelo**. La
Figura 1 y las frases de §3.3 y §7.2 no solo cambian de número, **cambian de argumento**. La herramienta lo
avisa expresamente.

---

## 5. Reescribir lo que ya no es cierto

Esto no se automatiza. Por orden de importancia:

1. **§5.3.1.** Si el cambio de signo se confirma —cuatro de cuatro modelos lo mostraban al escribir esto—, la
   frase «el beneficio se anula o revierte en los de mayor capacidad» deja de ser cierta (`FINDINGS §F68`).
   Reformular con lo que digan los datos, sea lo que sea.
2. **§3.3, §7.2 y la leyenda de la Figura 1**, según el paso 4.
3. **El Anexo I.** Su columna de «métrica restringida» pierde sentido cuando el corpus anota las tres
   categorías: no hay nada que restringir. Decidir si se conserva como registro histórico de la corrección o
   se sustituye.
4. **La Tabla 8, solo si se entiende antes por qué cambian las latencias** (`FINDINGS §F71`). Sustituir unas
   cifras inexplicadas por otras no mejora nada.

---

## 6. Verificar

```sh
python3 tools/verificar_informe.py --red
```

Las veinte comprobaciones deben quedar en cero fallos. Las que atan tablas y figuras a los datos **fallarán
mientras el informe esté desactualizado**, y eso es lo que se busca: sirven de lista de tareas.

Los dos avisos vigentes se retiran de `verificar_informe.py` cuando dejen de aplicar: la asimetría de
`max_tokens`, que la re-corrida resuelve, y los dos JSON rotos, si se reparan.

---

## 7. Propagar a los `.docx`

Según `PROPAGACION-PENDIENTE-DOCX-20260908.md`. **No regenerar con pandoc.** Y recordar que el recuento de
páginas no se puede leer del metadato del `.docx`: hay que abrir en Word o generar el PDF.
