## Slide 1

Clasificación y Extracción de Entidades Nombradas (NER)

en   contenido  de  cumplimiento   normativo  mediante RAG y LLM

Eduardo Mauricio Ahumada Gallardo

Profesor Guía: José Luis Martí Lara

Organización Vinculada:  AustraNet

Seminario Integrado de Investigación y Graduación 2025 \| Abril 2026

## Slide 2

Magíster en Tecnologías de la Información

Diapositiva 2

Introducción, Problema y Propuesta de Solución

Ámbito del Problema

• Instituciones financieras chilenas necesitan automatizar cumplimiento normativo (Compliance)

• Gran volumen de noticias públicas requiere revisión manual

• Problema: extraer entidades (personas, organizaciones) con contexto semántico complejo

Solución Propuesta

• Sistema RAG (Retrieval-Augmented Generation)

• LLMs de código abierto (Gemma, DeepSeek, Llama)

• Ollama para ejecución local (sin fuga de datos)

• Enfoque innovador: \'contexto único\' por noticia

Importancia de Tecnologías de la Información

PLN (Procesamiento de Lenguaje Natural) • Sistemas Distribuidos • Inteligencia Artificial • Arquitectura RAG • Ingeniería de Prompts

Principales Contribuciones

✓ Pipeline RAG para NER en compliance (español/LatAm)  ✓ Validación vs línea base humana  ✓ Comparación de 3 LLMs abiertos  ✓ Prototipo funcional para producción

## Slide 3

Magíster en Tecnologías de la Información

Diapositiva 3

Marco Teórico y Estado del Arte

Conceptos Técnicos Fundamentales

NER (Named Entity Recognition):

Extracción de personas, organizaciones, ubicaciones

Transformers & LLMs:

Arquitectura de atención, modelos generativos

RAG (Retrieval-Augmented Generation):

Lewis et al. (2020) - Mitigación de alucinaciones

Estado del Arte vs Propuesta

Métodos previos:

✗ CRF (frágiles a variabilidad)

✗ BERT (requieren datos etiquetados)

✗ APIs propietarias (privacidad, costos)

Propuesta innovadora:

✓ LLMs locales + RAG

✓ Validación contra humanos

✓ Código abierto (Gemma, DeepSeek, Llama)

Referencias Clave (Últimos 3-4 años)

  Lewis et al. (2020)   RAG for Knowledge-Intensive NLP Tasks   NeurIPS
  --------------------- --------------------------------------- ---------
  Wu et al. (2023)      BloombergGPT - LLM para Finanzas        arXiv
  Chang et al. (2024)   RAG para análisis financiero            Journal

## Slide 4

Magíster en Tecnologías de la Información

Diapositiva 4

Hipótesis de Trabajo y Metodología de Validación

Hipótesis Principal

Un sistema RAG + LLM logrará F1-Score SUPERIOR a la extracción manual humana en reconocimiento de entidades de compliance, haciendo viable la automatización de alto riesgo regulatorio

Variables Independientes

• Método de extracción:

  - Extracción manual

  - Gemma + RAG

  - DeepSeek + RAG

  - Llama + RAG

Variables Dependientes

• Precisión (% de aciertos)

• Recall (cobertura de entidades)

• F1-Score (métrica balanceada)

• Tasa de alucinación

• Tiempo de procesamiento

Metodología de Validación

1. Ground Truth: 100-150 noticias etiquetadas por 2 expertos (Cohen\'s Kappa \>0.75)  \|  2. Línea Base Manual: Análisis por especialista compliance  \|  3. Evaluación Comparativa: 3 LLMs vs Ground Truth  \|  4. Análisis Estadístico: ANOVA + Tukey post-hoc (p\<0.05)  \|  5. Validación en Producción: Feedback de stakeholders

## Slide 5

Magíster en Tecnologías de la Información

Diapositiva 5

Plan de Trabajo 2026

Ene-Mar 2026

Preparación de Datos & Ground Truth

Abr-May 2026

Implementación RAG & Optimización LLM

Jun-Jul 2026

Evaluación Comparativa & Validación

Ago-Sep 2026

Integración Prototipo & Documentación Final

Estimación de Esfuerzo Total: \~350 horas

  Fase    Preparación   Implementación   Evaluación   Integración
  ------- ------------- ---------------- ------------ -------------
  Horas   120h          100h             80h          50h

Trabajo Adelantado a la Fecha

✓ Viabilidad técnica confirmada: Ejecución nativa de LLMs en Apple M4  ✓ Código piloto funcional: NER en noticias públicas  ✓ Integración inicial: Streamlit para visualización  ✓ Diseño RAG: Mitigación de alucinaciones mediante context injection

## Slide 6

Magíster en Tecnologías de la Información

Diapositiva 6

Conclusión e Impacto Esperado

Impacto Nacional

Sector FinTech & RegTech chileno:

• Reducción 60-80% en costos de compliance manual

• Escalabilidad a nuevos mercados

• Mejora en detección de riesgos

• Viabilidad de IA abierta en contextos regulados

Impacto Internacional

Contribución a IA abierta y equitativa:

• Alternativa a soluciones propietarias costosas

• LLMs abiertos para NLP regulado

• Transferible a América Latina

• Blueprint para IA responsable

Recursos Comprometidos y Disponibles

✓ Hardware: Apple M4 disponible  ✓ Software: Todo código abierto (\$0)  ✓ Datos: Acceso a base de  noticias   OpenSanctions  y  AustraNet  ✓ Expertos: 2 especialistas compliance  ✓ Profesor guía: José Luis Martí Lara (bi-semanales)  ✓ NDA: Compromiso de confidencialidad con  AustraNet

Proyecto de alto impacto que combina rigor científico con pragmatismo industrial, contribuyendo tanto al estado del arte en IA/NLP como a resolución de problema crítico para sector financiero nacional
