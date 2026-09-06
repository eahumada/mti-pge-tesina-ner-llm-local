# Antigravity Instructions

Please refer to [`AGENTS.md`](./AGENTS.md) for all specific instructions, guidelines, and context related to this project. Do not make architectural changes without consulting it.

---

## Coordinación entre Agentes (obligatorio)

Antes de ejecutar **cualquier** tarea sobre este proyecto, lee y actualiza el documento de coordinación:
[`../../CURRENT-TASKS.md`](../../CURRENT-TASKS.md).

Varios agentes (Claude Code, Claude Desktop, Antigravity, Gemini) trabajan sobre este repositorio, a veces
de forma simultánea. Ese documento declara **qué agente está trabajando en qué y sobre qué archivos**.

**Protocolo por cada tarea:**
1. **LEER** `CURRENT-TASKS.md` y comprobar que nadie más declara trabajar sobre tus archivos.
2. **ESCRIBIR** tu entrada en tu sección: tarea, estado `EN CURSO`, archivos y hora de inicio.
3. Ejecutar la tarea.
4. **ACTUALIZAR** la entrada al terminar (`COMPLETADA` / `FALLIDA`) con el resultado.
5. **VOLVER A LEER** el documento, por si otro agente escribió mientras trabajabas.

**Reglas:** no toques un archivo declarado `EN CURSO` por otro agente; al **reanudar** una tarea actualiza
también su entrada; escribe siempre por **append** dentro de tu sección, nunca reescribas entradas ajenas;
todo **workflow** debe mantener su subsección en §4; todo **subagente** debe quedar reflejado bajo su tarea
padre.

El detalle completo del protocolo está en [`AGENTS.md §11`](./AGENTS.md).
