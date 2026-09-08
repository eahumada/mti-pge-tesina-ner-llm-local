from __future__ import annotations
import argparse
import json
import logging
import os
import sys
import time
import hashlib
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests

# Ensure sibling imports are valid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import BenchmarkConfig, ensure_directories, load_system_prompt
from src.data_loader import load_data_batch, create_sample_dataset, extract_ground_truth, validate_record_schema, DatasetIterator
from src.llm_runner import extract_entities_with_ollama, manage_model_lifecycle, check_model_available, is_cloud_model
from src.evaluator import evaluate_single_record, aggregate_model_results, build_confusion_matrix
from src.statistics import run_anova_test, run_tukey_posthoc, calculate_confidence_intervals, generate_statistical_report
from src.checkpoint import CheckpointState, save_checkpoint, load_checkpoint, is_batch_completed, mark_batch_completed
from src.pub_sub import create_task_queue, TaskMessage
from src.system_monitor import ThroughputTracker
from src.adaptive_workers import AdaptiveWorkerController, is_rate_limit_exception
from src.rag_manager import RAGManager
from src.kb_rag_manager import KBRAGManager, RAG_MODE_ENTITIES

logger = logging.getLogger("ner_benchmark")

# §2.bis.1 / FINDINGS §F53: manifiesto de artículos contaminados (ejemplares few-shot que son del propio
# corpus de evaluación). Se excluyen SOLO de la métrica publicada en los modos kb afectados; el crudo
# detailed_results.json conserva todos los registros. La exclusión es programática y declarada, no a mano.
_MANIFIESTO_CONTAMINADOS = os.path.join("data", "knowledge_base", "contaminated_exemplar_articles.json")


def _excluir_contaminados(results: list[dict], rag_mode) -> list[dict]:
    """Devuelve los resultados sin los artículos contaminados si el modo actual está afectado.
    Si el modo no está en la lista del manifiesto, o el manifiesto no existe, devuelve todo sin tocar."""
    try:
        with open(_MANIFIESTO_CONTAMINADOS, "r", encoding="utf-8") as f:
            man = json.load(f)
    except (FileNotFoundError, ValueError):
        return results
    modos = set(man.get("excluded_from_metric_modes", []))
    if rag_mode not in modos:
        return results
    excluidos = set(man.get("article_ids", []))
    filtrados = [r for r in results if str(r.get("record_id")) not in excluidos]
    n = len(results) - len(filtrados)
    if n:
        logger.info("§2.bis.1: excluidos %d registros contaminados de la métrica (modo '%s'); "
                    "el crudo los conserva.", n, rag_mode)
    return filtrados


def setup_logging(results_dir: str) -> None:
    """Configures system logging outputs."""
    os.makedirs(results_dir, exist_ok=True)
    log_file = os.path.join(results_dir, "benchmark.log")
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
    logger.setLevel(logging.DEBUG)

def validate_environment(config: BenchmarkConfig) -> bool:
    """Checks that Ollama endpoint is responsive and local models are ready."""
    try:
        response = requests.get(config.ollama_base_url, timeout=5)
        if response.status_code != 200:
            logger.error("Ollama service returned unexpected status code.")
            return False
    except Exception as e:
        logger.error(f"Cannot connect to Ollama service at {config.ollama_base_url}: {e}")
        return False
        
    for model in config.models:
        if is_cloud_model(model):
            logger.info(f"Model '{model}' is a cloud-hosted Ollama model. Bypassing local availability check.")
            continue
        if not check_model_available(model, config.ollama_base_url):
            logger.warning(f"Model '{model}' is not pulled in local Ollama repository. "
                           "The benchmark will skip or warn when invoking this model.")
    return True

def process_batch(batch: list[dict], model: str, system_prompt: str, config: BenchmarkConfig, batch_idx: int, condition_name: str | None = None, rag_manager = None) -> list[dict]:
    """Processes a batch of articles against a model in parallel and returns structured evaluations (REQ-PAR-03)."""
    results = []
    prompt_hash = hashlib.sha256(system_prompt.encode('utf-8')).hexdigest()[:8]
    display_model_name = condition_name if condition_name else model
    
    def process_single_record(record: dict, worker_id: int):
        if not validate_record_schema(record):
            logger.warning(f"[Worker {worker_id}] Record with ID '{record.get('id', 'unknown')}' has invalid schema. Skipping.")
            return None
            
        record_id = record["id"]
        source_text = record["caption"]
        ground_truth = record.get("ground_truth", extract_ground_truth(record))
        
        logger.info(f"[Worker {worker_id}] Model '{model}' (Mapped: '{display_model_name}') -> Extracting entities for record '{record_id}'...")
        
        rag_context = None
        if rag_manager:
            rag_context = rag_manager.query([source_text])

        # Run Ollama NER
        llm_output = extract_entities_with_ollama(
            text=source_text,
            model_name=model,
            system_prompt=system_prompt,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            seed=config.seed,
            max_retries=config.max_retries,
            ollama_base_url=config.ollama_base_url,
            rag_context=rag_context
        )
        
        # Evaluate metrics
        eval_output = evaluate_single_record(
            extracted=llm_output["entities"],
            ground_truth=ground_truth,
            source_text=source_text,
            threshold=config.fuzzy_threshold
        )
        
        # Aggregate trace result
        sm = llm_output.get("sys_metrics", {})
        result = {
            "batch_idx": batch_idx,
            "record_id": record_id,
            "model": display_model_name,
            "latency_sec": llm_output["latency"],
            "tokens_per_sec": llm_output["tokens_per_sec"], # efficiency metric (REQ42)
            "retries": llm_output["retries"],
            "parse_method": llm_output["parse_method"],
            "precision": eval_output["metrics"]["overall"]["precision"],
            "recall": eval_output["metrics"]["overall"]["recall"],
            "f1": eval_output["metrics"]["overall"]["f1"],
            "hallucination_rate": eval_output["hallucination"]["hallucination_rate"],
            "hallucinated_count": eval_output["hallucination"]["hallucinated_count"],
            # ── Hardware telemetry (system_monitor) ──────────────────────
            "cpu_avg_pct":        sm.get("avg_cpu_pct", 0.0),
            "cpu_peak_pct":       sm.get("peak_cpu_pct", 0.0),
            "proc_cpu_avg_pct":   sm.get("avg_proc_cpu_pct", 0.0),
            "mem_avg_mb":         sm.get("avg_mem_mb", 0.0),
            "mem_peak_mb":        sm.get("peak_mem_mb", 0.0),
            "sys_mem_avg_mb":     sm.get("avg_sys_mem_mb", 0.0),
            "sys_mem_avg_pct":    sm.get("avg_sys_mem_pct", 0.0),
            "vram_mb":            sm.get("vram_mb", 0.0),
            "model_disk_mb":      sm.get("model_disk_mb", 0.0),
            # ── Nested structures saved in detailed JSON ──────────────────
            "metrics": eval_output["metrics"],
            "error_taxonomy": eval_output["error_taxonomy"],
            "data_provenance": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model_version": model,
                "prompt_hash": prompt_hash
            }
        }
        return result

    # Concurrency control based on configuration
    num_workers = config.num_workers
    logger.info(f"Processing batch {batch_idx + 1} with {num_workers} parallel workers...")
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_single_record, record, idx + 1): record for idx, record in enumerate(batch)}
        for future in as_completed(futures):
            res = future.result()
            if res is not None:
                results.append(res)
                
    # Maintain original record ordering for consistent evaluation reporting (REQ-PAR-06)
    order_map = {record["id"]: idx for idx, record in enumerate(batch)}
    results.sort(key=lambda r: order_map.get(r["record_id"], 999))
    
    return results

def export_results(results: list[dict], summary: dict, stat_report: str, confusion: dict, config: BenchmarkConfig) -> None:
    """Exports structured result files."""
    ensure_directories(config)
    
    # 1. Main detailed traces as CSV
    df = pd.DataFrame(results)
    # Simplify nested columns for flat CSV export
    df_flat = df.drop(columns=["metrics", "error_taxonomy"], errors='ignore')
    df_flat.to_csv(os.path.join(config.results_dir, "benchmark_results.csv"), index=False)
    
    # Save detailed JSON file including nested metrics
    with open(os.path.join(config.results_dir, "detailed_results.json"), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    # 2. Aggregated metrics summary
    with open(os.path.join(config.results_dir, "benchmark_summary.json"), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
        
    # 3. Confusion Matrix
    with open(os.path.join(config.results_dir, "confusion_matrix.json"), 'w', encoding='utf-8') as f:
        json.dump(confusion, f, indent=2)
        
    # 4. Statistical analysis report
    with open(os.path.join(config.results_dir, "statistical_report.md"), 'w', encoding='utf-8') as f:
        f.write(stat_report)
        
    # 5. Reproducibility config
    with open(os.path.join(config.results_dir, "run_config.json"), 'w', encoding='utf-8') as f:
        json.dump(config.to_dict(), f, indent=2)

    # 6. Acceptance criteria validation (US16)
    best_model = None
    best_f1 = 0.0
    for model, metrics in summary.items():
        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            best_model = model
            
    best_hallucination = summary.get(best_model, {}).get("hallucination_rate", 0.0) if best_model else 0.0
    
    acceptance_status = {
        "target_f1_met": bool(best_f1 >= 0.85),
        "overall_f1": float(best_f1),
        "best_model": best_model,
        "hallucination_rate": float(best_hallucination),
        "hallucination_warning": bool(best_hallucination > 0.05)
    }
    with open(os.path.join(config.results_dir, "acceptance_status.json"), 'w', encoding='utf-8') as f:
        json.dump(acceptance_status, f, indent=2)
        
    logger.info("Successfully exported all results to results/ output directory.")

def run_benchmark(config: BenchmarkConfig, resume: bool = False, ablation: bool = False) -> None:
    """Main benchmark orchestration loop."""
    # Reconcile the ablation flag with the config so it is persisted in
    # run_config.json (previously it travelled only as a function argument and
    # ablation runs were indistinguishable from baseline runs in metadata).
    ablation = bool(ablation) or bool(getattr(config, "ablation", False))
    config.ablation = ablation

    setup_logging(config.results_dir)
    ensure_directories(config)
    
    logger.info("Initializing NER-LLM Sanctions Evaluator Pipeline...")
    
    if not validate_environment(config):
        logger.error("Environment validation failed. Exiting.")
        return
        
    system_prompt = load_system_prompt(config.system_prompt_file)
    logger.info(f"Loaded System Prompt (Length: {len(system_prompt)} chars)")
    
    # Load or create checkpoint state
    checkpoint_path = config.checkpoint_file
    state = None
    if resume:
        state = load_checkpoint(checkpoint_path)
        if state:
            logger.info(f"Resuming benchmark from checkpoint. Completed batches logged.")
            
    if not state:
        config_hash = hashlib.sha256(json.dumps(config.to_dict(), sort_keys=True).encode()).hexdigest()[:12]
        state = CheckpointState(config_hash=config_hash)
        logger.info("Starting a new benchmark session.")
        
    # Setup dataset iterator
    dataset = DatasetIterator(config.data_file, config.batch_size)
    total_batches = dataset.total_batches
    logger.info(f"Corpus loaded: {dataset.total_records} articles split into {total_batches} batches.")
    
    if total_batches == 0:
        logger.error("No data found to process. Please check data file path.")
        return
        
    # Setup Task Queue (decoupled pub/sub architecture) (FR1.5 / REQ-PAR-02)
    # Supporting Redis task queue configuration if active
    task_queue = create_task_queue(use_redis=False) # InMemory queue for concurrent execution
    
    # 1. Publish all pending tasks to the queue (Producer)
    logger.info("Main thread acting as Producer: Publishing pending tasks to queue...")
    published_count = 0
    
    if config.rag_study:
        # Select RAG manager based on configured mode:
        #   'entities'     → legacy RAGManager (dict-based, original behavior)
        #   'kb_*'         → KBRAGManager (knowledge-base, new approach)
        # Default is 'entities' for full backward compatibility.
        if config.rag_mode == RAG_MODE_ENTITIES:
            rag_mgr = RAGManager()
            rag_mgr.load_dictionaries()
            rag_conditions = ['baseline', 'rag_enhanced']
        else:
            rag_mgr = KBRAGManager(rag_mode=config.rag_mode)
            rag_mgr.load_knowledge_base()
            rag_conditions = ['baseline', 'kb_rag']
            logger.info(f"[RAG] Using Knowledge Base mode: '{config.rag_mode}'")
        for model in config.models:
            if not check_model_available(model, config.ollama_base_url):
                continue
            for condition_name in rag_conditions:
                condition_key = f"{model}_{condition_name}"
                for batch_idx in range(total_batches):
                    if is_batch_completed(state, condition_key, batch_idx):
                        continue
                    batch_records = dataset.get_batch(batch_idx)
                    if not batch_records:
                        continue
                    task_msg = TaskMessage(
                        task_id=f"{condition_key}-b{batch_idx}-{int(time.time())}",
                        batch_idx=batch_idx,
                        model_name=model,
                        records=batch_records,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        prompt_file=config.system_prompt_file,
                        condition_name=condition_key
                    )
                    task_queue.publish(task_msg)
                    published_count += 1
    elif ablation:
        # Prompt Ablation Study (REQ41): cycle through prompt configurations
        model = config.models[0]
        if not check_model_available(model, config.ollama_base_url):
            logger.error(f"Target model {model} not available for prompt ablation study.")
            return
            
        conditions = {
            "zs-en": "SYSTEM_PROMPT.md",
            "zs-es": "SYSTEM_PROMPT_ES.md",
            "fs-es": "SYSTEM_PROMPT_ES_FEWSHOT.md",
            "fs-en": "SYSTEM_PROMPT_EN_FEWSHOT.md"
        }
        for condition_name, prompt_file in conditions.items():
            for batch_idx in range(total_batches):
                if is_batch_completed(state, condition_name, batch_idx):
                    continue
                batch_records = dataset.get_batch(batch_idx)
                if not batch_records:
                    continue
                task_msg = TaskMessage(
                    task_id=f"{condition_name}-b{batch_idx}-{int(time.time())}",
                    batch_idx=batch_idx,
                    model_name=model, # Physical model name (e.g. gemma4:latest)
                    records=batch_records,
                    created_at=datetime.now(timezone.utc).isoformat(),
                    prompt_file=prompt_file,
                    condition_name=condition_name # Label for tracking
                )
                task_queue.publish(task_msg)
                published_count += 1
    else:
        # Standard model benchmarking sweep
        for model_idx, model in enumerate(config.models):
            if not check_model_available(model, config.ollama_base_url):
                if "mlx" in model.lower():
                    logger.warning(f"Model {model} not pulled in Ollama. Proceeding with soft fallback support.")
                else:
                    logger.warning(f"Skipping model {model} because it is not available in Ollama.")
                    continue
                
            for batch_idx in range(total_batches):
                if is_batch_completed(state, model, batch_idx):
                    continue
                    
                batch_records = dataset.get_batch(batch_idx)
                if not batch_records:
                    continue
                    
    # Enforce strictly sequential model evaluation: 1 model/condition at a time, but with parallel batch workers
    import threading
    state_lock = threading.Lock()

    # ── AIMD Adaptive Worker Controller ──────────────────────────────────────
    # Replaces hardcoded num_queue_workers=4 with a dynamically self-tuning
    # concurrency controller using Additive Increase / Multiplicative Decrease.
    # Initial value comes from config.num_workers (CLI --num-workers, default 2).
    adaptive_ctrl = AdaptiveWorkerController(
        min_workers=1,
        max_workers=getattr(config, "max_workers", None),  # None=auto (cpu-2); topado por --max-workers
        initial_workers=config.num_workers,
        stable_window_sec=600.0,       # 10 min without errors before AI phase
        increase_interval_sec=120.0,   # +1 worker every 2 min during AI phase
        ai_ceiling_fraction=0.75,      # cap AI at 75 % of max_workers
        circuit_failure_threshold=5,   # open circuit after 5 consecutive failures
        circuit_recovery_sec=300.0,    # probe recovery after 5 min cool-down
    )
    num_queue_workers = adaptive_ctrl.current_workers
    config.num_workers = adaptive_ctrl.current_workers
    
    if config.rag_study:
        # Select RAG manager based on configured mode (same logic as producer phase above)
        if config.rag_mode == RAG_MODE_ENTITIES:
            rag_mgr = RAGManager()
            rag_conditions = ['baseline', 'rag_enhanced']
        else:
            rag_mgr = KBRAGManager(rag_mode=config.rag_mode)
            rag_mgr.load_knowledge_base()
            rag_conditions = ['baseline', 'kb_rag']
            logger.info(f"[RAG] Worker phase — Knowledge Base mode: '{config.rag_mode}'")
        for model in config.models:
            if not check_model_available(model, config.ollama_base_url):
                continue
            for condition_name in rag_conditions:
                condition_key = f"{model}_{condition_name}"
                task_queue = create_task_queue(use_redis=False)
                published_count = 0
                for batch_idx in range(total_batches):
                    if is_batch_completed(state, condition_key, batch_idx):
                        continue
                    batch_records = dataset.get_batch(batch_idx)
                    if not batch_records:
                        continue
                    task_msg = TaskMessage(
                        task_id=f"{condition_key}-b{batch_idx}-{int(time.time())}",
                        batch_idx=batch_idx,
                        model_name=model,
                        records=batch_records,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        prompt_file=config.system_prompt_file,
                        condition_name=condition_key
                    )
                    task_queue.publish(task_msg)
                    published_count += 1
                if published_count > 0:
                    num_queue_workers = adaptive_ctrl.current_workers
                    logger.info(f"Running RAG study '{condition_key}' with {num_queue_workers} workers...")
                    def worker_consumer(worker_id: int):
                        while True:
                            claimed_task = task_queue.subscribe()
                            if not claimed_task: break
                            task_prompt = load_system_prompt(claimed_task.prompt_file)
                            # Activate RAG for any non-baseline condition ('rag_enhanced' or 'kb_rag')
                            is_rag_condition = (
                                'rag_enhanced' in claimed_task.condition_name
                                or 'kb_rag' in claimed_task.condition_name
                            )
                            active_rag = rag_mgr if is_rag_condition else None
                            try:
                                batch_results = process_batch(
                                    batch=claimed_task.records,
                                    model=claimed_task.model_name,
                                    system_prompt=task_prompt,
                                    config=config,
                                    batch_idx=claimed_task.batch_idx,
                                    condition_name=claimed_task.condition_name,
                                    rag_manager=active_rag
                                )
                                task_queue.acknowledge(claimed_task.task_id)
                                with state_lock:
                                    mark_batch_completed(state, claimed_task.condition_name, claimed_task.batch_idx, batch_results)
                                    save_checkpoint(state, checkpoint_path)
                                new_w = adaptive_ctrl.report_success()
                                config.num_workers = new_w
                            except Exception as exc:
                                is_rl = is_rate_limit_exception(exc)
                                new_w = adaptive_ctrl.report_error(is_rate_limit=is_rl)
                                config.num_workers = new_w
                                logger.error(f"[Worker {worker_id}] Error: {exc}")
                    with ThreadPoolExecutor(max_workers=num_queue_workers) as executor:
                        futures = [executor.submit(worker_consumer, idx + 1) for idx in range(num_queue_workers)]
                        for future in futures: future.result()
            logger.info(f"Unloading model weights for {model} to protect VRAM.")
            manage_model_lifecycle(model, None, config.ollama_base_url)
    elif ablation:
        # Prompt Ablation Study (REQ41)
        model = config.models[0]
        if not check_model_available(model, config.ollama_base_url):
            logger.error(f"Target model {model} not available for prompt ablation study.")
            return
            
        conditions = {
            "zs-en": "SYSTEM_PROMPT.md",
            "zs-es": "SYSTEM_PROMPT_ES.md",
            "fs-es": "SYSTEM_PROMPT_ES_FEWSHOT.md",
            "fs-en": "SYSTEM_PROMPT_EN_FEWSHOT.md"
        }
        
        for condition_name, prompt_file in conditions.items():
            # Clear task queue for this specific condition
            task_queue = create_task_queue(use_redis=False)
            published_count = 0
            
            for batch_idx in range(total_batches):
                if is_batch_completed(state, condition_name, batch_idx):
                    continue
                batch_records = dataset.get_batch(batch_idx)
                if not batch_records:
                    continue
                task_msg = TaskMessage(
                    task_id=f"{condition_name}-b{batch_idx}-{int(time.time())}",
                    batch_idx=batch_idx,
                    model_name=model,
                    records=batch_records,
                    created_at=datetime.now(timezone.utc).isoformat(),
                    prompt_file=prompt_file,
                    condition_name=condition_name
                )
                task_queue.publish(task_msg)
                published_count += 1
                
            if published_count > 0:
                num_queue_workers = adaptive_ctrl.current_workers
                logger.info(
                    f"Running ablation condition '{condition_name}' with "
                    f"{num_queue_workers} parallel workers (AIMD adaptive)..."
                )
                def worker_consumer(worker_id: int):
                    while True:
                        claimed_task = task_queue.subscribe()
                        if not claimed_task:
                            break
                        task_prompt = load_system_prompt(claimed_task.prompt_file)
                        try:
                            batch_results = process_batch(
                                batch=claimed_task.records,
                                model=claimed_task.model_name,
                                system_prompt=task_prompt,
                                config=config,
                                batch_idx=claimed_task.batch_idx,
                                condition_name=claimed_task.condition_name
                            )
                            task_queue.acknowledge(claimed_task.task_id)
                            with state_lock:
                                mark_batch_completed(state, claimed_task.model_name, claimed_task.batch_idx, batch_results)
                                save_checkpoint(state, checkpoint_path)
                            new_w = adaptive_ctrl.report_success()
                            config.num_workers = new_w
                        except Exception as exc:
                            is_rl = is_rate_limit_exception(exc)
                            new_w = adaptive_ctrl.report_error(is_rate_limit=is_rl)
                            config.num_workers = new_w
                            logger.error(
                                f"[Worker {worker_id}] Error processing task "
                                f"'{claimed_task.task_id}': {exc}. "
                                f"AIMD workers → {new_w}"
                            )

                with ThreadPoolExecutor(max_workers=num_queue_workers) as executor:
                    futures = [executor.submit(worker_consumer, idx + 1) for idx in range(num_queue_workers)]
                    for future in futures:
                        future.result()

                logger.info(
                    f"[AIMD] Ablation '{condition_name}' done. "
                    f"Controller status: {adaptive_ctrl.get_status()}"
                )
                
        # Unload model weights after ablation completes
        logger.info(f"Unloading model weights for {model} to protect VRAM.")
        manage_model_lifecycle(model, None, config.ollama_base_url)
        
    else:
        # Standard model benchmarking sweep
        from src.providers.factory import LLMProviderFactory
        for model in config.models:
            provider_type = LLMProviderFactory.detect_provider_name(model)
            if provider_type == "ollama" and not check_model_available(model, config.ollama_base_url):
                if "mlx" in model.lower():
                    logger.warning(f"Model {model} not pulled in Ollama. Proceeding with soft fallback support.")
                else:
                    logger.warning(f"Skipping model {model} because it is not available in Ollama.")
                    continue
                
            # Clear task queue for this specific model
            task_queue = create_task_queue(use_redis=False)
            published_count = 0
            
            for batch_idx in range(total_batches):
                if is_batch_completed(state, model, batch_idx):
                    continue
                batch_records = dataset.get_batch(batch_idx)
                if not batch_records:
                    continue
                task_msg = TaskMessage(
                    task_id=f"{model}-b{batch_idx}-{int(time.time())}",
                    batch_idx=batch_idx,
                    model_name=model,
                    records=batch_records,
                    created_at=datetime.now(timezone.utc).isoformat(),
                    prompt_file=config.system_prompt_file
                )
                task_queue.publish(task_msg)
                published_count += 1
                
            if published_count > 0:
                num_queue_workers = adaptive_ctrl.current_workers
                logger.info(
                    f"Running model '{model}' with {num_queue_workers} workers "
                    f"(AIMD adaptive, circuit={adaptive_ctrl.get_status()['circuit_state']})..."
                )
                def worker_consumer(worker_id: int):
                    while True:
                        claimed_task = task_queue.subscribe()
                        if not claimed_task:
                            break
                        task_prompt = load_system_prompt(claimed_task.prompt_file)
                        try:
                            batch_results = process_batch(
                                batch=claimed_task.records,
                                model=claimed_task.model_name,
                                system_prompt=task_prompt,
                                config=config,
                                batch_idx=claimed_task.batch_idx,
                                condition_name=claimed_task.condition_name
                            )
                            task_queue.acknowledge(claimed_task.task_id)
                            with state_lock:
                                mark_batch_completed(state, claimed_task.model_name, claimed_task.batch_idx, batch_results)
                                save_checkpoint(state, checkpoint_path)
                            new_w = adaptive_ctrl.report_success()
                            config.num_workers = new_w
                        except Exception as exc:
                            is_rl = is_rate_limit_exception(exc)
                            new_w = adaptive_ctrl.report_error(is_rate_limit=is_rl)
                            config.num_workers = new_w
                            logger.error(
                                f"[Worker {worker_id}] Error processing task "
                                f"'{claimed_task.task_id}': {exc}. "
                                f"AIMD workers → {new_w}"
                            )

                with ThreadPoolExecutor(max_workers=num_queue_workers) as executor:
                    futures = [executor.submit(worker_consumer, idx + 1) for idx in range(num_queue_workers)]
                    for future in futures:
                        future.result()

                logger.info(
                    f"[AIMD] Model '{model}' done. "
                    f"Controller status: {adaptive_ctrl.get_status()}"
                )
                
            # Unload model weights after model completes to protect VRAM before starting next model
            if provider_type == "ollama":
                logger.info(f"Unloading model weights for {model} to protect VRAM.")
                manage_model_lifecycle(model, None, config.ollama_base_url)
        
    # End of pipeline processing
    logger.info("==================================================")
    logger.info("BENCHMARK EXTRACTIONS COMPLETE. PROCESSING METRICS...")
    logger.info("==================================================")
    
    if not state.results:
        logger.error("No benchmark results generated.")
        return
        
    # §2.bis.1: la métrica publicada (summary, matriz de confusión, informe estadístico) se calcula sobre
    # los resultados SIN los artículos contaminados en los modos kb afectados. El crudo (state.results,
    # que exporta detailed_results.json) se conserva íntegro.
    metric_results = _excluir_contaminados(state.results, config.rag_mode)

    # Aggregate summary stats
    summary = aggregate_model_results(metric_results)

    # Calculate confusion matrix parameters
    confusion = build_confusion_matrix(metric_results)

    # Group results by model for statistical reporting
    model_results = {}
    for r in metric_results:
        model_name = r["model"]
        if model_name not in model_results:
            model_results[model_name] = []
        model_results[model_name].append(r)
        
    # Run statistical validation tests (ANOVA, Tukey + Sensitivity)
    stat_report = generate_statistical_report(model_results, config.data_file)
    
    # Export all files
    export_results(state.results, summary, stat_report, confusion, config)
    
    # Print clean summary to console
    print("\n" + "="*50)
    print("      FINAL BENCHMARK PERFORMANCE RESULTS")
    print("="*50)
    df_summary = pd.DataFrame(summary).T
    print(df_summary[["f1", "precision", "recall", "hallucination_rate", "latency_sec"]].to_string())
    print("="*50)
    print("Full reports saved under: results/ directory.")

def run_annotator_comparison(file1: str, file2: str) -> None:
    """Compares ground truth classifications between two files and prints Cohen's Kappa agreement."""
    from src.data_loader import load_all_records
    from src.statistics import calculate_cohens_kappa
    
    records1 = {r["id"]: r for r in load_all_records(file1)}
    records2 = {r["id"]: r for r in load_all_records(file2)}
    
    common_ids = set(records1.keys()) & set(records2.keys())
    if not common_ids:
        print("Error: No overlapping record IDs found between the two files.")
        return
        
    print(f"Comparing {len(common_ids)} overlapping records...")
    
    labels1 = []
    labels2 = []
    
    categories = ["Persons", "Organizations", "Locations"]
    for rid in sorted(common_ids):
        r1 = records1[rid]
        r2 = records2[rid]
        
        gt1 = r1.get("ground_truth", {})
        gt2 = r2.get("ground_truth", {})
        
        for cat in categories:
            list1 = gt1.get(cat, [])
            list2 = gt2.get(cat, [])
            labels1.append(1 if list1 else 0)
            labels2.append(1 if list2 else 0)
            
    kappa = calculate_cohens_kappa(labels1, labels2)
    print(f"\n=========================================")
    print(f"INTER-ANNOTATOR AGREEMENT REPORT (US02)")
    print(f"=========================================")
    print(f"Computed Cohen's Kappa: {kappa:.4f}")
    if kappa < 0.75:
        print(f"⚠️  WARNING: Cohen's Kappa is below the threshold of 0.75 (Kappa: {kappa:.4f}).")
        print(f"   Ground truth reliability is low. Please align annotator guidelines.")
    else:
        print(f"✅ SUCCESS: Cohen's Kappa meets reliability standards (Kappa: {kappa:.4f} >= 0.75).")
    print(f"=========================================\n")

def main():
    parser = argparse.ArgumentParser(description="Sanctions LLM Entity NER Benchmark Orchestrator")
    parser.add_argument("--models", nargs="+", help="List of Ollama models to benchmark")
    parser.add_argument("--batch-size", type=int, default=5, help="Batch size of articles per iteration")
    parser.add_argument("--data-file", type=str, default="data/sample_sanctions.json", help="Path to evaluation JSONL")
    parser.add_argument("--resume", action="store_true", help="Resume from last checkpoint")
    parser.add_argument("--results-dir", type=str, default=None, help="Explicit results directory. Required for --resume to find its checkpoint; without it a new timestamped directory is created each run.")
    parser.add_argument("--generate-sample-data", action="store_true", help="Generate 20-record sample dataset and exit")
    parser.add_argument("--temperature", type=float, default=0.1, help="LLM temperature configuration")
    parser.add_argument("--max-tokens", type=int, default=2048, help="LLM max output tokens limit")
    parser.add_argument("--seed", type=int, default=42, help="Seed value for reproducibility")
    parser.add_argument("--system-prompt-file", type=str, default="SYSTEM_PROMPT.md", help="Path to system prompt MD file")
    parser.add_argument("--compare-annotators", nargs=2, metavar=("FILE1", "FILE2"), help="Compute Cohen's Kappa inter-annotator agreement between two ground truth files")
    parser.add_argument("--ablation", action="store_true", help="Perform prompt ablation study comparing Zero-Shot EN, Zero-Shot ES, and Few-Shot ES prompts (REQ41)")
    parser.add_argument("--rag-study", action="store_true", help="Perform RAG integration study with and without dictionaries")
    parser.add_argument(
        "--rag-mode",
        type=str,
        default="entities",
        choices=["entities", "kb_guidelines", "kb_fewshot", "kb_combined"],
        help=(
            "RAG retrieval strategy (only used with --rag-study). "
            "'entities': legacy entity dict (original behavior, default). "
            "'kb_guidelines': domain NER disambiguation rules. "
            "'kb_fewshot': dynamic few-shot annotated example. "
            "'kb_combined': guidelines + exemplar (recommended, best F1). "
            "See: research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md"
        ),
    )
    parser.add_argument("--num-workers", type=int, default=2, help="Number of concurrent worker threads")
    parser.add_argument("--max-workers", type=int, default=None,
                        help="Hard cap on concurrent workers (AIMD never grows past this). "
                             "Use for cloud/quota-limited models, e.g. 1.")
    parser.add_argument("--request-delay", type=float, default=0.0,
                        help="Minimum seconds between LLM requests (global rate limit). "
                             "Use for cloud/quota-limited models, e.g. 4.0.")

    args = parser.parse_args()
    
    if args.compare_annotators:
        run_annotator_comparison(args.compare_annotators[0], args.compare_annotators[1])
        return
        
    if args.generate_sample_data:
        print(f"Generating realistic sample sanctions dataset at {args.data_file}...")
        create_sample_dataset(args.data_file)
        print("Dataset generated successfully.")
        return
        
    # Setup configuration overrides
    config = BenchmarkConfig(
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        data_file=args.data_file,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        seed=args.seed,
        system_prompt_file=args.system_prompt_file,
        rag_study=args.rag_study,
        rag_mode=args.rag_mode,
        ablation=args.ablation,
        **(
            {
                "results_dir": args.results_dir,
                "checkpoint_file": os.path.join(args.results_dir, ".checkpoint.json"),
            }
            if args.results_dir
            else {}
        ),
    )
    if args.models:
        config.models = args.models

    # Rate limiting / paralelismo tope para modelos cloud sujetos a cuota (2026-09-06).
    config.max_workers = args.max_workers  # None = auto (cpu-2); un entero lo topa
    if args.request_delay and args.request_delay > 0:
        os.environ["OLLAMA_REQUEST_DELAY_SEC"] = str(args.request_delay)
        logger.info("Rate limit activo: mínimo %.2fs entre requests LLM.", args.request_delay)
    if args.max_workers is not None:
        logger.info("Paralelismo topado a max_workers=%d.", args.max_workers)

    # Ensure sample data is present if file not found
    if not os.path.exists(config.data_file):
        logger.info(f"Data file '{config.data_file}' not found. Seeding with realistic sample sanctions records...")
        create_sample_dataset(config.data_file)
        
    run_benchmark(config, resume=args.resume, ablation=args.ablation)

if __name__ == "__main__":
    main()
