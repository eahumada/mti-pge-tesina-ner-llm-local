"""
adaptive_workers.py — AIMD Adaptive Worker Controller
======================================================
Implements an Additive Increase / Multiplicative Decrease (AIMD) algorithm
for dynamically adjusting the number of concurrent worker threads, inspired
by TCP congestion control and adapted for LLM API rate-limiting scenarios.

Algorithm:
  • Multiplicative Decrease (MD): On rate-limit error (HTTP 429, quota exhaustion,
    or model overload), cut workers in half (floor of current / 2), respecting
    min_workers. This reacts aggressively to back-pressure signals.
  • Additive Increase (AI): If there have been no errors for `stable_window_sec`
    (default 10 min), increase workers by +1 every `increase_interval_sec`
    (default 2 min), up to a ceiling of 75 % of max_workers.

Circuit Breaker states:
  CLOSED  → normal operation, requests flow through.
  OPEN    → too many consecutive failures; workers are pinned at 1.
  HALF_OPEN → probing recovery after cool-down period.

Thread Safety:
  All state mutations are guarded by a single threading.Lock().

References:
  - Jacobson, V. (1988). "Congestion avoidance and control." ACM SIGCOMM.
  - Brooker, M. (2022). "Retry Strategies in Distributed Systems." AWS Blog.
  - Netflix Hystrix / Resilience4j circuit-breaker patterns.
"""
from __future__ import annotations

import logging
import os
import threading
import time
from enum import Enum
from typing import Optional

logger = logging.getLogger("ner_benchmark.adaptive_workers")


# ──────────────────────────────────────────────────────────────────────────────
# Circuit-Breaker States
# ──────────────────────────────────────────────────────────────────────────────
class CircuitState(Enum):
    CLOSED = "CLOSED"         # Normal — all workers active
    OPEN = "OPEN"             # Tripped — pinned to 1 worker
    HALF_OPEN = "HALF_OPEN"   # Probing — limited workers, watching for success


# ──────────────────────────────────────────────────────────────────────────────
# AdaptiveWorkerController
# ──────────────────────────────────────────────────────────────────────────────
class AdaptiveWorkerController:
    """
    Thread-safe AIMD controller for num_workers concurrency.

    Parameters
    ----------
    min_workers : int
        Absolute lower bound (default: 1).
    max_workers : int
        Absolute upper bound (default: max(1, os.cpu_count() - 2)).
    stable_window_sec : float
        Seconds without any error before the AI phase begins (default: 600 s = 10 min).
    increase_interval_sec : float
        Seconds between each +1 additive increase step (default: 120 s = 2 min).
    ai_ceiling_fraction : float
        Additive Increase is capped at this fraction of max_workers (default: 0.75).
    circuit_failure_threshold : int
        Consecutive errors before circuit breaker opens (default: 5).
    circuit_recovery_sec : float
        Cool-down before the circuit moves to HALF_OPEN (default: 300 s = 5 min).
    initial_workers : int | None
        Starting value; if None, defaults to min_workers.
    """

    def __init__(
        self,
        min_workers: int = 1,
        max_workers: Optional[int] = None,
        stable_window_sec: float = 600.0,
        increase_interval_sec: float = 120.0,
        ai_ceiling_fraction: float = 0.75,
        circuit_failure_threshold: int = 5,
        circuit_recovery_sec: float = 300.0,
        initial_workers: Optional[int] = None,
    ) -> None:
        # ── Bounds ────────────────────────────────────────────────────────────
        self.min_workers = max(1, min_workers)
        if max_workers is None:
            cpu = os.cpu_count() or 2
            max_workers = max(1, cpu - 2)
        self.max_workers = max(self.min_workers, max_workers)

        # Ceiling for additive increase (75 % of max, but never below min)
        self._ai_ceiling = max(
            self.min_workers,
            int(self.max_workers * ai_ceiling_fraction)
        )

        # ── Timing parameters ─────────────────────────────────────────────────
        self._stable_window_sec = stable_window_sec
        self._increase_interval_sec = increase_interval_sec

        # ── State ─────────────────────────────────────────────────────────────
        self._lock = threading.Lock()
        self._workers: int = initial_workers if initial_workers is not None else self.min_workers
        self._workers = max(self.min_workers, min(self._workers, self.max_workers))

        # Timestamps
        self._last_error_ts: float = 0.0          # epoch of last error
        self._last_increase_ts: float = time.monotonic()  # epoch of last AI step
        self._session_start_ts: float = time.monotonic()

        # ── Circuit Breaker ───────────────────────────────────────────────────
        self._circuit_state = CircuitState.CLOSED
        self._consecutive_failures: int = 0
        self._circuit_failure_threshold = max(1, circuit_failure_threshold)
        self._circuit_recovery_sec = circuit_recovery_sec
        self._circuit_open_ts: float = 0.0

        # ── Counters (read-only metrics) ──────────────────────────────────────
        self.total_rate_limit_events: int = 0
        self.total_ai_steps: int = 0
        self.total_md_steps: int = 0

        logger.info(
            "[AIMD] AdaptiveWorkerController initialized | "
            f"workers={self._workers} | min={self.min_workers} | "
            f"max={self.max_workers} | ai_ceiling={self._ai_ceiling} | "
            f"stable_window={stable_window_sec}s | increase_interval={increase_interval_sec}s"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────────

    @property
    def current_workers(self) -> int:
        """Returns the current recommended worker count (thread-safe)."""
        with self._lock:
            return self._workers

    def report_rate_limit_error(self) -> int:
        """
        Call this when a rate-limit / quota / overload error is received from the API.

        Applies Multiplicative Decrease: workers = max(min, floor(current / 2)).
        Also increments the circuit-breaker failure counter.

        Returns
        -------
        int
            The new worker count after the decrease.
        """
        with self._lock:
            now = time.monotonic()
            self.total_rate_limit_events += 1
            self._last_error_ts = now
            self._consecutive_failures += 1

            old = self._workers
            self._workers = max(self.min_workers, self._workers // 2)
            self.total_md_steps += 1

            # Check circuit breaker threshold
            if self._consecutive_failures >= self._circuit_failure_threshold:
                if self._circuit_state != CircuitState.OPEN:
                    self._circuit_state = CircuitState.OPEN
                    self._circuit_open_ts = now
                    self._workers = self.min_workers  # pin to floor
                    logger.warning(
                        f"[AIMD] ⚡ CIRCUIT BREAKER OPENED after "
                        f"{self._consecutive_failures} consecutive failures. "
                        f"Workers pinned to {self._workers}. "
                        f"Recovery probe in {self._circuit_recovery_sec}s."
                    )

            logger.warning(
                f"[AIMD] ⬇  MULTIPLICATIVE DECREASE | "
                f"rate-limit event #{self.total_rate_limit_events} | "
                f"workers {old} → {self._workers} | "
                f"circuit={self._circuit_state.value}"
            )
            return self._workers

    def report_success(self) -> int:
        """
        Call this after a successful task completion (no rate-limit error).

        • Resets the consecutive failure counter.
        • Evaluates whether Additive Increase should be applied.
        • Manages HALF_OPEN → CLOSED circuit-breaker transitions.

        Returns
        -------
        int
            The current (possibly increased) worker count.
        """
        with self._lock:
            now = time.monotonic()
            self._consecutive_failures = 0  # reset on success

            # ── Circuit breaker recovery ───────────────────────────────────────
            if self._circuit_state == CircuitState.OPEN:
                elapsed_since_open = now - self._circuit_open_ts
                if elapsed_since_open >= self._circuit_recovery_sec:
                    self._circuit_state = CircuitState.HALF_OPEN
                    logger.info(
                        "[AIMD] 🔄 CIRCUIT BREAKER → HALF_OPEN: "
                        f"probing recovery after {elapsed_since_open:.0f}s. "
                        "Allowing limited AI steps."
                    )
                else:
                    # Still open; do not increase
                    return self._workers

            if self._circuit_state == CircuitState.HALF_OPEN:
                # One success in HALF_OPEN is sufficient to re-close
                self._circuit_state = CircuitState.CLOSED
                logger.info(
                    "[AIMD] ✅ CIRCUIT BREAKER → CLOSED: "
                    "system healthy again. Resuming normal AI increase."
                )

            # ── Additive Increase evaluation ──────────────────────────────────
            secs_since_error = (now - self._last_error_ts) if self._last_error_ts > 0 else (now - self._session_start_ts)
            secs_since_increase = now - self._last_increase_ts

            if (
                secs_since_error >= self._stable_window_sec
                and secs_since_increase >= self._increase_interval_sec
                and self._workers < self._ai_ceiling
            ):
                old = self._workers
                self._workers = min(self._ai_ceiling, self._workers + 1)
                self._last_increase_ts = now
                self.total_ai_steps += 1

                logger.info(
                    f"[AIMD] ⬆  ADDITIVE INCREASE | "
                    f"stable for {secs_since_error:.0f}s (≥{self._stable_window_sec:.0f}s) | "
                    f"workers {old} → {self._workers} | "
                    f"ceiling={self._ai_ceiling} (75% of max={self.max_workers})"
                )

            return self._workers

    def report_error(self, is_rate_limit: bool = False) -> int:
        """
        Unified error reporting entry point.

        Parameters
        ----------
        is_rate_limit : bool
            If True, applies Multiplicative Decrease (AIMD MD phase).
            If False, increments circuit breaker counter without changing worker count.

        Returns
        -------
        int
            The current worker count after any adjustment.
        """
        if is_rate_limit:
            return self.report_rate_limit_error()

        with self._lock:
            self._consecutive_failures += 1
            now = time.monotonic()
            self._last_error_ts = now

            if self._consecutive_failures >= self._circuit_failure_threshold:
                if self._circuit_state != CircuitState.OPEN:
                    old = self._workers
                    self._circuit_state = CircuitState.OPEN
                    self._circuit_open_ts = now
                    self._workers = self.min_workers
                    logger.warning(
                        f"[AIMD] ⚡ CIRCUIT BREAKER OPENED (non-rate-limit errors) | "
                        f"consecutive_failures={self._consecutive_failures} | "
                        f"workers {old} → {self._workers}"
                    )

            logger.debug(
                f"[AIMD] Error reported (non-rate-limit) | "
                f"consecutive={self._consecutive_failures} | workers={self._workers}"
            )
            return self._workers

    def get_status(self) -> dict:
        """Returns a snapshot of the controller's internal state (thread-safe)."""
        with self._lock:
            now = time.monotonic()
            secs_since_error = (
                (now - self._last_error_ts) if self._last_error_ts > 0 else None
            )
            return {
                "current_workers": self._workers,
                "min_workers": self.min_workers,
                "max_workers": self.max_workers,
                "ai_ceiling": self._ai_ceiling,
                "circuit_state": self._circuit_state.value,
                "consecutive_failures": self._consecutive_failures,
                "total_rate_limit_events": self.total_rate_limit_events,
                "total_ai_steps": self.total_ai_steps,
                "total_md_steps": self.total_md_steps,
                "secs_since_last_error": round(secs_since_error, 1) if secs_since_error is not None else None,
                "stable_window_sec": self._stable_window_sec,
                "increase_interval_sec": self._increase_interval_sec,
            }

    def __repr__(self) -> str:  # pragma: no cover
        s = self.get_status()
        return (
            f"<AdaptiveWorkerController workers={s['current_workers']} "
            f"circuit={s['circuit_state']} "
            f"md_steps={s['total_md_steps']} ai_steps={s['total_ai_steps']}>"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Convenience helpers
# ──────────────────────────────────────────────────────────────────────────────

def is_rate_limit_exception(exc: Exception) -> bool:
    """
    Heuristic to detect rate-limit signals from Ollama / cloud API errors.

    Checks for HTTP 429, 503, quota-related messages, and Ollama-specific
    'too many requests' / overload strings.
    """
    msg = str(exc).lower()
    RATE_LIMIT_SIGNALS = (
        "429",
        "too many requests",
        "rate limit",
        "ratelimit",
        "quota",
        "overloaded",
        "capacity",
        "503",
        "service unavailable",
        "exceeded",
    )
    return any(signal in msg for signal in RATE_LIMIT_SIGNALS)
