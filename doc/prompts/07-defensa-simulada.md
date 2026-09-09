# Revisión como profesor guía y comisión evaluadora — simulación de defensa

**Solo lectura. Este prompt no modifica nada.** Es una revisión crítica que devuelve fortalezas, mejoras y
preguntas de defensa; no edita ficheros, no corrige el informe y no propone eliminar contenido. Quien lo
ejecute entrega un informe y nada más. Las correcciones que se deriven se deciden después, con el criterio
del autor y por los cauces habituales.

**Cuándo usarlo.** Cuando un capítulo esté redactado y se quiera contrastarlo con el estándar de la defensa,
antes de darlo por cerrado. Es complementario de `03-integridad-metrica.md`, que verifica las cifras: este
mira el argumento.

**Cómo usarlo: por capítulos, no entero.** Ingresar secciones concretas —«Metodología», «Estado del arte»,
«Análisis de resultados»— en lugar de la tesina completa. Un texto largo satura el contexto y diluye la
crítica, que es justo lo que se busca de este prompt.

**Ajuste según la sección.** Si lo que se envía es el marco teórico, sustituir el criterio 1 por la
exhaustividad y actualidad de la revisión bibliográfica, en lugar del rigor arquitectónico.

---

## El prompt

> Actúa como un profesor guía exigente y como una comisión evaluadora de nivel de posgrado para una tesis de
> Magíster en Tecnologías de la Información. Tu objetivo es revisar críticamente el texto o capítulo que te
> proporcionaré a continuación y entregar un feedback estructurado, riguroso y accionable.
>
> Evalúa el documento bajo los siguientes criterios, considerando el estándar académico requerido para
> proyectos de grado enfocados en Inteligencia Artificial Generativa, modelos de lenguaje locales (ej.
> Ollama) y arquitecturas RAG (Retrieval-Augmented Generation):
>
> 1. **Rigor Técnico y Metodológico:** ¿Es sólida y replicable la metodología? ¿Se justifican adecuadamente
>    las decisiones arquitectónicas y la elección de los modelos frente al problema planteado? ¿El
>    procesamiento de los datos (ej. financieros o de noticias) está bien fundamentado?
> 2. **Análisis Crítico y Limitaciones:** ¿El texto reconoce adecuadamente las limitaciones de hardware,
>    sesgos del modelo o cuellos de botella en la recuperación de información (RAG)?
> 3. **Estructura y Redacción Académica:** ¿El hilo conductor es claro? ¿La redacción mantiene la formalidad,
>    concisión y precisión técnica propia de una tesis de magíster? Señala párrafos confusos o redundantes.
> 4. **Preguntas de la Comisión Evaluadora (Simulación de Defensa):** Asume el rol de la mesa revisora y
>    formula 4 preguntas incisivas, críticas o «trampa» que buscarían evidenciar debilidades en la propuesta,
>    la seguridad de la arquitectura o la evaluación de los resultados.
>
> **Formato de salida esperado:**
>
> - **Fortalezas clave:** breve resumen de lo que funciona bien en el texto.
> - **Áreas críticas de mejora:** puntos específicos a corregir, reescribir o profundizar, con ejemplos de
>   cómo mejorarlos.
> - **Preguntas de la mesa:** las 4 preguntas críticas para preparar la defensa.
>
> **Restricción:** no modifiques ningún fichero. Esta revisión es aditiva y constructiva: aporta sugerencias
> productivas y no elimina ni reescribe contenido. Si detectas algo que parece un error de dato, señálalo
> como hallazgo a verificar, no como corrección a aplicar.
>
> Aquí está el texto a revisar:
> `[INSERTAR AQUÍ EL TEXTO O CAPÍTULO]`

---

## Notas de este proyecto, para quien lo ejecute

Tres cosas que conviene tener presentes al leer las respuestas que devuelva:

**Un hallazgo suyo es una hipótesis.** Vale la misma regla que para los demás prompts de esta biblioteca: si
señala una cifra como sospechosa, se comprueba contra `results/` antes de tocar nada. En este proyecto una
auditoría automatizada llamó «duplicado» a una fila que eran dos configuraciones legítimas del mismo modelo.

**No propondrá eliminar, y si lo hace no se le hace caso.** La política es aditiva. Si un recuento no cuadra,
se corrige el recuento.

**El informe tiene ya sus reparos conocidos**, y conviene no confundir una crítica nueva con una vieja ya
atendida: el profesor guía devolvió cuatro —bloques en blanco y saltos de página, ficha del estudiante en la
primera hoja, poco desarrollo con secciones de un solo párrafo, y marco conceptual pobre sin comparar
metodologías—. Están registrados en `TODO-INFORME-FINAL.md`.
