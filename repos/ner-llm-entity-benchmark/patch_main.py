import os

def patch_main():
    file_path = "src/main.py"
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Patch 1: Producer phase
        if "if ablation:" in line and "Prompt Ablation Study (REQ41): cycle through prompt configurations" in lines[i+1]:
            # Inject rag_study
            out_lines.append("    if config.rag_study:\n")
            out_lines.append("        rag_mgr = RAGManager()\n")
            out_lines.append("        rag_mgr.load_dictionaries()\n")
            out_lines.append("        for model in config.models:\n")
            out_lines.append("            if not check_model_available(model, config.ollama_base_url):\n")
            out_lines.append("                continue\n")
            out_lines.append("            for condition_name in ['baseline', 'rag_enhanced']:\n")
            out_lines.append("                condition_key = f\"{model}_{condition_name}\"\n")
            out_lines.append("                for batch_idx in range(total_batches):\n")
            out_lines.append("                    if is_batch_completed(state, condition_key, batch_idx):\n")
            out_lines.append("                        continue\n")
            out_lines.append("                    batch_records = dataset.get_batch(batch_idx)\n")
            out_lines.append("                    if not batch_records:\n")
            out_lines.append("                        continue\n")
            out_lines.append("                    task_msg = TaskMessage(\n")
            out_lines.append("                        task_id=f\"{condition_key}-b{batch_idx}-{int(time.time())}\",\n")
            out_lines.append("                        batch_idx=batch_idx,\n")
            out_lines.append("                        model_name=model,\n")
            out_lines.append("                        records=batch_records,\n")
            out_lines.append("                        created_at=datetime.now(timezone.utc).isoformat(),\n")
            out_lines.append("                        prompt_file=config.system_prompt_file,\n")
            out_lines.append("                        condition_name=condition_key\n")
            out_lines.append("                    )\n")
            out_lines.append("                    task_queue.publish(task_msg)\n")
            out_lines.append("                    published_count += 1\n")
            out_lines.append("    elif ablation:\n")
            i += 1
            continue
            
        # Patch 2: Consumer phase
        if "if ablation:" in line and "Prompt Ablation Study (REQ41)" in lines[i+1]:
            out_lines.append("    if config.rag_study:\n")
            out_lines.append("        rag_mgr = RAGManager()\n")
            out_lines.append("        for model in config.models:\n")
            out_lines.append("            if not check_model_available(model, config.ollama_base_url):\n")
            out_lines.append("                continue\n")
            out_lines.append("            for condition_name in ['baseline', 'rag_enhanced']:\n")
            out_lines.append("                condition_key = f\"{model}_{condition_name}\"\n")
            out_lines.append("                task_queue = create_task_queue(use_redis=False)\n")
            out_lines.append("                published_count = 0\n")
            out_lines.append("                for batch_idx in range(total_batches):\n")
            out_lines.append("                    if is_batch_completed(state, condition_key, batch_idx):\n")
            out_lines.append("                        continue\n")
            out_lines.append("                    batch_records = dataset.get_batch(batch_idx)\n")
            out_lines.append("                    if not batch_records:\n")
            out_lines.append("                        continue\n")
            out_lines.append("                    task_msg = TaskMessage(\n")
            out_lines.append("                        task_id=f\"{condition_key}-b{batch_idx}-{int(time.time())}\",\n")
            out_lines.append("                        batch_idx=batch_idx,\n")
            out_lines.append("                        model_name=model,\n")
            out_lines.append("                        records=batch_records,\n")
            out_lines.append("                        created_at=datetime.now(timezone.utc).isoformat(),\n")
            out_lines.append("                        prompt_file=config.system_prompt_file,\n")
            out_lines.append("                        condition_name=condition_key\n")
            out_lines.append("                    )\n")
            out_lines.append("                    task_queue.publish(task_msg)\n")
            out_lines.append("                    published_count += 1\n")
            out_lines.append("                if published_count > 0:\n")
            out_lines.append("                    num_queue_workers = adaptive_ctrl.current_workers\n")
            out_lines.append("                    logger.info(f\"Running RAG study '{condition_key}' with {num_queue_workers} workers...\")\n")
            out_lines.append("                    def worker_consumer(worker_id: int):\n")
            out_lines.append("                        while True:\n")
            out_lines.append("                            claimed_task = task_queue.subscribe()\n")
            out_lines.append("                            if not claimed_task: break\n")
            out_lines.append("                            task_prompt = load_system_prompt(claimed_task.prompt_file)\n")
            out_lines.append("                            active_rag = rag_mgr if 'rag_enhanced' in claimed_task.condition_name else None\n")
            out_lines.append("                            try:\n")
            out_lines.append("                                batch_results = process_batch(\n")
            out_lines.append("                                    batch=claimed_task.records,\n")
            out_lines.append("                                    model=claimed_task.model_name,\n")
            out_lines.append("                                    system_prompt=task_prompt,\n")
            out_lines.append("                                    config=config,\n")
            out_lines.append("                                    batch_idx=claimed_task.batch_idx,\n")
            out_lines.append("                                    condition_name=claimed_task.condition_name,\n")
            out_lines.append("                                    rag_manager=active_rag\n")
            out_lines.append("                                )\n")
            out_lines.append("                                task_queue.acknowledge(claimed_task.task_id)\n")
            out_lines.append("                                with state_lock:\n")
            out_lines.append("                                    mark_batch_completed(state, claimed_task.condition_name, claimed_task.batch_idx, batch_results)\n")
            out_lines.append("                                    save_checkpoint(state, checkpoint_path)\n")
            out_lines.append("                                new_w = adaptive_ctrl.report_success()\n")
            out_lines.append("                                config.num_workers = new_w\n")
            out_lines.append("                            except Exception as exc:\n")
            out_lines.append("                                is_rl = is_rate_limit_exception(exc)\n")
            out_lines.append("                                new_w = adaptive_ctrl.report_error(is_rate_limit=is_rl)\n")
            out_lines.append("                                config.num_workers = new_w\n")
            out_lines.append("                                logger.error(f\"[Worker {worker_id}] Error: {exc}\")\n")
            out_lines.append("                    with ThreadPoolExecutor(max_workers=num_queue_workers) as executor:\n")
            out_lines.append("                        futures = [executor.submit(worker_consumer, idx + 1) for idx in range(num_queue_workers)]\n")
            out_lines.append("                        for future in futures: future.result()\n")
            out_lines.append("            logger.info(f\"Unloading model weights for {model} to protect VRAM.\")\n")
            out_lines.append("            manage_model_lifecycle(model, None, config.ollama_base_url)\n")
            out_lines.append("    elif ablation:\n")
            i += 1
            continue

        out_lines.append(line)
        i += 1
        
    with open(file_path, "w") as f:
        f.writelines(out_lines)
    print("Patched main.py successfully.")

if __name__ == "__main__":
    patch_main()
