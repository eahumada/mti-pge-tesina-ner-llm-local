import argparse
import logging
import os
import sys
import json
import time
from datetime import datetime, timezone

# Ensure sibling imports are valid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import BenchmarkConfig, load_system_prompt
from src.pub_sub import create_task_queue
from src.main import process_batch, validate_environment
from src.checkpoint import load_checkpoint, save_checkpoint, mark_batch_completed, CheckpointState

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] worker: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ner_benchmark.worker")

def main():
    parser = argparse.ArgumentParser(description="NER-LLM Benchmark Standalone Distributed Worker Process (REQ-PAR-04)")
    parser.add_argument("--worker-id", type=int, default=1, help="Unique identifier for this worker instance")
    parser.add_argument("--redis-url", type=str, default=None, help="Redis URL to override config settings")
    parser.add_argument("--config-file", type=str, default=None, help="Path to custom config JSON file")
    args = parser.parse_args()

    # Load configuration
    config = BenchmarkConfig()
    if args.config_file and os.path.exists(args.config_file):
        try:
            with open(args.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                for k, v in config_data.items():
                    if hasattr(config, k):
                        setattr(config, k, v)
            logger.info(f"Loaded config parameters from {args.config_file}")
        except Exception as e:
            logger.error(f"Error loading custom config: {e}")

    if args.redis_url:
        config.redis_url = args.redis_url

    logger.info(f"Starting NER Queue Worker Process ID: {args.worker_id}")
    logger.info(f"Connecting to task queue at: {config.redis_url}")

    # Initialize queue (use Redis for distributed execution)
    use_redis = config.redis_url is not None
    task_queue = create_task_queue(use_redis=use_redis, redis_url=config.redis_url)

    if not validate_environment(config):
        logger.error("Local inference environment check failed. Exiting.")
        sys.exit(1)

    system_prompt = load_system_prompt(config.system_prompt_file)
    checkpoint_path = config.checkpoint_file

    logger.info(f"[Worker {args.worker_id}] Ready and listening for incoming queue tasks...")

    # Load state checkpoint
    # Using simple retry backoff for filesystem safety in distributed processes
    def safe_load_state() -> CheckpointState:
        for _ in range(5):
            try:
                state = load_checkpoint(checkpoint_path)
                if state:
                    return state
            except Exception:
                time.sleep(0.5)
        return CheckpointState(config_hash="distributed-worker")

    while True:
        try:
            # Subscribe (atomic claim)
            claimed_task = task_queue.subscribe()
            if not claimed_task:
                # No tasks currently in queue, wait briefly before polling again
                time.sleep(2)
                continue

            logger.info(f"[Worker {args.worker_id}] Claimed task '{claimed_task.task_id}' for model '{claimed_task.model_name}'")

            # Process task
            batch_results = process_batch(
                batch=claimed_task.records,
                model=claimed_task.model_name,
                system_prompt=system_prompt,
                config=config,
                batch_idx=claimed_task.batch_idx
            )

            # Acknowledge task completion in queue
            task_queue.acknowledge(claimed_task.task_id)

            # Thread/Process safe file update backoff loop
            updated = False
            for attempt in range(5):
                try:
                    state = safe_load_state()
                    mark_batch_completed(state, claimed_task.model_name, claimed_task.batch_idx, batch_results)
                    save_checkpoint(state, checkpoint_path)
                    updated = True
                    break
                except Exception as e:
                    logger.warning(f"[Worker {args.worker_id}] Save attempt {attempt+1} failed: {e}. Retrying...")
                    time.sleep(0.5)

            if updated:
                logger.info(f"[Worker {args.worker_id}] Successfully processed and logged task '{claimed_task.task_id}'")
            else:
                logger.error(f"[Worker {args.worker_id}] Failed to save checkpoint state for task '{claimed_task.task_id}'")

        except KeyboardInterrupt:
            logger.info(f"[Worker {args.worker_id}] Shutting down gracefully...")
            break
        except Exception as e:
            logger.error(f"[Worker {args.worker_id}] Unexpected error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
