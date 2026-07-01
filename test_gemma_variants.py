#!/usr/bin/env python3
"""
GEMMA MODELS TESTING SCRIPT
Test multiple Gemma model variants and compare performance

Usage:
    python test_gemma_variants.py --quick          # Test 3 variants (30 min)
    python test_gemma_variants.py --full           # Test all variants (2+ hours)
    python test_gemma_variants.py --model gemma:7b # Test specific model
"""

import os
import json
import time
import subprocess
import psutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys

# Test configuration
MODELS = {
    "baseline": {
        "name": "gemma:7b",
        "alias": "Gemma 7B (Baseline)",
        "variant": "Standard",
        "quantization": "4-bit (default)",
        "expected_vram_gb": 4,
        "expected_f1": 0.70,
        "required": True
    },
    "code": {
        "name": "gemma:7b-code",
        "alias": "Gemma 7B-Code",
        "variant": "Code-optimized",
        "quantization": "4-bit",
        "expected_vram_gb": 4,
        "expected_f1": 0.73,
        "required": False
    },
    "instruct": {
        "name": "gemma:7b-instruct",
        "alias": "Gemma 7B-Instruct",
        "variant": "Instruction-tuned",
        "quantization": "4-bit",
        "expected_vram_gb": 4,
        "expected_f1": 0.71,
        "required": False
    },
    "27b_q4": {
        "name": "gemma:27b-instruct-q4_0",
        "alias": "Gemma 27B-Instruct (Q4)",
        "variant": "Large, quantized",
        "quantization": "4-bit (Q4_0)",
        "expected_vram_gb": 8.5,
        "expected_f1": 0.78,
        "required": False
    },
    "27b_q5": {
        "name": "gemma:27b-instruct-q5_0",
        "alias": "Gemma 27B-Instruct (Q5)",
        "variant": "Large, higher quality",
        "quantization": "5-bit (Q5_0)",
        "expected_vram_gb": 10.5,
        "expected_f1": 0.79,
        "required": False
    }
}

# Prompt for entity extraction
EXTRACTION_PROMPT = """You are a financial compliance entity extraction expert.
Extract ONLY named entities from the following article text.
Return results as JSON with three categories.

Entity Types:
- Persons: Individual names, titles included if relevant
- Organizations: Company names, government agencies, NGOs
- Locations: Countries, cities, regions, geographic features

Article: {text}

Return ONLY valid JSON, no explanation:
{{
  "Persons": [],
  "Organizations": [],
  "Locations": []
}}"""


class GemmaModelTester:
    """Test suite for Gemma model variants"""

    def __init__(self, data_path: str = "data/kleptotrace.json", output_dir: str = "results"):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Load test articles
        self.test_articles = self._load_test_articles()

    def _load_test_articles(self) -> List[Dict]:
        """Load test articles from Kleptotrace dataset"""
        if not self.data_path.exists():
            print(f"❌ Data file not found: {self.data_path}")
            print("   Creating minimal test article...")
            return [{
                "id": "test_001",
                "text": """
                Juan García, director of ABC Corp, met with officials from the
                Santiago Chamber of Commerce yesterday. The meeting discussed
                new compliance requirements. Other attendees included Maria López
                from Banco Metropolitano and representatives from the Ministry of Finance.
                """
            }]

        try:
            with open(self.data_path) as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data[:3]  # Use first 3 articles for testing
                return [data]
        except Exception as e:
            print(f"⚠️  Warning: Could not load data file: {e}")
            return []

    def get_system_memory(self) -> float:
        """Get available system memory in GB"""
        return psutil.virtual_memory().available / (1024**3)

    def download_model(self, model_name: str) -> bool:
        """Download model via Ollama"""
        print(f"  📥 Checking model availability: {model_name}")
        try:
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"    ⏱️  Download timeout (model may be large)")
            return False
        except Exception as e:
            print(f"    ❌ Download failed: {e}")
            return False

    def test_model(self, model_name: str, test_text: str) -> Dict:
        """Run single inference and measure performance"""

        # Record VRAM before
        vram_before = self.get_system_memory()
        time_before = time.time()

        try:
            # Prepare prompt
            prompt = EXTRACTION_PROMPT.format(text=test_text[:500])  # Limit text size

            # Run inference via Ollama API
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout per inference
            )

            # Record timing
            elapsed = time.time() - time_before
            vram_after = self.get_system_memory()
            vram_used = vram_before - vram_after

            # Parse output
            output = result.stdout.strip()

            return {
                "success": True,
                "elapsed_seconds": elapsed,
                "vram_used_gb": max(0, vram_used),  # Can't be negative
                "output": output[:200] if output else "",
                "output_tokens": len(output.split())
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout - inference took too long",
                "elapsed_seconds": 120
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def run_model_test(self, model_key: str, quick_mode: bool = True) -> Dict:
        """Run complete test for one model"""

        model_config = MODELS[model_key]
        model_name = model_config["name"]

        print(f"\n{'='*70}")
        print(f"Testing: {model_config['alias']}")
        print(f"{'='*70}")
        print(f"  Variant:       {model_config['variant']}")
        print(f"  Quantization:  {model_config['quantization']}")
        print(f"  Expected F1:   {model_config['expected_f1']:.0%}")
        print(f"  Est. VRAM:     {model_config['expected_vram_gb']} GB")

        # Download model
        if not self.download_model(model_name):
            print(f"  ❌ Failed to download model")
            return {"model": model_name, "status": "download_failed"}

        print(f"  ✅ Model ready")

        # Run tests
        results = {
            "model": model_name,
            "alias": model_config["alias"],
            "status": "success",
            "tests": [],
            "summary": {}
        }

        # Use fewer articles in quick mode
        test_articles = self.test_articles[:1] if quick_mode else self.test_articles

        for idx, article in enumerate(test_articles):
            print(f"  Running test {idx+1}/{len(test_articles)}...", end=" ", flush=True)

            test_text = article.get("text", article.get("content", ""))
            test_result = self.test_model(model_name, test_text)

            if test_result.get("success"):
                print(f"✅ ({test_result['elapsed_seconds']:.1f}s)")
            else:
                print(f"❌ ({test_result.get('error', 'Unknown')})")

            results["tests"].append({
                "article_id": article.get("id", f"test_{idx}"),
                **test_result
            })

        # Calculate summary
        successful_tests = [t for t in results["tests"] if t.get("success")]

        if successful_tests:
            avg_time = sum(t["elapsed_seconds"] for t in successful_tests) / len(successful_tests)
            avg_vram = sum(t.get("vram_used_gb", 0) for t in successful_tests) / len(successful_tests)
            avg_tokens_per_sec = sum(
                t.get("output_tokens", 0) / max(t["elapsed_seconds"], 0.1)
                for t in successful_tests
            ) / len(successful_tests)

            results["summary"] = {
                "tests_passed": len(successful_tests),
                "tests_total": len(results["tests"]),
                "avg_inference_time_sec": avg_time,
                "avg_vram_used_gb": avg_vram,
                "avg_tokens_per_sec": avg_tokens_per_sec,
                "vram_safety": self._assess_vram_safety(avg_vram)
            }

            # Print summary
            print(f"\n  📊 Results:")
            print(f"     Avg inference time: {avg_time:.2f}s")
            print(f"     Avg VRAM used:      {avg_vram:.2f} GB")
            print(f"     Tokens/sec:         {avg_tokens_per_sec:.0f}")
            print(f"     VRAM Safety:        {results['summary']['vram_safety']}")

        return results

    def _assess_vram_safety(self, vram_used: float) -> str:
        """Assess if VRAM usage is safe for M4 16GB"""
        if vram_used < 8:
            return "✅ Safe (plenty of headroom)"
        elif vram_used < 10:
            return "✅ Safe (modest headroom)"
        elif vram_used < 12:
            return "⚠️  Caution (tight)"
        else:
            return "❌ Risky (may trigger swap)"

    def run_benchmark_suite(self, mode: str = "quick") -> Dict:
        """Run benchmark across multiple models"""

        print(f"\n{'#'*70}")
        print(f"# GEMMA MODELS BENCHMARK SUITE ({mode.upper()} MODE)")
        print(f"{'#'*70}")
        print(f"Hardware: Apple M4 - 16GB unified memory")
        print(f"Available VRAM: {self.get_system_memory():.1f} GB")
        print(f"Test articles: {len(self.test_articles)}")
        print(f"Timestamp: {datetime.now().isoformat()}")

        # Determine which models to test
        if mode == "quick":
            test_models = ["baseline", "code", "instruct"]
        elif mode == "full":
            test_models = list(MODELS.keys())
        else:
            test_models = ["baseline"]

        results = {
            "timestamp": datetime.now().isoformat(),
            "hardware": "Apple M4 - 16GB",
            "mode": mode,
            "available_vram_gb": self.get_system_memory(),
            "models": []
        }

        for model_key in test_models:
            try:
                result = self.run_model_test(
                    model_key,
                    quick_mode=(mode == "quick")
                )
                results["models"].append(result)
            except KeyboardInterrupt:
                print("\n\n⚠️  Test interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                results["models"].append({
                    "model": model_key,
                    "status": f"error: {str(e)}"
                })

        return results

    def save_results(self, results: Dict, filename: str = "gemma_benchmark.json"):
        """Save results to file"""
        output_file = self.output_dir / filename
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Results saved to: {output_file}")
        return output_file

    def print_summary_table(self, results: Dict):
        """Print results as formatted comparison table"""

        print(f"\n{'='*100}")
        print(f"GEMMA MODELS BENCHMARK RESULTS")
        print(f"{'='*100}")

        # Header
        print(f"{'Model':<35} {'Time (s)':<12} {'VRAM (GB)':<12} {'Tokens/s':<12} {'Safety':<15}")
        print(f"{'-'*100}")

        # Model results
        for model_result in results["models"]:
            name = model_result.get("alias", model_result["model"])[:33]
            summary = model_result.get("summary", {})

            if summary:
                time_s = f"{summary.get('avg_inference_time_sec', 0):.2f}"
                vram_gb = f"{summary.get('avg_vram_used_gb', 0):.1f}"
                tokens_s = f"{summary.get('avg_tokens_per_sec', 0):.0f}"
                safety = summary.get('vram_safety', 'Unknown')
            else:
                time_s = "N/A"
                vram_gb = "N/A"
                tokens_s = "N/A"
                safety = f"⚠️  {model_result.get('status', 'Failed')}"

            print(f"{name:<35} {time_s:<12} {vram_gb:<12} {tokens_s:<12} {safety:<15}")

        print(f"{'='*100}")

        # Recommendations
        print(f"\n📊 RECOMMENDATIONS:")
        successful = [m for m in results["models"] if m.get("summary")]

        if successful:
            # Find best VRAM/performance balance
            best_model = max(
                successful,
                key=lambda m: m.get("summary", {}).get("avg_tokens_per_sec", 0)
            )
            print(f"  🏆 Best performance: {best_model.get('alias', 'N/A')}")

            # Find safest
            safest = min(
                successful,
                key=lambda m: m.get("summary", {}).get("avg_vram_used_gb", 0)
            )
            print(f"  ✅ Safest VRAM: {safest.get('alias', 'N/A')}")


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="Test Gemma model variants for compliance entity extraction"
    )
    parser.add_argument(
        "--mode",
        choices=["quick", "full"],
        default="quick",
        help="Test mode: quick (3 models, 30 min) or full (all models, 2+ hours)"
    )
    parser.add_argument(
        "--model",
        help="Test specific model (e.g., gemma:7b-code)"
    )
    parser.add_argument(
        "--data",
        default="data/kleptotrace.json",
        help="Path to test data file"
    )
    parser.add_argument(
        "--output",
        default="results",
        help="Output directory for results"
    )

    args = parser.parse_args()

    # Check if Ollama is running
    try:
        subprocess.run(["ollama", "list"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Error: Ollama is not running or not installed")
        print("   Start Ollama before running this script")
        sys.exit(1)

    # Run tests
    tester = GemmaModelTester(data_path=args.data, output_dir=args.output)

    if args.model:
        # Test specific model
        results = tester.run_model_test(args.model)
    else:
        # Run full benchmark suite
        results = tester.run_benchmark_suite(mode=args.mode)

    # Save and display results
    output_file = tester.save_results(results)
    tester.print_summary_table(results)

    print(f"\n✅ Testing complete!")
    print(f"   Results saved to: {output_file}")


if __name__ == "__main__":
    main()
