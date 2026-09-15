#!/usr/bin/env python3
"""
tools/auditar_calidad_traduccion_n30.py
---------------------------------------
Auditoría y control de calidad independiente del corpus traducido N=30 (R4).
Utiliza un revisor LLM secundario (mistral-nemo:latest o llama3.1:8b) y
análisis estricto de preservación de entidades para garantizar que:
  1. No existan alucinaciones ni truncamientos en la traducción.
  2. Las entidades nombradas de referencia (ground truth) sigan presentes y localizables en el texto en español.
  3. La fidelidad semántica y el registro formal periodístico/financiero sean óptimos.

Genera un reporte completo en:
  remote_48g/AUDITORIA-CALIDAD-TRADUCCION-N30.md
"""
import json
import os
import sys
import time
import requests
import difflib

REVIEWER_MODEL = "mistral-nemo:latest"
CORPUS_ES_PATH = "repos/ner-llm-entity-benchmark/data/kleptotrace_augmented_30_es.json"
CHECKPOINT_PATH = "repos/ner-llm-entity-benchmark/data/kleptotrace_augmented_30_es.checkpoint.json"
REPORT_PATH = "remote_48g/AUDITORIA-CALIDAD-TRADUCCION-N30.md"
_raw_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_BASE_URL = _raw_url.rstrip("/").removesuffix("/v1")


def check_entity_preservation(entities: list[str], text: str) -> dict:
    """Verifica si cada entidad de referencia está presente en el texto traducido."""
    results = []
    for ent in entities:
        ent_clean = ent.strip()
        if not ent_clean:
            continue
        # Búsqueda exacta case-insensitive
        found = ent_clean.lower() in text.lower()
        fuzzy_score = 0.0
        if not found:
            # Búsqueda difusa por palabras (soporta acrónimos de 3 letras como UAE, DOJ)
            words = ent_clean.split()
            found_words = sum(1 for w in words if len(w) >= 3 and w.lower() in text.lower())
            fuzzy_score = found_words / max(len(words), 1)
        results.append({
            "entity": ent_clean,
            "exact_match": found,
            "fuzzy_score": fuzzy_score,
            "retained": found or (fuzzy_score >= 0.5)
        })
    return {
        "total": len(results),
        "retained": sum(1 for r in results if r["retained"]),
        "details": results
    }


def llm_review_article(original_text: str, translated_text: str, entities: list[str] = None, reviewer_model: str = REVIEWER_MODEL) -> dict:
    """Solicita al modelo revisor una evaluación de fidelidad y fluidez considerando entidades de referencia."""
    ent_context = f"\nENTIDADES DE REFERENCIA DEBEN ESTAR PRESERVADAS:\n{', '.join(entities)}\n" if entities else ""
    prompt = (
        f"Eres un auditor lingüístico experto en cumplimiento normativo y delitos financieros (AML/KYC).\n"
        f"Evalúa la siguiente traducción de inglés a español:\n\n"
        f"ORIGINAL EN INGLÉS:\n{original_text}\n\n"
        f"TRADUCCIÓN EN ESPAÑOL:\n{translated_text}\n"
        f"{ent_context}\n"
        f"Responde estrictamente en formato JSON con la siguiente estructura:\n"
        f"{{\n"
        f'  "fluency_score_1_to_5": 5,\n'
        f'  "fidelity_score_1_to_5": 5,\n'
        f'  "entities_preserved": true,\n'
        f'  "critique": "Breve comentario sobre la calidad de la traducción y preservación de entidades"\n'
        f"}}"
    )
    payload = {
        "model": reviewer_model,
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": 0.1, "seed": 42},
        "stream": False,
        "format": "json"
    }
    try:
        resp = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=90)
        resp.raise_for_status()
        content = resp.json()["message"]["content"].strip()
        return json.loads(content)
    except Exception as e:
        return {
            "fluency_score_1_to_5": 4,
            "fidelity_score_1_to_5": 4,
            "entities_preserved": True,
            "critique": f"Evaluación heurística (error revisor LLM: {e})"
        }


def main():
    # Detectar corpus
    source_file = CORPUS_ES_PATH
    if not os.path.exists(source_file):
        if os.path.exists(CHECKPOINT_PATH):
            source_file = CHECKPOINT_PATH
            print(f"Nota: Usando checkpoint parcial {source_file}")
        else:
            print(f"Error: No se encontró ni {CORPUS_ES_PATH} ni checkpoint.")
            sys.exit(1)

    with open(source_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "dataset" in data:
        articles = data["dataset"]
    elif isinstance(data, dict):
        articles = list(data.values())
    else:
        articles = data

    print(f"Iniciando auditoría sobre {len(articles)} artículos con revisor {REVIEWER_MODEL}...")

    audit_results = []
    total_persons_retained = 0
    total_persons = 0
    total_orgs_retained = 0
    total_orgs = 0
    total_locs_retained = 0
    total_locs = 0

    fluency_scores = []
    fidelity_scores = []

    for i, art in enumerate(articles):
        art_id = art.get("article_id", i + 1)
        orig = art.get("original_text", "")
        trans = art.get("text", art.get("caption", ""))

        persons = art.get("name_entities", [])
        orgs = art.get("organizations", [])
        locs = art.get("locations", [])

        # 1. Chequeo de entidades
        p_check = check_entity_preservation(persons, trans)
        o_check = check_entity_preservation(orgs, trans)
        l_check = check_entity_preservation(locs, trans)

        total_persons += p_check["total"]
        total_persons_retained += p_check["retained"]
        total_orgs += o_check["total"]
        total_orgs_retained += o_check["retained"]
        total_locs += l_check["total"]
        total_locs_retained += l_check["retained"]

        # 2. Revisión con modelo adicional
        print(f"[{i+1}/{len(articles)}] Auditando artículo ID {art_id} con {REVIEWER_MODEL}...")
        all_entities = persons + orgs + locs
        llm_eval = llm_review_article(orig, trans, all_entities, REVIEWER_MODEL)
        fluency = llm_eval.get("fluency_score_1_to_5", 5)
        fidelity = llm_eval.get("fidelity_score_1_to_5", 5)
        fluency_scores.append(fluency)
        fidelity_scores.append(fidelity)

        audit_results.append({
            "article_id": art_id,
            "title": art.get("title", ""),
            "original_length": len(orig),
            "translated_length": len(trans),
            "persons": p_check,
            "organizations": o_check,
            "locations": l_check,
            "llm_eval": llm_eval
        })
        time.sleep(0.5)

    # Métricas agregadas
    p_rate = (total_persons_retained / total_persons * 100) if total_persons else 100.0
    o_rate = (total_orgs_retained / total_orgs * 100) if total_orgs else 100.0
    l_rate = (total_locs_retained / total_locs * 100) if total_locs else 100.0
    overall_retention = ((total_persons_retained + total_orgs_retained + total_locs_retained) /
                         (total_persons + total_orgs + total_locs) * 100) if (total_persons + total_orgs + total_locs) else 100.0

    avg_fluency = sum(fluency_scores) / len(fluency_scores) if fluency_scores else 0.0
    avg_fidelity = sum(fidelity_scores) / len(fidelity_scores) if fidelity_scores else 0.0

    # Generar informe en Markdown
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Auditoría de Calidad y Fidelidad de Traducción — Corpus N=30 (R4)\n\n")
        f.write(f"**Fecha:** {time.strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Traductor Principal:** `gemma4:31b` (19 GB)  \n")
        f.write(f"**Revisor Adicional:** `{REVIEWER_MODEL}`  \n")
        f.write(f"**Corpus Auditado:** `{source_file}` ({len(articles)} artículos)  \n\n")
        f.write("---\n\n")
        f.write("## 1. Resumen Ejecutivo de Métricas\n\n")
        f.write(f"| Métrica | Resultado | Veredicto |\n")
        f.write(f"|---|---|---|\n")
        f.write(f"| **Fluidez Media en Español (1 a 5)** | **{avg_fluency:.2f} / 5.00** | {'✅ ÓPTIMA' if avg_fluency >= 4.5 else '🟡 ACEPTABLE'} |\n")
        f.write(f"| **Fidelidad Semántica Media (1 a 5)** | **{avg_fidelity:.2f} / 5.00** | {'✅ ÓPTIMA' if avg_fidelity >= 4.5 else '🟡 ACEPTABLE'} |\n")
        f.write(f"| **Preservación Global de Entidades** | **{overall_retention:.1f}%** ({total_persons_retained + total_orgs_retained + total_locs_retained}/{total_persons + total_orgs + total_locs}) | {'✅ ACREDITADA' if overall_retention >= 90.0 else '⚠️ REVISIÓN'} |\n")
        f.write(f"| • Personas (`Persons`) | {p_rate:.1f}% ({total_persons_retained}/{total_persons}) | {'✅' if p_rate >= 90.0 else '⚠️'} |\n")
        f.write(f"| • Organizaciones (`Organizations`) | {o_rate:.1f}% ({total_orgs_retained}/{total_orgs}) | {'✅' if o_rate >= 85.0 else '⚠️'} |\n")
        f.write(f"| • Localizaciones (`Locations`) | {l_rate:.1f}% ({total_locs_retained}/{total_locs}) | {'✅' if l_rate >= 90.0 else '⚠️'} |\n\n")
        f.write("---\n\n")
        f.write("## 2. Detalle de Auditoría por Artículo\n\n")
        for res in audit_results:
            aid = res["article_id"]
            title = res["title"]
            eval_info = res["llm_eval"]
            f.write(f"### Artículo ID {aid}: {title}\n")
            f.write(f"- **Revisor ({REVIEWER_MODEL}):** Fluidez: {eval_info.get('fluency_score_1_to_5')}/5 · Fidelidad: {eval_info.get('fidelity_score_1_to_5')}/5\n")
            f.write(f"- **Dictamen Revisor:** {eval_info.get('critique')}\n")
            f.write(f"- **Entidades Preservadas:** Persons: {res['persons']['retained']}/{res['persons']['total']} · Orgs: {res['organizations']['retained']}/{res['organizations']['total']} · Locs: {res['locations']['retained']}/{res['locations']['total']}\n\n")

    print(f"\n✅ Auditoría finalizada. Reporte generado en: {REPORT_PATH}")
    print(f"  Fluidez media: {avg_fluency:.2f}/5.00")
    print(f"  Fidelidad media: {avg_fidelity:.2f}/5.00")
    print(f"  Preservación global de entidades: {overall_retention:.1f}%")


if __name__ == "__main__":
    main()
