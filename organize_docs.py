import os
import shutil

# Rutas principales
root_dir = "/Users/eahumada/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local"
doc_dir = os.path.join(root_dir, "doc")

# Estructura de carpetas a crear en doc/
folders = [
    "equipo_remoto",
    "revisiones_y_entregas",
    "prompts",
    "historico",
    "defensa",
    "seguridad",
    "investigacion",
    "scripts"
]

for folder in folders:
    os.makedirs(os.path.join(doc_dir, folder), exist_ok=True)

# Mapeo de archivos de la raiz a sus respectivas carpetas en doc/
moves_from_root = {
    "ADENDA-EQUIPO-REMOTO-20260906.md": "equipo_remoto",
    "ALERTA-EQUIPO-REMOTO-20260906.md": "equipo_remoto",
    "ENCARGO-CIERRE-EQUIPO-48GB-20260910.md": "equipo_remoto",
    "ENCARGO-EQUIPO-48GB-SOLO-CORRIDAS-VALIDAS-20260909.md": "equipo_remoto",
    "ENCARGO-REMOTO-GPTOSS-20260907.md": "equipo_remoto",
    "ENCARGO-REMOTO-N30-20260907.md": "equipo_remoto",
    "PROMPT-EQUIPO-REMOTO-48GB.md": "equipo_remoto",
    "PROMPT-EQUIPO-REMOTO-RECORRIDA-COMPLETA-20260908.md": "equipo_remoto",
    "URGENTE-REMOTO-RECORRIDA-20260906.md": "equipo_remoto",

    "CAMBIOS-DESDE-ENVIO-PROFESOR-20260908.md": "revisiones_y_entregas",
    "ANALISIS-ACTUALIZACIONES-INFORME-FINAL_20260903.md": "revisiones_y_entregas",
    "AUDITORIA_CONSISTENCIA_20260903.md": "revisiones_y_entregas",
    "CIERRE-BENCHMARKS-20260907.md": "revisiones_y_entregas",
    "CIERRE-RECORRIDA-PROCEDIMIENTO.md": "revisiones_y_entregas",
    "CORRECCION-B1-SUMMARIES-20260907.md": "revisiones_y_entregas",
    "CORRECCION-QWEN3-THINKING-20260906.md": "revisiones_y_entregas",
    "DECISION-ESTADISTICA-20260909.md": "revisiones_y_entregas",
    "DECISIONES-PENDIENTES-20260908.md": "revisiones_y_entregas",
    "ESTADO-RECORRIDA-20260908.md": "revisiones_y_entregas",
    "INFORME-AVANCE-20260906.md": "revisiones_y_entregas",
    "INVENTARIO-AFECTADO-POR-F86-20260909.md": "revisiones_y_entregas",
    "INVENTARIO-DATOS-INCORRECTOS-20260908.md": "revisiones_y_entregas",
    "NOTA-NUEVA-REVISION-20260917.md": "revisiones_y_entregas",
    "PROPAGACION-PENDIENTE-DOCX-20260908.md": "revisiones_y_entregas",
    "RECOMENDACIONES-EJECUCIONES-FUTURAS.md": "revisiones_y_entregas",
    "REPORTE-SESION-20260906.md": "revisiones_y_entregas",
    "VEREDICTO-REVISION-GLOBAL-20260908.md": "revisiones_y_entregas",

    "PROMPT-CLAUDE-DESKTOP-20260907.md": "prompts",
    "PROMPT-CLAUDE-DESKTOP-DOCX-Y-PDF-20260909.md": "prompts",
    "PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md": "prompts",
    "PROMPT-CLAUDE-DESKTOP-PROPAGACION-20260907.md": "prompts",
    "PROMPT-CLAUDE-DESKTOP-RESINCRONIZACION-20260908.md": "prompts",
    "PROMPT-PENDIENTE-INFORME-FINAL.md": "prompts",

    "HISTORIAL-CONSOLIDADO.md": "historico",
    "BACKLOG.md": "historico",
    "WORKLOG.md": "historico",
    "TODO-INFORME-FINAL.md": "historico",
    "TODO.md": "historico",
    "REPORTS_INDEX.md": "historico",
    "THESIS_PROJECT_ANALYSIS_REPORT.md": "historico",
    "EXECUTIVE_SUMMARY.md": "historico",

    "DEFENSA-PREGUNTAS-Y-RESPUESTAS.md": "defensa",
    "DEFENSE_CHECKLIST.md": "defensa",

    "SEGURIDAD-CLAVE-GOOGLE-20260908.md": "seguridad",
    "SOLICITUD-GITHUB-PURGA-20260908.md": "seguridad",

    "GEMMA_MODELS_INVESTIGATION.md": "investigacion",
    "GEMMA_QUICK_START.md": "investigacion",
    "F1_IMPROVEMENT_ROADMAP.md": "investigacion"
}

# Archivos de doc/ que también queremos mover
moves_from_doc = {
    "DATASET_RESEARCH.md": "investigacion",
    "RESEARCH_INCONTEXT_BATCHING_AND_MILESTONES.md": "investigacion",
    "INTEGRATION_RESULTS.md": "historico",
    "REQUIREMENTS_SUMMARY.md": "historico",
    "TRACEABILITY_MATRIX.md": "historico",
    "check_remaining_stories.py": "scripts",
    "generate_reqs.py": "scripts",
    "generate_todo_from_hu.py": "scripts",
    "generate_user_stories.py": "scripts"
}

for filename, folder in moves_from_root.items():
    src = os.path.join(root_dir, filename)
    dst = os.path.join(doc_dir, folder, filename)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {filename} -> doc/{folder}/")

for filename, folder in moves_from_doc.items():
    src = os.path.join(doc_dir, filename)
    dst = os.path.join(doc_dir, folder, filename)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {filename} -> doc/{folder}/")

print("Done organizing.")
