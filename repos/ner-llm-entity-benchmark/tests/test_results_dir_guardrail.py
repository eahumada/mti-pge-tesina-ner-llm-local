"""Regression tests for the results-directory data-loss guardrail (src/config.py).

Background
----------
The 2026-07-01 run over the augmented N=30 corpus wrote its artifacts into the
results ROOT (`results/`) instead of a timestamped subdirectory. A later run on
2026-07-27 overwrote them, permanently destroying the per-record data of the run
that backs the thesis' headline figure (F1 = 79.03%); only the aggregated
metrics in `benchmark_augmented_30.log` survived.

These tests pin down four behaviours:
  1. a results_dir resolving to the ROOT aborts the run;
  2. an explicit SUBdirectory (as passed via `--results-dir`) is accepted;
  3. the default (no override) still auto-generates the timestamped
     `results/<dataset>_<YYYYmmdd_HHMMSS>` subdirectory exactly as before;
  4. the `ablation` flag is part of the persisted configuration dump.

Run with:  ./venv/bin/python -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.config import (  # noqa: E402
    BenchmarkConfig,
    ResultsDirRootError,
    _is_results_root,
    assert_not_results_root,
    ensure_directories,
)


class ResultsRootAbortsTest(unittest.TestCase):
    """(1) Any spelling of the results ROOT must abort."""

    def setUp(self) -> None:
        self._cwd = os.getcwd()
        os.chdir(REPO_ROOT)

    def tearDown(self) -> None:
        os.chdir(self._cwd)

    def test_root_spellings_are_detected(self) -> None:
        for spelling in [
            "results",
            "results/",
            "./results",
            "results/.",
            "results//",
            "results/sub/..",
            os.path.abspath("results"),
            os.path.abspath("results") + "/",
            "",
            "   ",
        ]:
            with self.subTest(spelling=spelling):
                self.assertTrue(
                    _is_results_root(spelling),
                    f"{spelling!r} should be recognised as the results ROOT",
                )

    def test_assert_helper_raises_on_root(self) -> None:
        with self.assertRaises(ResultsDirRootError) as ctx:
            assert_not_results_root("results")
        msg = str(ctx.exception)
        self.assertIn("ABORT", msg)
        self.assertIn("results ROOT", msg)
        self.assertIn("--results-dir", msg)

    def test_config_aborts_when_results_dir_is_root(self) -> None:
        # `results_dir='results'` alone is rewritten to a timestamped subdir by
        # __post_init__, so force the failure mode the incident produced: a
        # results_dir that stays pointing at the root after __post_init__.
        for spelling in ["results/", "./results", os.path.abspath("results")]:
            with self.subTest(spelling=spelling):
                with self.assertRaises(ResultsDirRootError):
                    BenchmarkConfig(results_dir=spelling)

    def test_ensure_directories_aborts_on_post_construction_mutation(self) -> None:
        """Last line of defence: results_dir mutated to the root after __init__.

        This is exactly the shape of the 2026-07-01 incident — a config that
        ends up pointing at the root by some other route — and no directory
        must be created before the abort.
        """
        cfg = BenchmarkConfig(results_dir="results/tmp_guardrail_probe")
        cfg.results_dir = "results"
        with self.assertRaises(ResultsDirRootError):
            ensure_directories(cfg)
        self.assertFalse(os.path.exists("results/tmp_guardrail_probe"))

    def test_ensure_directories_accepts_a_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "results", "a_run")
            cfg = BenchmarkConfig(results_dir=target)
            ensure_directories(cfg)
            self.assertTrue(os.path.isdir(target))


class ExplicitSubdirectoryTest(unittest.TestCase):
    """(2) `--results-dir results/<name>` must keep working."""

    def setUp(self) -> None:
        self._cwd = os.getcwd()
        os.chdir(REPO_ROOT)

    def tearDown(self) -> None:
        os.chdir(self._cwd)

    def test_explicit_subdirectory_is_accepted(self) -> None:
        explicit = "results/benchmark_x_16models"
        cfg = BenchmarkConfig(
            results_dir=explicit,
            checkpoint_file=os.path.join(explicit, ".checkpoint.json"),
        )
        # No rewrite, no abort: the caller's directory is honoured verbatim.
        self.assertEqual(cfg.results_dir, explicit)
        self.assertEqual(
            cfg.checkpoint_file, "results/benchmark_x_16models/.checkpoint.json"
        )
        self.assertFalse(_is_results_root(cfg.results_dir))

    def test_nested_and_absolute_subdirectories_are_accepted(self) -> None:
        for explicit in [
            "results/ablation/2026-09-03",
            os.path.join(os.path.abspath("results"), "some_run"),
            os.path.join(tempfile.gettempdir(), "results_elsewhere"),
        ]:
            with self.subTest(explicit=explicit):
                cfg = BenchmarkConfig(results_dir=explicit)
                self.assertEqual(cfg.results_dir, explicit)


class DefaultBehaviourUnchangedTest(unittest.TestCase):
    """(3) The default path must behave EXACTLY as before the guardrail."""

    def setUp(self) -> None:
        self._cwd = os.getcwd()
        os.chdir(REPO_ROOT)

    def tearDown(self) -> None:
        os.chdir(self._cwd)

    def test_default_generates_timestamped_subdirectory(self) -> None:
        cfg = BenchmarkConfig()  # no overrides at all
        self.assertRegex(
            cfg.results_dir,
            r"^results/sample_sanctions_\d{8}_\d{6}$",
        )
        self.assertEqual(
            cfg.checkpoint_file,
            os.path.join(cfg.results_dir, ".checkpoint.json"),
        )
        self.assertFalse(_is_results_root(cfg.results_dir))

    def test_default_uses_dataset_name_from_data_file(self) -> None:
        cfg = BenchmarkConfig(data_file="data/benchmark_balanced_120.json")
        m = re.match(r"^results/benchmark_balanced_120_(\d{8}_\d{6})$", cfg.results_dir)
        self.assertIsNotNone(
            m, f"unexpected auto-generated results_dir: {cfg.results_dir!r}"
        )
        self.assertEqual(
            cfg.checkpoint_file,
            os.path.join(cfg.results_dir, ".checkpoint.json"),
        )

    def test_default_does_not_create_directories(self) -> None:
        """__post_init__ must stay side-effect free (ensure_directories does I/O)."""
        cfg = BenchmarkConfig()
        self.assertFalse(os.path.exists(cfg.results_dir))

    def test_other_defaults_are_untouched(self) -> None:
        cfg = BenchmarkConfig()
        self.assertEqual(cfg.batch_size, 5)
        self.assertEqual(cfg.num_workers, 2)
        self.assertEqual(cfg.data_file, "data/sample_sanctions.json")
        self.assertEqual(cfg.system_prompt_file, "SYSTEM_PROMPT.md")
        self.assertEqual(cfg.seed, 42)
        self.assertEqual(cfg.temperature, 0.1)
        self.assertFalse(cfg.rag_study)
        self.assertEqual(cfg.rag_mode, "entities")


class AblationPersistedTest(unittest.TestCase):
    """(4) `ablation` must reach run_config.json."""

    def setUp(self) -> None:
        self._cwd = os.getcwd()
        os.chdir(REPO_ROOT)

    def tearDown(self) -> None:
        os.chdir(self._cwd)

    def test_ablation_defaults_to_false_and_is_dumped(self) -> None:
        dumped = BenchmarkConfig().to_dict()
        self.assertIn("ablation", dumped)
        self.assertIs(dumped["ablation"], False)

    def test_ablation_true_is_dumped(self) -> None:
        dumped = BenchmarkConfig(ablation=True).to_dict()
        self.assertIs(dumped["ablation"], True)

    def test_ablation_survives_json_roundtrip(self) -> None:
        """Mirrors export_results(): json.dump(config.to_dict()) -> run_config.json."""
        cfg = BenchmarkConfig(ablation=True, system_prompt_file="SYSTEM_PROMPT_ES.md")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "run_config.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(cfg.to_dict(), fh, indent=2)
            with open(path, encoding="utf-8") as fh:
                reloaded = json.load(fh)
        self.assertIs(reloaded["ablation"], True)
        self.assertEqual(reloaded["system_prompt_file"], "SYSTEM_PROMPT_ES.md")

    def test_main_wires_cli_flag_into_config(self) -> None:
        """Static check: src/main.py must pass args.ablation into BenchmarkConfig.

        Asserted statically to avoid importing src.main (pulls sklearn/ollama).
        """
        with open(os.path.join(REPO_ROOT, "src", "main.py"), encoding="utf-8") as fh:
            main_src = fh.read()
        self.assertIn("ablation=args.ablation,", main_src)
        self.assertIn("config.ablation = ablation", main_src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
