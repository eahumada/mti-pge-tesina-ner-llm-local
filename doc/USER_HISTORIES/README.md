# Historias de Usuario (User Histories Index)

Este directorio contiene las especificaciones detalladas de las **Historias de Usuario (HU)** formuladas para el proyecto de tesis MTI. Cada historia de usuario está vinculada a requisitos funcionales y no funcionales del sistema y se traduce en tareas accionables en el archivo `TODO.md`.

---

## 🗺️ Matriz de Relaciones: Requisitos $\rightarrow$ Historias de Usuario $\rightarrow$ TODO Tasks

La siguiente tabla consolida la trazabilidad completa del proyecto, mostrando la relación entre los Requisitos del PRD, las Historias de Usuario (`HUnn.md`) y las tareas del `TODO.md` general.

| ID Historia | Título de la Historia | Requisitos Mapeados | Archivo de Historia | Estado en `TODO.md` |
| :---: | :--- | :--- | :---: | :---: |
| **HU01** | Dataset Ingestion & Validation | `FR1.1`, `FR5.1`, `FR5.3` | [HU01.md](HU01.md) | **Completado** |
| **HU02** | Ground Truth & Inter-Annotator Agreement | `FR1.2`, `FR1.3` | [HU02.md](HU02.md) | **Completado** |
| **HU03** | Single-Context RAG & local LLM Runner | `FR2.1`, `FR2.2`, `FR2.4`, `NFR1.1`, `NFR1.2`, `NFR5.1` | [HU03.md](HU03.md) | **Completado** |
| **HU04** | VRAM Weight Management | `NFR3.3`, `FR5.2` | [HU04.md](HU04.md) | **Completado** |
| **HU05** | Thread-Safe InMemory Queue & Batch Processing | `FR1.4`, `FR1.5`, `NFR4.2` | [HU05.md](HU05.md) | **Completado** |
| **HU06** | Redis Integration & Crash Resumability | `FR1.6`, `NFR4.3` | [HU06.md](HU06.md) | **Completado** |
| **HU07** | Fuzzy Entity Matching & Typed Metrics | `FR3.1`, `FR3.2`, `FR3.3`, `RF3.2` | [HU07.md](HU07.md) | **Completado** |
| **HU08** | Hallucination Detection & Confusion Matrix | `FR4.1`, `RF3.1` | [HU08.md](HU08.md) | **Completado** |
| **HU09** | ANOVA & Tukey Post-Hoc Analysis | `FR3.4`, `RF3.3` | [HU09.md](HU09.md) | **Completado** |
| **HU10** | Auditable Run Configs & Logs | `NFR5.2`, `NFR6.2`, `NFR6.1` | [HU10.md](HU10.md) | **Completado** |
| **HU11** | Streamlit Interactive Dashboard | `FR4.2`, `FR4.3` | [HU11.md](HU11.md) | **Completado** |
| **HU12** | Detailed Trace Explorer | `FR4.4`, `NFR6.1` | [HU12.md](HU12.md) | **Completado** |
| **HU13** | Cost & Resource Optimization | `NFR3.2`, `RNF2.2` | [HU13.md](HU13.md) | **Completado** |
| **HU14** | Performance & Processing Speed Bounds | `NFR3.1`, `RNF2.1` | [HU14.md](HU14.md) | **Completado** |
| **HU15** | Spanish & Latin American Localization | `NFR5.1`, `RNF5.1` | [HU15.md](HU15.md) | **Completado** |
| **HU16** | Automated System Acceptance Tests | `NFR7.1` | [HU16.md](HU16.md) | **Completado** |
| **HU17** | Sensitivity Analysis | `FR3.4` | [HU17.md](HU17.md) | **Completado** |
| **HU18** | Simulated Production Validation & Feedback | `FR4.2`, `FR4.3` | [HU18.md](HU18.md) | **Completado** |
| **HU19** | Fine-Grained Error Taxonomy | `REQ40` | [HU19.md](HU19.md) | **Completado** |
| **HU20** | Few-Shot Ablation Study | `REQ41` | [HU20.md](HU20.md) | **Completado** |
| **HU21** | Hardware Efficiency Index | `REQ42` | [HU21.md](HU21.md) | **Completado** |

---

## 🛠️ Estructura del Archivo de Historia (`HUnn.md`)

Cada historia de usuario individual contiene las siguientes secciones para asegurar el rigor de la ingeniería de software:
1. **Metadata:** Identificador (HUxx), Fase, Requisitos Asociados.
2. **Historia de Usuario (User Story):** Rol, funcionalidad y justificación comercial/académica.
3. **Criterios de Aceptación (Acceptance Criteria):** Checklist binario verificado durante la etapa de integración.
4. **Detalles de Implementación:** Ubicación del código fuente e invariantes asociadas.
