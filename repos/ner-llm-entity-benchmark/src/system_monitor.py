"""
system_monitor.py — Real-time resource telemetry for LLM inference.

Captures per-request CPU, RAM, and Ollama VRAM metrics using a background
sampling thread. Results are attached to each benchmark record for full
reproducibility and hardware efficiency analysis.
"""
from __future__ import annotations
import os
import time
import threading
import logging
from dataclasses import dataclass, field, asdict

import psutil
import requests

logger = logging.getLogger("ner_benchmark.system_monitor")

# ── Dataclass for one sample snapshot ─────────────────────────────────────────

@dataclass
class ResourceSnapshot:
    timestamp: float = 0.0
    cpu_pct: float = 0.0          # system-wide CPU %
    proc_cpu_pct: float = 0.0     # benchmark process CPU %
    rss_mb: float = 0.0           # benchmark process RSS (MB)
    sys_mem_used_mb: float = 0.0  # system-wide used RAM (MB)
    sys_mem_pct: float = 0.0      # system-wide RAM %

# ── Aggregated metrics returned after inference ────────────────────────────────

@dataclass
class InferenceResourceMetrics:
    # CPU
    avg_cpu_pct: float = 0.0
    peak_cpu_pct: float = 0.0
    avg_proc_cpu_pct: float = 0.0
    peak_proc_cpu_pct: float = 0.0
    # RAM
    avg_mem_mb: float = 0.0
    peak_mem_mb: float = 0.0
    avg_sys_mem_mb: float = 0.0
    peak_sys_mem_mb: float = 0.0
    avg_sys_mem_pct: float = 0.0
    # VRAM / Ollama model info
    vram_mb: float = 0.0           # VRAM used by active Ollama models (MB)
    model_disk_mb: float = 0.0     # Model size on disk (MB) from Ollama API
    # Sampling info
    sample_count: int = 0
    duration_sec: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

# ── Main context-manager monitor ──────────────────────────────────────────────

class SystemMonitor:
    """
    Context manager that samples CPU and RAM during LLM inference.

    Usage:
        with SystemMonitor(model_name="qwen3:8b") as mon:
            result = client.chat(...)
        metrics = mon.metrics   # InferenceResourceMetrics
    """

    def __init__(
        self,
        model_name: str = "",
        sample_interval: float = 0.5,
        ollama_base_url: str = "http://localhost:11434",
    ):
        self.model_name = model_name
        self.sample_interval = sample_interval
        self.ollama_base_url = ollama_base_url

        self._samples: list[ResourceSnapshot] = []
        self._running = False
        self._thread: threading.Thread | None = None
        self._process = psutil.Process(os.getpid())
        self._start_time: float = 0.0
        self._end_time: float = 0.0
        self.metrics: InferenceResourceMetrics = InferenceResourceMetrics()

    # ── Context manager ──────────────────────────────────────────────────────

    def __enter__(self) -> "SystemMonitor":
        self._samples.clear()
        self._running = True
        self._start_time = time.time()
        # Warm up psutil cpu_percent (first call always returns 0.0)
        self._process.cpu_percent(interval=None)
        psutil.cpu_percent(interval=None)
        self._thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *args) -> None:
        self._end_time = time.time()
        self._running = False
        if self._thread:
            self._thread.join(timeout=max(self.sample_interval * 3, 2.0))
        self._compute_metrics()

    # ── Sampling loop ────────────────────────────────────────────────────────

    def _sample_loop(self) -> None:
        while self._running:
            try:
                snap = ResourceSnapshot(
                    timestamp=time.time(),
                    cpu_pct=psutil.cpu_percent(interval=None),
                    proc_cpu_pct=self._process.cpu_percent(interval=None),
                    rss_mb=self._process.memory_info().rss / 1024 / 1024,
                    sys_mem_used_mb=psutil.virtual_memory().used / 1024 / 1024,
                    sys_mem_pct=psutil.virtual_memory().percent,
                )
                self._samples.append(snap)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception as exc:
                logger.debug(f"SystemMonitor sample error: {exc}")
            time.sleep(self.sample_interval)

    # ── Metric aggregation ───────────────────────────────────────────────────

    def _compute_metrics(self) -> None:
        n = len(self._samples)
        duration = self._end_time - self._start_time

        if n == 0:
            self.metrics = InferenceResourceMetrics(duration_sec=round(duration, 3))
            return

        def avg(vals): return sum(vals) / len(vals)
        def peak(vals): return max(vals)

        cpu_pcts      = [s.cpu_pct for s in self._samples]
        proc_cpus     = [s.proc_cpu_pct for s in self._samples]
        rss_mbs       = [s.rss_mb for s in self._samples]
        sys_mem_mbs   = [s.sys_mem_used_mb for s in self._samples]
        sys_mem_pcts  = [s.sys_mem_pct for s in self._samples]

        vram_mb, disk_mb = self._query_ollama_resources()

        self.metrics = InferenceResourceMetrics(
            avg_cpu_pct=round(avg(cpu_pcts), 1),
            peak_cpu_pct=round(peak(cpu_pcts), 1),
            avg_proc_cpu_pct=round(avg(proc_cpus), 1),
            peak_proc_cpu_pct=round(peak(proc_cpus), 1),
            avg_mem_mb=round(avg(rss_mbs), 1),
            peak_mem_mb=round(peak(rss_mbs), 1),
            avg_sys_mem_mb=round(avg(sys_mem_mbs), 1),
            peak_sys_mem_mb=round(peak(sys_mem_mbs), 1),
            avg_sys_mem_pct=round(avg(sys_mem_pcts), 1),
            vram_mb=vram_mb,
            model_disk_mb=disk_mb,
            sample_count=n,
            duration_sec=round(duration, 3),
        )

    def _query_ollama_resources(self) -> tuple[float, float]:
        """Queries Ollama /api/ps for loaded model VRAM and /api/tags for disk size."""
        vram_mb = 0.0
        disk_mb = 0.0
        try:
            ps_resp = requests.get(
                f"{self.ollama_base_url}/api/ps", timeout=3
            )
            if ps_resp.status_code == 200:
                ps_data = ps_resp.json()
                for m in ps_data.get("models", []):
                    if self.model_name and self.model_name in m.get("name", ""):
                        size_vram = m.get("size_vram", 0) or 0
                        vram_mb = round(size_vram / 1024 / 1024, 1)
                        break
                # If not matched by name, take the largest loaded model
                if vram_mb == 0.0 and ps_data.get("models"):
                    total = sum(
                        (m.get("size_vram") or 0) for m in ps_data["models"]
                    )
                    vram_mb = round(total / 1024 / 1024, 1)
        except Exception as exc:
            logger.debug(f"VRAM query error: {exc}")

        try:
            tags_resp = requests.get(
                f"{self.ollama_base_url}/api/tags", timeout=3
            )
            if tags_resp.status_code == 200:
                for m in tags_resp.json().get("models", []):
                    if self.model_name and self.model_name in m.get("name", ""):
                        disk_mb = round((m.get("size") or 0) / 1024 / 1024, 1)
                        break
        except Exception as exc:
            logger.debug(f"Disk size query error: {exc}")

        return vram_mb, disk_mb


# ── Batch-level throughput tracker ────────────────────────────────────────────

class ThroughputTracker:
    """
    Tracks request-level throughput across an entire model benchmark run.

    Records timestamp of each completed request to compute:
      - requests per second (overall and rolling)
      - latency percentiles (p50, p95, p99)
    """

    def __init__(self):
        self._latencies: list[float] = []
        self._timestamps: list[float] = []
        self._start: float = time.time()

    def record(self, latency_sec: float) -> None:
        self._latencies.append(latency_sec)
        self._timestamps.append(time.time())

    @property
    def count(self) -> int:
        return len(self._latencies)

    @property
    def wall_time_sec(self) -> float:
        if not self._timestamps:
            return 0.0
        return self._timestamps[-1] - self._start

    @property
    def requests_per_sec(self) -> float:
        wt = self.wall_time_sec
        return round(self.count / wt, 4) if wt > 0 else 0.0

    def percentile(self, pct: float) -> float:
        """Returns the p-th percentile latency (e.g. pct=95 → p95)."""
        if not self._latencies:
            return 0.0
        sorted_lats = sorted(self._latencies)
        idx = int(len(sorted_lats) * pct / 100)
        idx = min(idx, len(sorted_lats) - 1)
        return round(sorted_lats[idx], 3)

    def summary(self) -> dict:
        lats = self._latencies
        if not lats:
            return {}
        return {
            "req_count": self.count,
            "requests_per_sec": self.requests_per_sec,
            "wall_time_sec": round(self.wall_time_sec, 2),
            "latency_p50_sec": self.percentile(50),
            "latency_p95_sec": self.percentile(95),
            "latency_p99_sec": self.percentile(99),
            "latency_min_sec": round(min(lats), 3),
            "latency_max_sec": round(max(lats), 3),
            "latency_avg_sec": round(sum(lats) / len(lats), 3),
        }
