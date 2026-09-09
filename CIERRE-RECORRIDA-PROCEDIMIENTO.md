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

### Ensayado el 2026-09-09 con once modelos, y funciona

Antes de que lleguen los trece se ejecutó la fusión sobre los **once** ya entregados, extrayendo sus CSV de la
rama a un directorio temporal. **Corre de extremo a extremo**: 2 486 filas, **22 grupos**, 113 `record_id`
únicos, F = 30,9783 con p = 3,2723 × 10⁻¹⁰⁹. No hay que descubrir un bloqueo el último día.

Tres cosas que el ensayo dejó claras:

- **El manifiesto de contaminados llega con la rama.** La herramienta lo busca por defecto en
  `data/knowledge_base/contaminated_exemplar_articles.json`, que **no está en `main`**: solo aparece tras el
  paso 1. Ejecutar el paso 2 antes que el 1 la detiene, que es el comportamiento correcto.
- **No pasar `--expected-n 120`.** Es el recuento **antes** de excluir los contaminados, y forzarlo hace que
  los veintiséis grupos se marquen `INCOMPLETO` teniendo exactamente las filas que deben tener. Sin la
  bandera, la herramienta deduce 113 después de excluir y no emite un solo aviso. Se comprobó en los dos
  sentidos: con `--expected-n 120` salen 22 avisos falsos y con 113 o sin bandera, ninguno.
- **El intérprete es el del proyecto.** `repos/ner-llm-entity-benchmark/venv/bin/python`, con pandas 3.0.5 y
  scipy 1.18.0. El `python3` del sistema no tiene pandas y la herramienta ni siquiera arranca.

La orden ensayada, con las rutas del árbol de trabajo tras fusionar la rama:

```sh
cd repos/ner-llm-entity-benchmark
./venv/bin/python src/merge_and_analyze.py \
    results/recorrida_20260908/*__N120 \
    --output-dir results/ANALISIS_CONJUNTO_<fecha> \
    --grupos-esperados 26
```

---

## 2.bis. Rehacer los contrastes de robustez

El ANOVA que produce el paso anterior trata como independientes unas observaciones que no lo son. Los dos
contrastes que lo acreditan se rehacen con una sola orden:

```sh
repos/ner-llm-entity-benchmark/venv/bin/python tools/robustez_estadistica.py \
    repos/ner-llm-entity-benchmark/results/ANALISIS_CONJUNTO_<fecha>/merged_results.csv \
    --json repos/ner-llm-entity-benchmark/results/ROBUSTEZ_ESTADISTICA_<fecha>
```

Da el **Friedman** de medidas repetidas y el **post-hoc pareado** —Wilcoxon por modelo entre línea base y KB
RAG sobre los mismos registros, con Holm sobre las trece comparaciones de interés—. De ahí salen `§F75`,
`§F76` y la **decisión 7**.

**Hasta el 2026-09-09 esto no se podía hacer:** los artefactos publicados se habían calculado a mano y ningún
script los reproducía (`FINDINGS §F83`). La herramienta se validó exigiéndole reproducir lo publicado
—χ² = 1169,2327 y 8 de 13 significativos— con `--validar`, que conviene ejecutar de nuevo sobre el
consolidado antiguo si alguna vez se toca la herramienta.

**Y hay que esperar cambios grandes.** Sobre los once modelos entregados al 2026-09-09, el post-hoc pareado
da **2 significativos de 11** frente a los 8 de 13 de los datos antiguos. La cifra es provisional —falta
`nemotron-mini:4b`, que era el de mayor efecto— pero la dirección está clara: **§5.3.1 habrá que reescribirlo
con bastante más que un cambio de cifras**.

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

1. **§5.3.1, y ya no es una hipótesis: está medido** (`FINDINGS §F86`). Con los trece modelos rehechos:
   - La frase «el beneficio se anula o revierte en los de mayor capacidad» **es falsa**. Los cinco de mayor
     capacidad tienen **todos** Δ positivo: +0,81, +0,97, +2,29, +1,67 y +2,53.
   - La correlación que sostiene el argumento **se desploma**: Spearman pasa de −0,5165 a **−0,0879
     (p = 0,7752)** y Pearson de −0,6004 a −0,5266 (p = 0,0645), este último **sostenido por un solo punto**:
     retirando `nemotron-mini:4b` queda en +0,0120 con p = 0,971.
   - **Lo que sí se puede afirmar:** **tres** modelos mejoran de forma significativa tras el post-hoc
     pareado —`nemotron-mini:4b` +14,23, `llama3.2:latest` +6,73 y `gemma4:12b-mlx` +2,29—, los dos primeros
     de los más pequeños del estudio, y **ningún modelo grande empeora**. Es más modesto que lo publicado y
     es verdadero.

   **Esperar a que se resuelva `§F85` antes de escribir las cifras definitivas**, porque el punto que más
   pesa en el análisis es justamente el que arrastra los diecisiete ceros del `TypeError`.
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
