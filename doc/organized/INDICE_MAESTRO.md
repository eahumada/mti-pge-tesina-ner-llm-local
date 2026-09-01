# ÍNDICE MAESTRO DE DOCUMENTOS
## Proyecto de Tesina MTI — SIIG PGE-25

**Estudiante:** Eduardo Mauricio Ahumada Gallardo  
**Título:** Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo Corporativo Mediante un LLM Ejecutado Localmente con Soberanía de Datos  
**Profesor Guía:** José Luis Martí Lara  
**Última Actualización:** 2026-07-04  

---

## Estructura de Carpetas

```
doc/organized/
├── INDICE_MAESTRO.md                        ← Este archivo
├── Hito_1_Perfil_Proyecto/                  ← Formulario de perfil de postulación
├── Hito_2_Tarea1_Revision_Bibliografica/    ← Marco teórico y bibliografía inicial
├── Hito_3_Tarea2_Propuesta_Tesina/          ← Propuesta formal de tesina
├── Hito_4_Tarea3_Informe_Avance/            ← Informe de Avance Nº2 y benchmark
├── Hito_5_Tarea4_Informe_Final/             ← Informe final, requisitos, HU, referencias
├── Instructions/                             ← Formularios y guías oficiales del programa
└── Presentations/                            ← Slides de defensa y SIIG
```

---

## Resumen por Hito

### Hito 1 — Perfil de Proyecto (2026-03-07)
> Formulario de perfil de la tesina para postulación al programa PGE-25.

| Archivo Clave | Tipo | Fecha |
| :--- | :---: | :---: |
| `Formulario-perfil-tesina.docx-2.pdf` | PDF | 2026-03-07 |
| `Formulario-perfil-tesina.docx-2.md` | MD | 2026-06-27 |

📂 Ver índice completo: [Hito_1_Perfil_Proyecto/INDEX.md](./Hito_1_Perfil_Proyecto/INDEX.md)

---

### Hito 2 — Tarea 1: Revisión Bibliográfica (2026-02-12)
> Marco teórico y estado del arte inicial del proyecto de tesina.

| Archivo Clave | Tipo | Fecha |
| :--- | :---: | :---: |
| `TAREA N1 Marco Teórico y Estado del Arte del Proyecto de Tesina.docx` | DOCX | 2026-02-12 |

📂 Ver índice completo: [Hito_2_Tarea1_Revision_Bibliografica/INDEX.md](./Hito_2_Tarea1_Revision_Bibliografica/INDEX.md)

---

### Hito 3 — Tarea 2: Propuesta de Tesina (2026-04-17)
> Formulación y entrega formal de la propuesta del proyecto de tesina a la Universidad.

| Archivo Clave | Tipo | Fecha |
| :--- | :---: | :---: |
| `TAREA_N2_Formulacion_Propuesta_Tesina_EXPANDIDA_USM.pdf` | PDF | 2026-04-17 |
| `TAREA_N2_Formulacion_Propuesta_Tesina_EXPANDIDA_USM.md` | MD | 2026-07-01 |

📂 Ver índice completo: [Hito_3_Tarea2_Propuesta_Tesina/INDEX.md](./Hito_3_Tarea2_Propuesta_Tesina/INDEX.md)

---

### Hito 4 — Tarea 3: Informe de Avance Nº2 (2026-07-04)
> Resultados del benchmark experimental (15 modelos, N=30 artículos) y entrega del formulario IA-26.

| Archivo Clave | Tipo | Fecha |
| :--- | :---: | :---: |
| `Informe-Avance-2-v2.md` | MD | 2026-07-04 |
| `Formulario-IA-26-Rellenado.docx` | DOCX | 2026-07-01 |
| `benchmark_results_consolidated.md` | MD | 2026-07-01 |
| `referencia_datasets_nlp.md` | MD | 2026-07-01 |

📂 Ver índice completo: [Hito_4_Tarea3_Informe_Avance/INDEX.md](./Hito_4_Tarea3_Informe_Avance/INDEX.md)

**Resultados clave del Hito 4:**
- `gemma4:31b`: F1=79.03%, Recall=89.1%, Hallucination=0.0% (N=30)
- `gemma4:31b-mlx`: F1=77.47%, Recall=87.2%, Hallucination=0.0% (N=30)
- ANOVA: F=0.141, p=0.708 (sin diferencia estadística significativa entre modelos)

---

### Hito 5 — Tarea 4: Informe Final (Pendiente — entrega 2026-07-31)
> Documentación completa del proyecto: análisis, requisitos, historias de usuario y referencias bibliográficas.

| Archivo Clave | Tipo | Fecha |
| :--- | :---: | :---: |
| `2026-07-01_THESIS_PROJECT_ANALYSIS_REPORT.md` | MD | 2026-07-01 |
| `2026-07-01_EXECUTIVE_SUMMARY.md` | MD | 2026-07-01 |
| `2026-07-01_DEFENSE_CHECKLIST.md` | MD | 2026-07-01 |
| `2026-07-01_WORKLOG.md` | MD | 2026-07-01 |
| `2026-07-01_F1_IMPROVEMENT_ROADMAP.md` | MD | 2026-07-01 |
| `referencias/2026-06-28_bibliography.bib` | BIB | 2026-06-28 |
| `historias_de_usuario/` (21 HU) | MD | 2026-06-28 |
| `requisitos/` (42 REQ) | MD | 2026-06-27/28 |

📂 Ver índice completo: [Hito_5_Tarea4_Informe_Final/INDEX.md](./Hito_5_Tarea4_Informe_Final/INDEX.md)

---

### Carpetas Auxiliares

| Carpeta | Descripción |
| :--- | :--- |
| [Instructions/](./Instructions/INDEX.md) | Formularios y guías oficiales del programa SIIG-PGE25 (2024-2026) |
| [Presentations/](./Presentations/INDEX.md) | Slides de defensa oral y material del SIIG |

---

## Línea de Tiempo del Proyecto

```
2026-02-12  Entrega Tarea 1 — Marco Teórico y Revisión Bibliográfica
2026-03-07  Entrega Hito 1 — Perfil de Proyecto (postulación PGE-25)
2026-04-17  Entrega Tarea 2 — Propuesta Formal de Tesina (USM)
2026-06-27  Creación de 42 Requisitos Formales (REQ01–REQ42)
2026-06-28  Creación de 21 Historias de Usuario (HU01–HU21) + Referencias
2026-06-29  Corrida de Benchmark de Ablación (4 prompts × Gemma4)
2026-07-01  Corrida del Benchmark Completo (15 modelos × Kleptotrace/CoNLL-2002 N=15)
            Generación de Reportes Analíticos y Documentación de Defensa
2026-07-01  Entrega Formulario IA-26 (Informe de Avance Nº2) — Word
2026-07-04  Informe de Avance Nº2 versión final en Markdown (N=30, F1=79%)
2026-07-31  [PENDIENTE] Entrega Informe Final de Tesina
2026-08-??  [PENDIENTE] Defensa Oral ante Comisión Examinadora
```
