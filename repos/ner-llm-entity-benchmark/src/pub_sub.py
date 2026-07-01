from __future__ import annotations
import json
import logging
import queue
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

# Configure module logger
logger = logging.getLogger("ner_benchmark.pub_sub")

@dataclass
class TaskMessage:
    task_id: str
    batch_idx: int
    model_name: str
    records: list[dict]
    created_at: str
    prompt_file: str = "SYSTEM_PROMPT.md"
    condition_name: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

@dataclass
class TaskResult:
    task_id: str
    batch_idx: int
    model_name: str
    results: list[dict]
    completed_at: str
    success: bool
    error: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

class AbstractTaskQueue(ABC):
    @abstractmethod
    def publish(self, message: TaskMessage) -> None:
        pass

    @abstractmethod
    def subscribe(self) -> TaskMessage | None:
        pass

    @abstractmethod
    def acknowledge(self, task_id: str) -> None:
        pass

    @abstractmethod
    def get_pending_count(self) -> int:
        pass

class InMemoryTaskQueue(AbstractTaskQueue):
    """Thread-safe queue for local standard testing."""
    def __init__(self):
        self._queue = queue.Queue()
        self._in_flight = {}
        import threading
        self._lock = threading.Lock()

    def publish(self, message: TaskMessage) -> None:
        self._queue.put(message)
        logger.info(f"Published task {message.task_id} for batch {message.batch_idx} to memory queue.")

    def subscribe(self) -> TaskMessage | None:
        try:
            message = self._queue.get_nowait()
            with self._lock:
                self._in_flight[message.task_id] = message
            logger.info(f"Subscribed/Claimed task {message.task_id} from memory queue.")
            return message
        except queue.Empty:
            return None

    def acknowledge(self, task_id: str) -> None:
        with self._lock:
            if task_id in self._in_flight:
                self._in_flight.pop(task_id)
                logger.info(f"Acknowledged task {task_id} in memory queue.")

    def get_pending_count(self) -> int:
        return self._queue.qsize()

class RedisTaskQueue(AbstractTaskQueue):
    """Redis-based task queue for production scale."""
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client = None
        self.queue_name = "ner_benchmark_tasks"
        self.processing_set = "ner_benchmark_processing"
        
        try:
            import redis
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            logger.info(f"Connected successfully to Redis at {redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}. Falling back to in-memory queue simulation.")
            self.client = None

    def publish(self, message: TaskMessage) -> None:
        if not self.client:
            logger.warning("Redis client unavailable. Simulating publish in memory.")
            return
        self.client.rpush(self.queue_name, message.to_json())
        logger.info(f"Published task {message.task_id} to Redis list.")

    def subscribe(self) -> TaskMessage | None:
        if not self.client:
            return None
        
        # Atomic pop from queue and push to processing set for resumability
        task_data = self.client.lpop(self.queue_name)
        if task_data:
            try:
                task_dict = json.loads(task_data)
                message = TaskMessage(**task_dict)
                self.client.hset(self.processing_set, message.task_id, task_data)
                logger.info(f"Subscribed and claimed task {message.task_id} from Redis.")
                return message
            except Exception as e:
                logger.error(f"Error parsing task from Redis: {e}")
        return None

    def acknowledge(self, task_id: str) -> None:
        if not self.client:
            return
        self.client.hdel(self.processing_set, task_id)
        logger.info(f"Acknowledged and removed task {task_id} from Redis processing set.")

    def get_pending_count(self) -> int:
        if not self.client:
            return 0
        return self.client.llen(self.queue_name)

def create_task_queue(use_redis: bool = False, redis_url: str = 'redis://localhost:6379') -> AbstractTaskQueue:
    """Factory to spin up appropriate queue."""
    if use_redis:
        try:
            return RedisTaskQueue(redis_url)
        except Exception:
            logger.warning("Falling back to InMemoryTaskQueue due to connection failure.")
    return InMemoryTaskQueue()
