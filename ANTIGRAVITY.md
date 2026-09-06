# NER Benchmark Project Directives
## RAG Integration Policy
- **Strict Additive Documentation**: Never overwrite or delete existing documentation when adding new session findings. All documents (`BENCHMARKS.md`, `TODO.md`, `ROADMAP.md`, etc.) must be strictly additive. Verify via git history that no previous content is lost.
- **Comparative Study Value**: A difference of up to 0.02 in F1 Score when comparing Baseline vs RAG is tolerable and considered highly relevant information. Always preserve the RAG infrastructure and indexing work to allow alternate runs (with and without RAG) side-by-side.
- **Metric Degradation Rule**: A drop of up to 0.02 in F1 score is acceptable for the sake of comparison. However, continue evaluating whether further lists degrade precision. The goal is to accurately present the results of the study with and without RAG.
- **Optimal Analysis**: Always analyze the optimal configuration carefully before rolling out to the full 16-model benchmark sweep.


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
