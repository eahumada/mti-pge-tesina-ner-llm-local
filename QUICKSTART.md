# Guía Rápida de Inicio (Quickstart) — Tesina MTI & Banco NER-LLM

Bienvenido al repositorio del proyecto **Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo Corporativo Mediante Modelos de Lenguaje Grande Ejecutados Localmente con Soberanía de Datos**.

Esta guía detalla paso a paso cómo clonar, configurar el entorno, descargar datos, re-ejecutar benchmarks, lanzar el Dashboard interactivo con su chatbot local y auditar la consistencia del informe final.

---

## 📋 Requisitos Previos del Sistema

1. **Sistema Operativo:** macOS (optimizado para Apple Silicon M1/M2/M3/M4 con soporte Metal/MLX) o Linux (Ubuntu 22.04+ con GPU NVIDIA/AMD o CPU multinúcleo).
2. **Python:** Versión `3.10` a `3.14` (recomendado `3.12` o `3.14`).
3. **Gestor de Paquetes / Dependencias:** `pip`, `venv`, `git`, `curl`.
4. **Motor LLM Local:** [Ollama](https://ollama.com/) instalado y corriendo en local (`http://localhost:11434`).

---

## 🚀 Paso 1: Clonar y Preparar el Entorno

### 1.1 Clonar el repositorio
```bash
git clone https://github.com/eahumada/mti-pge-tesina-ner-llm-local.git
cd mti-pge-tesina-ner-llm-local
```

### 1.2 Configurar el entorno virtual del benchmark
El banco de pruebas y el Dashboard viven en la subcarpeta `repos/ner-llm-entity-benchmark/`:

```bash
cd repos/ner-llm-entity-benchmark

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS / Linux:
source venv/bin/activate
# En Windows (WSL o Git Bash):
# source venv/Scripts/activate

# Instalar dependencias Python
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

*(Opcional: puedes ejecutar alternativamente el script interactivo `./setup.sh` que detecta tu SO y automatiza este paso).*

---

## 🦙 Paso 2: Configurar Ollama y Descargar Modelos

Asegúrate de que el daemon de Ollama esté en ejecución. En macOS, basta con abrir la aplicación Ollama. En Linux:
```bash
ollama serve > /dev/null 2>&1 &
```

Verifica la conectividad:
```bash
curl http://localhost:11434/api/tags
```

### Descargar los modelos recomendados del estudio

Para utilizar las capacidades completas (Benchmarks + Chatbot del Dashboard):

```bash
# 1. Modelo recomendado para el Chatbot del Dashboard (optimizado Apple Silicon)
ollama pull gemma4:e2b-mlx

# 2. Modelos principales del estudio experimental (ejecución local soberana)
ollama pull gemma4:12b-mlx
ollama pull gemma4:31b-mlx
ollama pull llama3.1:8b
ollama pull qwen3:8b
ollama pull nemotron-mini:4b
ollama pull deepseek-r1:1.5b
ollama pull mistral-nemo:latest
```

---

## 📦 Paso 3: Operaciones Comunes con Datasets

Los datasets balanceados ya vienen preprocesados en `repos/ner-llm-entity-benchmark/data/`. Sin embargo, si deseas re-descargar fuentes externas o generar datos aumentados, ejecuta dentro de `repos/ner-llm-entity-benchmark/` con el venv activo:

```bash
# Descargar corpus CoNLL-2002 en español
python download_conll2002.py

# Descargar lista de sanciones de la OFAC (SDN List)
python download_ofac.py

# Recrear el dataset balanceado de 120 artículos (Kleptotrace + CoNLL-2002)
python create_balanced_120.py

# Generar diccionarios de metadatos multilingües para RAG
python generate_metadata_dicts.py

# Generar variantes aumentadas con inyección sintética de ruido/entidades
python generate_augmented_datasets.py
```

---

## 🔬 Paso 4: Ejecución de Benchmarks

Todos los comandos de ejecución se lanzan desde `repos/ner-llm-entity-benchmark/` con el entorno virtual activo (`source venv/bin/activate`).

### 4.1 Prueba Rápida de Humo (Smoke Test con muestra pequeña)
Genera una muestra de 20 registros y evalúa un modelo rápido (ej. `llama3.1:8b`):
```bash
# Generar dataset de muestra
python src/main.py --generate-sample-data

# Correr evaluación sobre la muestra
python src/main.py --models llama3.1:8b --data-file data/sample_20.json --batch-size 5
```

### 4.2 Corrida Estándar con RAG Integrado (KB Combined)
Para replicar la configuración ganadora de la tesina (Directiva `kb_combined` con directrices de desambiguación + ejemplar contextual):
```bash
python src/main.py \
  --models gemma4:12b-mlx gemma4:31b-mlx \
  --data-file data/benchmark_balanced_120.json \
  --batch-size 5 \
  --rag-study \
  --rag-mode kb_combined \
  --seed 42
```

### 4.3 Estudio de Variantes de Prompt (Ablación Lingüística)
Evalúa las diferencias entre Zero-Shot Inglés (`zs-en`), Zero-Shot Español (`zs-es`) y Few-Shot Español (`fs-es`):
```bash
python src/main.py \
  --models llama3.1:8b gemma4:12b-mlx \
  --data-file data/benchmark_balanced_120.json \
  --ablation
```

### 4.4 Reanudación Automática de Corridas Interrumpidas
Si una corrida se cancela o la máquina se reinicia, el sistema guarda puntos de control periódicos (`.checkpoint.json`). Para continuar donde quedó:
```bash
python src/main.py \
  --models gemma4:31b-mlx \
  --resume \
  --results-dir results/NOMBRE_DE_TU_CORRIDA/
```

---

## 📊 Paso 5: Lanzar y Navegar el Dashboard Interactivo

El Dashboard web en Streamlit permite explorar de forma visual e intuitiva todos los resultados históricos y canónicos.

### 5.1 Iniciar el Dashboard
Desde `repos/ner-llm-entity-benchmark/`:
```bash
source venv/bin/activate
streamlit run src/dashboard.py
```

Abre tu navegador en: **`http://localhost:8501`**

### 5.2 Selección de Corridas en la Barra Lateral
En el menú desplegable superior izquierdo ("Seleccionar Corrida para Análisis"):
- **`📊 R2 Consolidado 5 Semillas (Anexo K) — R2_CONSOLIDADO_5SEMILLAS_20260916` (Por defecto):** Carga los 12.430 registros de las 5 semillas con intervalos de confianza al 95 % (F1 medio: **82.97%**).
- **`🏆 Entrega Final Canónica N=120 (Tabla 7) — ANALISIS_CONJUNTO_20260909_FIX`:** Carga el conjunto canónico del informe principal sobre N=113 artículos limpios (F1 líder: **82.94%**).

### 5.3 Contenido de las Pestañas
1. **📊 Comparación de Modelos:** Gráficos de barra con métricas F1, Precisión y Exhaustividad.
2. **🧬 Análisis de Alucinaciones:** Tasa de alucinación por modelo (umbral seguro ≤ 5%).
3. **🏷️ Errores por Entidad:** Desglose cualitativo por tipo de entidad (`PER`, `ORG`, `LOC`).
4. **📈 Significancia Estadística:** Resultados en vivo de ANOVA unidireccional y matriz de Tukey HSD.
5. **⏱️ Eficiencia de Hardware:** Métricas de memoria VRAM/RAM y tokens/segundo.
6. **🎯 Criterios de Aceptación:** Banners automáticos de confirmación de la hipótesis de tesina (umbral ≥ 70%, meta aspiracional 85%).
7. **🏭 Simulación Productiva:** Evaluación de latencias bajo controlador AIMD.
8. **📝 Feedback Stakeholders:** Formulario para registrar retroalimentación cualitativa.
9. **💬 Chat con tus Resultados:** Asistente conversacional con LLM local.

---

## 💬 Paso 6: Consultar los Resultados en el Chatbot Local (Pestaña 9)

La pestaña **"💬 Chat con tus Resultados (Gemini / Ollama Local)"** te permite interactuar en lenguaje natural con los datos cargados en el Dashboard mediante un modelo soberano ejecutado 100% en tu máquina.

### 6.1 Cómo funciona el Chatbot
- El asistente utiliza por defecto el modelo local **`gemma4:e2b-mlx`** vía la API de Ollama (`/api/chat`).
- Si dicho modelo no estuviera instalado, implementa un fallback automático hacia `gemma4:31b-mlx`, `gemma4:12b-mlx` o el primer modelo disponible reportado por `/api/tags`.
- El Dashboard inyecta dinámicamente en el contexto del modelo las métricas de la corrida actualmente seleccionada (F1 de cada modelo, tasas de alucinación, latencias, ANOVA y p-values).

### 6.2 Ejemplos de Preguntas que puedes hacerle

Copia y pega cualquiera de estas consultas en la caja de texto del chat:

> **Pregunta 1 (Hipótesis principal):**  
> *"¿Cuál fue el mejor modelo de la corrida seleccionada, qué F1-Score alcanzó y qué significa respecto a la hipótesis del 70% de la tesina?"*

> **Pregunta 2 (Efecto del RAG):**  
> *"¿Qué impacto tuvo la integración de RAG contextual en comparación con la línea base (Baseline) y en qué modelos se observó mayor beneficio?"*

> **Pregunta 3 (Estadística inferencial):**  
> *"Explícame en términos sencillos si las diferencias entre los modelos son estadísticamente significativas según el análisis ANOVA y Tukey."*

> **Pregunta 4 (Alucinaciones y seguridad):**  
> *"¿Cuáles modelos mantuvieron una tasa de alucinación por debajo del 1% y cuál presentó el peor comportamiento?"*

> **Pregunta 5 (Eficiencia de hardware):**  
> *"Si tuviera que desplegar este sistema en un entorno con recursos limitados de memoria, ¿cuál modelo ofrece la mejor relación entre F1 y tokens por segundo?"*

---

## 🔍 Paso 7: Auditorías y Verificación de Consistencia de la Tesina

Desde la **raíz del proyecto** (`mti-pge-tesina-ner-llm-local/`), puedes ejecutar las herramientas pre-commit para asegurar que cualquier modificación mantenga la sincronía absoluta con los entregables académicos:

```bash
# 1. Auditoría integral de las 53 comprobaciones de la tesina (citas, tablas, numeración)
python3 tools/verificar_informe.py

# 2. Auditar que ninguna afirmación en bitácoras contradiga los datos reales
python3 tools/auditar_afirmaciones.py

# 3. Detectar desfases numéricos entre el documento DOCX y el Markdown canónico
python3 tools/desfase_cifras_docx.py
```

Todas las herramientas deben reportar `0 fallos nuevos` y código de salida `0`.

---

## 📚 Enlaces Rápidos y Navegación

- 📖 **Índice Maestro Completo:** [`MASTER-INDEX.md`](./MASTER-INDEX.md) (referencia cruzada de los 10 módulos del proyecto).
- 📝 **Fuente Canónica del Informe Final (Markdown):** [`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`](./doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md).
- 📄 **Entregable Oficial en Word (DOCX):** [`Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`](./Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx).
- 🤖 **Protocolo de Agentes y Coordinación:** [`CURRENT-TASKS.md`](./CURRENT-TASKS.md) y [`CLAUDE.md`](./CLAUDE.md).
- 💡 **Registro de Hallazgos Empíricos:** [`FINDINGS.md`](./FINDINGS.md) (187 evidencias certificadas).
- 🎓 **Preparación para la Defensa:** [`DEFENSA-PREGUNTAS-Y-RESPUESTAS.md`](./DEFENSA-PREGUNTAS-Y-RESPUESTAS.md).
