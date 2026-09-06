# Instrucciones para Gemini — Proyecto Tesina NER MTI

Este archivo es el punto de entrada para agentes basados en Gemini (incluido Antigravity) que trabajen en
la **raíz** del proyecto. Las directivas técnicas del banco de pruebas están en
[`repos/ner-llm-entity-benchmark/GEMINI.md`](./repos/ner-llm-entity-benchmark/GEMINI.md) y en
[`repos/ner-llm-entity-benchmark/AGENTS.md`](./repos/ner-llm-entity-benchmark/AGENTS.md).

## Directivas del proyecto

- **Documentación estrictamente aditiva:** nunca se sobrescribe ni se elimina documentación existente al
  añadir hallazgos de una sesión. Si un conteo no cuadra, se corrige el conteo, no los datos.
- **Trazabilidad:** toda cifra citada en la tesina debe corresponder a un archivo versionado bajo
  `repos/ner-llm-entity-benchmark/results/`.
- **Entregables:** el `.docx` canónico y sus versiones congeladas se describen en
  [`CLAUDE.md`](./CLAUDE.md) y en [`doc/versions/informe_final/VERSIONES.md`](./doc/versions/informe_final/VERSIONES.md).
- **No regenerar los `.docx` con pandoc:** contienen correcciones manuales de numeración multinivel,
  estilos de fila y saltos de página que una regeneración destruiría.


---

## Coordinación entre Agentes — `CURRENT-TASKS.md`

En la raíz del proyecto existe un documento vivo de coordinación: [`CURRENT-TASKS.md`](./CURRENT-TASKS.md).
Declara **qué agente está trabajando en qué y sobre qué archivos**, con secciones separadas para
**Claude Code** (§1), **Claude Desktop** (§2), **Antigravity** (§3) y **Workflows** (§4).

### Protocolo obligatorio — para cada tarea

1. **LEER** `CURRENT-TASKS.md` antes de empezar y comprobar que ningún otro agente declara estar
   trabajando sobre los archivos que se van a tocar.
2. **ESCRIBIR** la entrada propia en la sección del agente correspondiente: tarea, estado `EN CURSO`,
   archivos afectados y hora de inicio.
3. Ejecutar la tarea.
4. **ACTUALIZAR** la entrada al terminar: `COMPLETADA` o `FALLIDA`, con el resultado.
5. **VOLVER A LEER** el documento, por si otro agente escribió mientras tanto.

### Reglas

- Si un archivo figura como `EN CURSO` por otro agente, **no tocarlo**: esperar o elegir otro.
- Al **reanudar** una tarea interrumpida, actualizar también su entrada (estado y motivo de la interrupción).
- Escribir siempre por **append** dentro de la propia sección; nunca reescribir entradas ajenas.
- **Todo workflow** debe tener su subsección en §4 (objetivo, fases, agentes, archivos tocados y resultado)
  y mantenerla actualizada.
- **Todo subagente** debe quedar reflejado bajo la tarea padre que lo lanzó.
- Releer el archivo **inmediatamente antes** de escribir: `ListAgents` enumera las sesiones de Claude Code
  pero **no** las de Claude Desktop, así que la ausencia de pares en el listado no prueba que nadie más
  esté editando.

El detalle completo del protocolo, junto con las políticas de orquestación de workflows y de concurrencia
entre sesiones, está en [`CLAUDE.md`](./CLAUDE.md).
