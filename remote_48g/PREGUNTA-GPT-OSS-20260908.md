# `gpt-oss:20b` no está en el barrido: ¿deliberado o descuido?

**Del equipo principal al equipo de 48 GB. 2026-09-08, 20:42.** Conviene resolverlo antes de que termine la
re-corrida, no después.

`gpt-oss:20b` **no aparece en `_sweep_progress.log`**: ni START, ni END, ni SKIP. El barrido sigue el orden de
la Tabla 7 y salta del cuarto modelo (`gemma4:latest`) al sexto (`qwen2.5:14b`).

Suponemos que aplicasteis `FINDINGS §F44`, donde el autor decidió que «`gpt-oss:20b` se deja con think ON,
congelado; su corrida oficial no se re-ejecuta ni se toca». Es una lectura razonable, y por eso preguntamos en
lugar de corregir.

**Nuestra lectura es que esa decisión era sobre el *thinking*, no sobre el corpus.** Se tomó porque apagarle
el razonamiento le hace dejar de responder —`recall = 0` en 7 de 15 y en 10 de 15—, de modo que lo que
protegía era el régimen de razonamiento, no la versión del corpus con la que se mide.

**Lo que pasaría si no se re-ejecuta.** El consolidado final tendría doce modelos sobre el corpus con las 545
localizaciones anotadas y uno sobre el corpus antiguo. Su F1 quedaría unos veinte puntos por debajo del resto
**por un defecto del corpus y no por su desempeño**, porque los demás suben entre +19,75 y +22,22 al
corregirlo. En la tabla final parecería el peor de su franja sin serlo.

**Lo que proponemos:** re-ejecutarlo **con `think` ON**, que es lo que la decisión protege, sobre el corpus
corregido y con `max_tokens=4096` como los demás. Así se respeta `§F44` en lo que decía y se resuelve además
la asimetría de presupuesto de salida que hoy lo hace incomparable con los otros doce (`FINDINGS §F61.bis`).

**Aviso técnico:** `merge_and_analyze.py` exige ahora 26 grupos y se pararía con 24, así que esto no puede
colarse en silencio hasta el ANOVA. Pero descubrirlo al fusionar es mucho peor que decidirlo hoy.

Una corrección de paso: `§F44` dice que la corrida oficial de `gpt-oss:20b` es `results/excluidos_n120_REMOTO`,
y el consolidado publicado toma en realidad sus filas de `gptoss_rerun_REMOTO`. Esa frase está desactualizada
en nuestro propio documento.
