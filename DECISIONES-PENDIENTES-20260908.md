# Decisiones que esperan al autor

**2026-09-08, 18:55.** Reunidas aquí porque estaban repartidas entre `FINDINGS.md`, `CURRENT-TASKS.md` y
tres documentos sueltos, mezcladas con decisiones ya tomadas. Son **cinco**, ninguna urgente, todas con
recomendación. Ninguna bloquea a la otra.

---

## 1. ¿El informe adopta ya F = 35,5557, o espera al consolidado nuevo?

**Qué pasa.** El ANOVA publicado (F = 38,2222, p = 3,4453e-160) se calculó **incluyendo los siete artículos
contaminados** que la propia decisión del 2026-09-08 manda excluir. Sin ellos: **F = 35,5557,
p = 3,6729e-148**, sobre 2 938 observaciones en lugar de 3 120.

**Lo que no cambia:** ninguno de los trece modelos cambia de veredicto. Siguen siendo `nemotron-mini:4b` y
`llama3.2:latest` los dos únicos con mejora significativa. **Lo que sí:** el efecto del RAG se encoge en doce
de los trece.

**Recomendación: esperar.** La re-corrida completa va a sustituir el consolidado entero, así que adoptar la
cifra ahora es trabajo que se hace dos veces. El riesgo de esperar es nulo mientras no se entregue.
**Salvo que haya que entregar antes de que termine la re-corrida**, en cuyo caso hay que adoptarla, porque el
informe no puede publicar una cifra calculada sobre una población que él mismo declara excluida.

Evidencia: `FINDINGS §F66`.

---

## 2. Los nueve respaldos con nombres de modelos excluidos

**Qué pasa.** De los 36 `.bak_prescore` —instantáneas anteriores a la corrección de puntuación—, doce se
versionaron hoy por ser única copia y estar limpios. **Nueve contienen nombres de modelos excluidos** y
siguen sin versionar, es decir, **sin respaldo**: si alguien los borra, no hay vuelta.

**La tensión es real.** La política prohíbe esos nombres en ficheros de datos versionados; pero también
manda conservar los artefactos que atestiguan, y un respaldo histórico es de esa clase.

**Recomendación: decidir explícitamente, en cualquier sentido.** Lo que no conviene es el estado actual, que
es «ni una cosa ni otra»: fuera de la política y sin respaldo. Si se versionan, conviene una nota que
explique por qué esos nombres siguen ahí.

Evidencia: `FINDINGS §F67.bis`.

---

## 3. Los dos ficheros JSON que el barrido de exclusión dejó ilegibles

**Qué pasa.** `results/excluidos_n120_REMOTO/detailed_results.json.bak_prescore` tiene **240 de 480** claves
`"model"` sin valor, y su `benchmark_summary.json.bak_prescore` perdió una clave de primer nivel. Los rompió
la retirada de nombres, hecha por sustitución de texto. **Las otras 240 filas son de `gpt-oss:20b` y están
intactas**, atrapadas dentro de un fichero que ya no se puede cargar.

**Recomendación: reparar quedándose con las filas cuyo `model` tenga valor**, y anotar dentro del fichero
cuántas se retiraron y por qué. Eso deja un JSON válido, respeta la exclusión y salva lo salvable. No lo hice
por iniciativa propia porque implica decidir qué pasa con las 240 del modelo excluido.

Evidencia: `FINDINGS §F70`.

---

## 4. Las cuatro filas sin corrida de origen de `BENCHMARKS.md`

**Qué pasa.** Único bloqueante del `TODO §10` que sigue abierto, de los ocho —los otros siete están cerrados.
Son cuatro filas de configuraciones de prompt cuyas cifras no son trazables a ningún artefacto. Ya están
marcadas con su advertencia, y **el informe no las usa**: su Tabla 5 publica la corrida catalogada.

**Recomendación: dejarlas donde están, con su advertencia.** No bloquean la defensa. Retirarlas también sería
defendible; lo que no lo sería es publicarlas sin la advertencia, y eso ya está resuelto.

---

## 5. Quién propaga los 22 commits a los tres `.docx`, y cuándo

**Qué pasa.** Los tres `.docx` están congelados en el commit de las 04:25 y el Markdown ha recibido 22
commits desde entonces. **El entregable no es el informe.** Y lo más delicado no es lo que falta sino lo que
dice: su §3.3 afirma «el 65 %, 20 946 de 32 201», que es la cifra del Anexo I sobre 42 configuraciones
aplicada a una sección que habla del estudio.

**Recomendación: propagar antes de cualquier entrega, y no con pandoc.** La lista exacta, con ubicaciones,
está en `PROPAGACION-PENDIENTE-DOCX-20260908.md`. Conviene esperar a que termine la re-corrida para no
propagar dos veces, **salvo** que haya entrega antes.

---

## Y un aviso que todavía no es decisión

Con tres de los trece modelos rehechos, el efecto del KB RAG **cambia de signo en los dos de 31B**: de −0,53
y −0,18 a +0,81 y +0,97. Si eso se confirma con los trece, la frase de §5.3.1 que dice que el beneficio «se
anula o revierte en los de mayor capacidad» **habrá que reformularla**. No hay nada que decidir todavía, pero
conviene no encontrárselo el último día. Evidencia: `FINDINGS §F68`.
