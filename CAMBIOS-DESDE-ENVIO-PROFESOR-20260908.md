# Cambios desde el envío al profesor guía del 2026-09-08

**Documento de trabajo, no forma parte de la tesina.** Resume, en lenguaje simple, qué cambió en el informe
desde la versión enviada el 8 de septiembre de 2026 (`doc/versions/enviados/2026-09-08_Informe_Final_Tesina_NER_ENVIADO-AL-PROFESOR-GUIA.pdf`).
Sirve para que el autor pueda explicarle al profesor guía, en una conversación o por escrito, qué se corrigió
y por qué, sin tener que leer los más de 130 hallazgos técnicos registrados en `FINDINGS.md`. Se actualiza a
medida que avanza el trabajo; la fecha de "última actualización" al final de cada bloque indica su vigencia.

---

## 1. El defecto más importante: un tercio de los datos tenía dos errores de origen

El corpus real de 120 artículos (105 en español, 15 en inglés) que sostiene el resultado central del estudio
tenía, hasta el 8 de septiembre, dos defectos técnicos que **inflaban artificialmente los errores medidos**:

- **Codificación rota (*mojibake*).** Los nombres con tilde o «ñ» se guardaron mal (`JosÃ© Bono` en vez de
  `José Bono`) en el 20 % de las entidades y el 87 % de los artículos. El efecto no era parejo: premiaba a
  los modelos que copiaban la corrupción tal cual y castigaba a los que escribían el nombre bien.
- **Una categoría de entidad sin anotar.** Los modelos debían extraer personas, organizaciones y
  localizaciones, pero el corpus solo tenía anotadas las dos primeras. Cada localización correctamente
  extraída se contaba como un error. De ahí procedía dos tercios de todos los falsos positivos del estudio.

**Ambos defectos se corrigieron y todo el estudio se volvió a ejecutar completo el 8 de septiembre.** Las
cifras que hoy sostienen el informe (Tabla 7, 81,47 % / 82,44 % de F1 para el mejor modelo local) ya no
arrastran ninguno de los dos. El detalle técnico completo se conserva en los Anexos H e I del informe, y en
`FINDINGS.md §F53` a `§F58`, `§F157` y `§F166`.

*Última actualización: 2026-09-17.*

---

## 2. Corrección de método estadístico

Varias piezas del análisis estadístico original tenían defectos que no cambiaban la conclusión principal
pero sí exigían corrección:

- El diseño correcto es de **medidas repetidas** (los mismos 120 artículos se miden con cada modelo), y el
  ANOVA original no lo reflejaba; se verificó que el resultado se sostiene con el contraste correcto.
- La comparación entre modelos con y sin RAG mezclaba, en un párrafo, una cifra calculada por artículo
  (macro) con una calculada sobre el total del corpus (micro), presentándolas como equivalentes sin serlo.
- Se añadieron las pruebas de supuestos que faltaban (homocedasticidad con Levene/Brown-Forsythe) y el
  tamaño del efecto (Cohen's d) donde el informe solo daba significancia estadística sin magnitud.

*Última actualización: 2026-09-17.*

---

## 3. Limpieza de modelos y cifras que no correspondían al estudio

Seis modelos que en algún momento se probaron pero fueron excluidos por decisión del autor (uno por no ser
reproducible, otros por no formar parte del alcance final) seguían apareciendo en los tres `.docx` aunque ya
no estaban en el Markdown fuente. Se verificó y corrigió en los tres entregables. Se estableció además la
regla de que un modelo excluido no vuelve a incluirse ni se cita su cifra como resultado, ni siquiera como
caso extremo.

*Última actualización: 2026-09-17.*

---

## 4. Construcción de un verificador automático del informe

Se construyó `tools/verificar_informe.py`, que hoy corre 56 comprobaciones automáticas antes de cada commit
(numeración de tablas, bibliografía completa con URL verificada, que los tres `.docx` y el PDF digan lo mismo
que el Markdown, que ninguna cifra de una tabla sea inventada, etc.). Antes de que existiera, varios de los
defectos de las secciones 1-3 de este documento sobrevivieron semanas sin que nada los detectara. Ahora un
gancho de Git (`pre-commit`) lo ejecuta automáticamente y detiene el commit si aparece un fallo nuevo.

*Última actualización: 2026-09-17.*

---

## 5. Estudios nuevos de replicación (encargo al equipo remoto de 48 GB)

Entre el 14 y el 17 de septiembre se ejecutó un encargo completo de re-corridas con semillas aleatorias
declaradas, para comprobar si los hallazgos del informe se sostenían al repetir el experimento (algo que la
versión del 8 de septiembre no había hecho: cada resultado salía de una sola corrida). Resultado, resumido:

- **El hallazgo "redactar el prompt en español aporta +10,4 puntos de F1" no se sostiene como se creía.**
  Al investigarlo a fondo, se descubrió que 6 de esos 10,4 puntos procedían de un solo artículo que un
  modelo no pudo procesar en la corrida original (no es un efecto real del idioma). Replicado con 5 semillas
  sobre el corpus pequeño, el efecto es real pero bastante menor.
- **El beneficio del RAG contextual sobre el modelo más débil del estudio (+12,3 puntos) sí se sostiene**,
  replicado y confirmado sobre datos limpios.
- **El efecto de que el idioma del prompt coincida con el del texto se invierte entre corpus**: ayuda sobre
  el corpus pequeño de dominio, pero no sobre el corpus grande y real, donde otra configuración (*few-shot*
  en inglés) resulta más robusta pese a que el 87 % del corpus está en español. Es un hallazgo genuino, no
  un error: revela que el efecto depende del tipo de texto, algo que una sola corrida sobre un solo corpus
  no podía mostrar.
- **Se añadió un intervalo de confianza real (5 semillas) a la tabla central de resultados** (Anexo K nuevo),
  algo que el informe del 8 de septiembre no tenía: cada cifra salía de una única ejecución sin margen de
  error declarado. El intervalo confirma que las cifras publicadas son representativas y no casualidades de
  una corrida particular.

*Última actualización: 2026-09-17.*

---

## 6. Procedencia y validez del corpus

Se verificó y documentó con cita bibliográfica completa que 105 de los 120 artículos del corpus real
proceden de CoNLL-2002 en español (Tjong Kim Sang, 2002), no de una fuente sin verificar. Por separado, se
auditó la traducción al español del corpus sintético de 30 artículos (dominio AML/KYC): se encontraron y
corrigieron 7 de 8 discrepancias de traducción de entidades, y se documentó como limitación metodológica
declarada (no oculta) que la comparación de variantes de idioma sobre ese corpus traducido es válida para
lo que el estudio necesita, pero no para afirmar nada sobre español nativo.

*Última actualización: 2026-09-17.*

---

## 7. Una limitación metodológica descubierta y declarada, no resuelta

Se descubrió que el módulo de recuperación aumentada (RAG) usa solo 7 ejemplares de referencia, y que esos
ejemplares se solapan con el 94 % de los artículos que se usan para medir el propio sistema — es decir, hay
riesgo de que el modelo vea, de forma indirecta, la respuesta correcta de un artículo muy parecido al que se
le pide resolver. **No se ha corregido**: requiere una decisión del autor entre tres caminos (reconstruir los
ejemplares con material ajeno al corpus de evaluación, excluir esa comparación del informe, o declarar la
limitación tal como está). Documentado en el informe como limitación conocida, pendiente de decisión.

*Última actualización: 2026-09-17.*

---

## 8. Limpieza editorial

- Reducidos guiones largos y negritas del cuerpo a un uso excepcional, retirado el arte ASCII y los emojis,
  y comprimidos los pasajes que narraban en detalle defectos ya corregidos (dos meses de historia forense),
  dejando en el cuerpo solo la explicación necesaria para sostener la hipótesis.
- Ampliado el marco teórico (capítulo 2) en dos rondas, atendiendo un reparo directo del profesor guía sobre
  desarrollo insuficiente.
- Retirada una figura y una anécdota con datos no verificables, a petición expresa del autor.

*Última actualización: 2026-09-17.*

---

## Qué sigue pendiente

- Propagar la compresión de los Anexos H/I y las últimas correcciones a los tres `.docx` y al PDF de la raíz
  (requiere Word; encargado a Claude Desktop).
- Decisión del autor sobre el punto 7 (ejemplares del RAG).
- Revisión final de citas bibliográficas contra sus fuentes originales y pasada de simplificación de prosa
  densa, en curso al momento de escribir esto.
