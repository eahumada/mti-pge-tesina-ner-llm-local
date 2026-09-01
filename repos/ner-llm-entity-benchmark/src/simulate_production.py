from __future__ import annotations
import os
import sys
import json
from datetime import datetime, timezone

# Ensure imports are resolved
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_all_records
from src.evaluator import evaluate_single_record
from src.llm_runner import extract_entities_with_ollama

def simulate_daily_batch(
    data_file: str = "data/benchmark_balanced_120.json",
    model: str = "gemma4:latest",
    base_url: str = "http://localhost:11434",
    system_prompt_file: str = "SYSTEM_PROMPT.md",
    max_articles: int = 5
):
    """
    Simulates a daily batch processing flow of news articles for compliance stakeholders.
    Uses REAL LLM inference via the local Ollama server (no mocking).
    """
    print("==================================================")
    print("🚦 STARTING DAILY BATCH PRODUCTION SIMULATION (Real LLM)")
    print("==================================================")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Model: {model}")
    print(f"Ollama Endpoint: {base_url}")
    print(f"Loading incoming news feed from {data_file}...")

    records = load_all_records(data_file)
    if not records:
        print("Error: No articles found to process.")
        return

    # Load system prompt
    system_prompt = ""
    if os.path.exists(system_prompt_file):
        with open(system_prompt_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "[SYSTEM]" in content:
            parts = content.split("[SYSTEM]")
            system_prompt = parts[1].split("[USER]")[0].strip() if "[USER]" in parts[1] else parts[1].strip()
        else:
            system_prompt = content.strip()
    else:
        system_prompt = (
            "You are an expert compliance and anti-money laundering (AML) analyst. "
            "Perform Named Entity Recognition (NER) on news. Extract entities into: "
            "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
            "\"Persons\", \"Organizations\", \"Locations\"."
        )

    articles_to_process = records[:max_articles]
    print(f"Successfully loaded {len(records)} incoming articles. Processing first {len(articles_to_process)}.")
    print("Simulating ingestion queue publishing...\n")

    results = []

    for idx, record in enumerate(articles_to_process):
        art_id = record.get("id", f"article-{idx+1}")
        caption = record.get("caption", record.get("text", ""))
        print(f"[{idx+1}/{len(articles_to_process)}] Ingesting article ID: {art_id}")
        print(f"Snippet: {caption[:120]}...")
        print(f"Routing to local LLM worker node ({model})...")

        # === REAL LLM CALL via Ollama ===
        llm_result = extract_entities_with_ollama(
            text=caption,
            model_name=model,
            system_prompt=system_prompt,
            ollama_base_url=base_url,
            max_retries=2,
            temperature=0.1,
            max_tokens=2048
        )

        extracted = llm_result.get("entities", {"Persons": [], "Organizations": [], "Locations": []})
        latency = llm_result.get("latency", 0.0)
        tokens_per_sec = llm_result.get("tokens_per_sec", 0.0)
        retries = llm_result.get("retries", 0)

        # Evaluate against ground truth if available
        gt = record.get("ground_truth", {"Persons": [], "Organizations": [], "Locations": []})
        eval_out = evaluate_single_record(
            extracted=extracted,
            ground_truth=gt,
            source_text=caption,
            threshold=85
        )

        result = {
            "batch_idx": 0,
            "record_id": art_id,
            "model": model,
            "latency_sec": latency,
            "tokens_per_sec": tokens_per_sec,
            "retries": retries,
            "parse_method": llm_result.get("parse_method", "unknown"),
            "precision": eval_out["metrics"]["overall"]["precision"],
            "recall": eval_out["metrics"]["overall"]["recall"],
            "f1": eval_out["metrics"]["overall"]["f1"],
            "hallucination_rate": eval_out["hallucination"]["hallucination_rate"],
            "hallucinated_count": eval_out["hallucination"]["hallucinated_count"],
            "extracted_entities": extracted,
            "metrics": eval_out["metrics"]
        }
        results.append(result)
        print(f"Extraction completed. F1-Score: {result['f1']:.2%} | Latency: {latency:.2f}s | Tokens/sec: {tokens_per_sec:.1f}\n")

    print("==================================================")
    print("🔬 COMPILING BATCH STATS & AUDIT LOGS")
    print("==================================================")

    avg_f1 = sum(r["f1"] for r in results) / len(results) if results else 0.0
    avg_halluc = sum(r["hallucination_rate"] for r in results) / len(results) if results else 0.0
    avg_latency = sum(r["latency_sec"] for r in results) / len(results) if results else 0.0

    print(f"Total processed: {len(results)} articles")
    print(f"Average F1-Score: {avg_f1:.2%}")
    print(f"Average Hallucination Rate: {avg_halluc:.2%}")
    print(f"Average Latency: {avg_latency:.2f}s per article")

    sim_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "articles_processed": len(results),
        "average_f1": avg_f1,
        "average_hallucination_rate": avg_halluc,
        "average_latency_sec": avg_latency,
        "is_real_llm": True,
        "results": results
    }

    os.makedirs("results", exist_ok=True)
    with open("results/simulation_summary.json", "w", encoding="utf-8") as f:
        json.dump(sim_data, f, indent=2)

    print("\n✅ Simulation completed (REAL LLM). Run summary saved to results/simulation_summary.json.")
    print("Stakeholders can now view metrics and provide feedback via the Streamlit dashboard.")
    print("==================================================")


if __name__ == "__main__":
    simulate_daily_batch()
