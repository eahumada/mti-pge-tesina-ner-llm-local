# Versiones entregadas al profesor guía

Este directorio conserva **el artefacto exacto que se envió**, byte a byte, para que quede constancia de qué
leyó el profesor guía en cada momento y de qué correcciones son posteriores al envío.

---

## Envío del 2026-09-08

| | |
|:---|:---|
| **Fichero enviado** | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03_5.pdf` |
| **Copia conservada** | `2026-09-08_Informe_Final_Tesina_NER_ENVIADO-AL-PROFESOR-GUIA.pdf` |
| **SHA-256 del PDF** | `872d23993314247da8cca21ed86afe7e884ee14cd06c813969ced3da7ed6892f` |
| **DOCX de origen** | `efe56e1d7495…`, conservado junto al PDF con el mismo nombre base |
| **Versión interna** | `v11`, congelada por Claude Desktop |
| **Generado** | 2026-09-08 07:12 UTC |
| **Extensión** | **31 páginas: cuerpo 20, anexos 11** |
| **Estado del Markdown** | commit `448566c` |

La copia se ha verificado byte a byte contra el fichero que salió, y coincide. El PDF es además idéntico a
`doc/versions/informe_final/Informe_Final_Tesina_NER_v11.pdf` y a la copia de la raíz del proyecto.

### Cumplimiento de los límites institucionales

Los dos límites se cumplen con holgura: el **cuerpo va cinco páginas por debajo** de sus veinticinco, y los
anexos catorce por debajo de las veinticinco propias. El objetivo interno de veinticinco páginas totales no se
cumple, y conviene saber por qué: el Markdown creció de 15 915 a 19 549 palabras al atender los reparos del
profesor sobre el poco desarrollo y al incorporar las correcciones de la revisión. Claude Desktop comprobó
además que **la compactación por estilo está agotada**: una pasada agresiva sobre interlineados, encabezados,
leyendas y filas de tabla dio un resultado idéntico, 31/20/11, porque los cortes los manda ahora el contenido
y no el espaciado. Bajar de treinta y una páginas exigiría suprimir texto, y eso queda a decisión del autor.

### Qué correcciones incluye esta versión

Verificado sobre el XML del `.docx`, no sobre la fuente:

- Las **cuatro citas inexistentes sustituidas** por obras reales: Cañete y otros (BETO), Islam y otros
  (FinanceBench), Salinas Alvarado y otros (ALTA 2015) y Loukas y otros (FiNER, ACL 2022).
- **BloombergGPT** con su arquitectura real, BLOOM 50B, y F1 de 53,6 a 75,5 %.
- La **Tabla 2** con su columna renombrada a «Desempeño publicado» y su glosa de incomparabilidad.
- Los **nueve anexos A-I**, incluido el **Anexo I** con la medición restringida y sus cuarenta y nueve
  configuraciones.
- Las **diecinueve tablas** numeradas en orden de aparición con leyenda encima.
- El **idioma real de los tres corpus** declarado en el resumen, el abstract, el objetivo 2 y §4.1.
- Las **conclusiones 4, 5, 6 y 7** reformuladas, el **mecanismo nuevo de §6.1** y el **Anexo H.3** reescrito
  con la medición reproducible.

### Qué NO incluye, y es posterior al envío

Corresponde íntegramente al commit `7f820d2`, hecho después de generar el PDF. Son tres cosas y conviene
tenerlas presentes si el profesor comenta alguna:

1. **El Anexo B** transcribe tres ejemplos *few-shot* que no existen en el artefacto. El prompt que las
   corridas cargaron realmente contiene **dos**, y de contenido distinto. En la versión enviada siguen los
   tres antiguos.
2. **La fuente de los diccionarios** aparece atribuida a OpenSanctions en §5.6 y en el Anexo F; la fuente real
   es la lista SDN del Departamento del Tesoro de los Estados Unidos.
3. **La entrada [38]**, la ontología FollowTheMoney, no está: la versión enviada tiene **37 entradas** y el
   Markdown actual tiene 38.

Ninguna de las tres afecta a una cifra ni a una conclusión.
