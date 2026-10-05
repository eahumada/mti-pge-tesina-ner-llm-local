# Encargo a Claude Desktop — resincronizar los `.docx` y el PDF con el Markdown canónico

**Fecha del encargo:** 2026-09-08. **Solicitado por:** el autor. **Estado del Markdown:** commit `448566c`.

## Por qué este encargo es urgente

Una segunda pasada de revisión independiente, con seis auditores y un orquestador, dictaminó que **el
documento que se entrega no es el documento corregido**. Dos auditores extrajeron el XML por separado y
coincidieron: los tres `.docx` y el PDF de la raíz conservan una bibliografía de **veinte entradas frente a
las treinta y siete** del Markdown, y entre esas veinte siguen figurando cuatro referencias que el Markdown
ya sustituyó por obras verificables y que ninguno de los dos auditores pudo localizar. Conservan además la
tabla del estado del arte con cifras que nadie ha publicado y una cita suelta en formato APA.

Conviene ser preciso en el enunciado, como lo fueron los auditores: no se afirma que esas cuatro referencias
fueran inventadas de forma deliberada, sino que **no son localizables** y que la fuente canónica ya las había
reemplazado. Eso basta para exigir la corrección sin acusar a nadie.

## Fuentes que hay que mirar, en este orden de autoridad

La **fuente canónica** es el Markdown, `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`.
Toda diferencia con los `.docx` se resuelve a favor del Markdown. Las **reglas del proyecto** están en
`CLAUDE.md`, con cuatro bloques nuevos escritos hoy sobre integridad de la medición, verificación previa al
commit, secretos y concurrencia. Las **normas institucionales** están en
`Instrucciones Informe Final de Tesina/`: `plantilla_final-2026.docx`, `tesinas-finales-2026.pdf` y
`ieee-citationref.pdf`. Y el **razonamiento detrás de cada corrección** está en `FINDINGS.md`, secciones
`§F51` a `§F56`, por si alguna decisión resulta discutible al aplicarla.

## Qué ha cambiado en el Markdown y hay que trasladar

**La bibliografía pasó de veinte a treinta y siete entradas, y las treinta y siete llevan URL verificada**,
abierta y contrastada una a una contra la ficha oficial de la obra. Cuatro entradas se sustituyeron porque no
correspondían a obra alguna: García y López por Cañete y otros (BETO, PML4DC en ICLR 2020), Chang, Kim y Park
por Islam y otros (FinanceBench), Smith, Johnson y Davis por Salinas Alvarado, Verspoor y Baldwin (ALTA 2015),
y Min y otros por Loukas y otros (FiNER, ACL **2022** y no 2023). Se corrigieron además errores de fondo en
otras cinco: la primera autora de [11] es Orevaoghene Ahia y no «T. Ahia»; el primer autor de [14] es Zihao
Zhao y no «A. Zhao»; el de [6] es Yunfan Gao y no «X. Gao»; el libro de [5] lo publica Packt y no O'Reilly; y
el corpus de [18] se titula *Kleptotrace-micro-dataset*, está depositado en Zenodo con DOI y el título que
figuraba era una descripción redactada como si fuera un título. El enlace de [12] devolvía 404 y se sustituyó
por su ficha en ACL Anthology.

**La tabla del estado del arte, que ahora es la Tabla 2, se reescribió por completo.** Su columna dejó de
titularse «F1», porque agrupaba métricas de tareas distintas como si fueran homogéneas, y pasó a «Desempeño
publicado», con una glosa que advierte que las filas no son comparables. Tres de sus cinco filas declaraban
cifras que nadie publicó: el 91 % de FiNER-139 es en realidad 82,1 % de micro-F1 y su tarea es etiquetado
numérico XBRL y no reconocimiento de personas y organizaciones; el 88 % del español corresponde a BETO y no a
XLM-R; y el 83 % de GPT-4 con recuperación es en realidad 50 %. Se corrigió también la atribución de
BloombergGPT, que el artículo declara BLOOM y no GPT-J, con F1 entre 53,6 y 75,5 y no «85 %+». Ninguna fila se
eliminó: todas se reescribieron con datos reales.

**Las diecinueve tablas están ahora numeradas de forma contigua en orden de aparición, cada una con su
leyenda inmediatamente encima**, como exige la plantilla. Antes había diecinueve tablas y solo cinco con
leyenda, numeradas de la doce a la dieciséis, mientras el texto citaba «Tabla 1», «Tabla 2» y «Tabla 5»,
números que ninguna leyenda definía. Se corrigió de paso que la misma tabla, el benchmark exploratorio, se
citaba como Tabla 2 en el cuerpo y como Tabla 5 en el Anexo E.

**Las siete conclusiones se reformularon sobre datos verificados**, y esta es la parte que más cuidado exige
al maquetar, porque cambian de extensión. La primera declara el idioma de cada corpus y ambas convenciones de
medición. La segunda pasa de presentar +10,40 puntos como resultado a declararlo tendencia no replicada,
porque existen tres corridas del mismo experimento y las otras dan +3,11 y −0,43 con p = 0,9328. La tercera
abandona la equivalencia local-nube y declara que la soberanía cuesta unos cinco puntos de F1. La cuarta
declara que las cifras económicas son estimaciones y no mediciones. La quinta retira la prevención de
desbordamientos de VRAM, que el controlador no puede hacer porque no recibe telemetría de memoria. La sexta
corrige «los dos más débiles» y declara que la relación inversa entre capacidad y beneficio es una tendencia
no significativa. Y la séptima sustituye un rango irreproducible por dos efectos opuestos y medidos.

**Hay un anexo nuevo, el Anexo I**, con cuarenta y nueve filas: cada configuración del corpus N=120 con su
cifra publicada y su equivalente restringido a las categorías que el corpus anota. Es la decisión del autor
sobre el hallazgo `§F53`: publicar en columna paralela sin sustituir ni borrar nada. **El Anexo H.3 se
reescribió** con la medición del script `repos/ner-llm-entity-benchmark/tools/analisis_mojibake.py`, que se
publica precisamente para que esa tabla sea reproducible; la versión anterior declaraba una partición de 88 y
31 artículos, cuya suma es 119 y no 120. El **Anexo G** declaraba veinte commits entre el 29 de junio y el 1
de septiembre cuando hay más de ciento treinta, y el **G.4** afirmaba que el estudio principal cubre cinco
modelos cuando cubre trece. En el capítulo 5 había **dos «Hallazgo 4»**, y el segundo pasó a ser el cinco. El
resumen y el abstract se reescribieron enteros, quedan en 199 y 189 palabras y **dicen exactamente lo mismo**.
Y el trabajo futuro tiene tres líneas nuevas, la octava, la novena y la décima.

## Cómo hacerlo, y una tensión que hay que resolver con criterio

`CLAUDE.md` prohíbe regenerar los `.docx` con pandoc, y la razón es buena: contienen correcciones manuales de
numeración multinivel (`numId=0`), estilos de fila y saltos de página que una regeneración destruiría. La vía
prevista es `tools/docx_replace_terms.py`, que edita el XML preservando el formato.

**El problema es que el volumen de cambio de esta ronda desborda esa herramienta**: diecisiete entradas
bibliográficas nuevas, un anexo entero de cuarenta y nueve filas, la renumeración de diecinueve tablas con sus
leyendas y siete conclusiones reescritas no son sustituciones de términos. Esta tensión es real y la decisión
es tuya, pero la recomendación es no regenerar: aplicar por edición dirigida del XML lo que sea sustitución de
texto o de filas, e **insertar el Anexo I y las leyendas como bloques nuevos**, conservando los estilos
existentes. Si concluyes que no hay forma de hacerlo sin regenerar, dilo antes de empezar y que lo decida el
autor: perder la numeración multinivel corregida a mano costaría más que rehacer la maquetación.

## Reglas que el documento generado tiene que cumplir

El cuerpo no puede exceder **veinticinco páginas** sin contar anexos, y hay presupuesto: la última medición
daba diecinueve. Los anexos no cuentan y pueden ocupar hasta veinticinco más. El **resumen y el abstract van
fundidos en la primera página**, sincronizados y por debajo de doscientas palabras cada uno. Las **leyendas
van encima** de sus tablas. **Nada de emojis, marcas de agua, sellos de borrador ni arte ASCII**: donde un
símbolo hacía de valor se escribe la palabra. Y los **guiones largos y las negritas se mantienen al mínimo**
en el cuerpo: cuéntalos en el documento generado y compáralos con los de la fuente, porque el renderizador no
debe añadir énfasis al restituir estilos ni al aplicar la plantilla. Sobre los recuentos absolutos, un aviso
que ahorra discusiones: **no son reproducibles entre métodos de conteo distintos** —tres auditores dieron
19/108, 28/127 y 31/150 sobre el mismo texto, según incluyeran o no tablas, citas y encabezados—, de modo que
lo que importa es que el generado no añada énfasis respecto de la fuente, no acertar con una cifra concreta.

Quedan además cinco tareas de maquetación que los auditores señalaron y que no dependen de esta
resincronización: sustituir la cita en formato APA que queda en el cuerpo, restituir la numeración de las
listas anuladas con `numId=0`, devolver el margen superior a 2,50 centímetros, quitar la numeración de los
títulos de «Referencias» y «Anexos», e insertar el salto de página antes de los anexos.

## Verificación antes de dar por cerrado el trabajo

Sobre el `.docx` y sobre el PDF, no sobre el Markdown: que la bibliografía tenga **treinta y siete entradas**
y que ninguna de las cuatro retiradas siga presente; que la Tabla 2 sea la nueva, con su columna renombrada y
su glosa; que existan **diecinueve tablas con leyenda contigua** del uno al diecinueve; que el Anexo I esté
completo con sus cuarenta y nueve filas; que el resumen y el abstract quepan en la primera página y digan lo
mismo; que el cuerpo no pase de veinticinco páginas; y que no haya emojis ni marcas de agua. El PDF se
reexporta al final y se verifica sobre el PDF, porque el conteo de páginas del `.docx` y el del PDF no
siempre coinciden.

Los tres artefactos a resincronizar son `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`,
que es el entregable canónico con plantilla institucional, `Informe_Final_Tesina_NER.docx` y
`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx`, más el PDF
homónimo del primero. Haz **copia de seguridad de los cuatro antes de tocarlos** y declara la tarea en
`CURRENT-TASKS.md` §2 antes de empezar, como exige el protocolo de coordinación.
