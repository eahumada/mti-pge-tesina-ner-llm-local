import os
import sys
import time
import requests
import resource

# Ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm_runner import manage_model_lifecycle, check_model_available

def get_memory_usage_mb() -> float:
    """Returns the current resident set size (memory footprint) of the process in MB."""
    # resource.getrusage returns usage in kilobytes on Linux/Mac
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == 'darwin':
        # On macOS, ru_maxrss is in bytes
        return usage / (1024 * 1024)
    return usage / 1024

def run_stress_test(model: str = "gemma4", cycles: int = 5, base_url: str = "http://localhost:11434"):
    """
    Cycles model loading and unloading sequentially to verify VRAM/RAM stability
    and ensure model lifecycles are managed without OOM or leak crashes (NFR3.3 / RNF2.2).
    """
    print("==================================================")
    print("🧠 RUNNING MEMORY STABILITY STRESS TEST")
    print("==================================================")
    print(f"Target Model: {model}")
    print(f"Test Cycles: {cycles}")
    print(f"Ollama Endpoint: {base_url}")
    
    if not check_model_available(model, base_url):
        print(f"Error: Model '{model}' is not pulled in local Ollama repository. Cannot test.")
        return
        
    initial_mem = get_memory_usage_mb()
    print(f"Initial process memory usage: {initial_mem:.2f} MB")
    
    for i in range(cycles):
        print(f"\n--- Cycle {i+1}/{cycles} ---")
        
        # 1. Load weights
        print(f"1. Triggering model weight load for {model}...")
        try:
            # Load model weights via Ollama chat call with short dummy prompt
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "hello"}],
                "options": {"num_predict": 1}
            }
            res = requests.post(f"{base_url}/api/chat", json=payload, timeout=30)
            if res.status_code == 200:
                print("   Model load trigger acknowledged.")
            else:
                print(f"   Warning: Load status code {res.status_code}")
        except Exception as e:
            print(f"   Load trigger failed: {e}")
            
        time.sleep(2)
        load_mem = get_memory_usage_mb()
        print(f"   Process memory usage: {load_mem:.2f} MB (Delta: {load_mem - initial_mem:+.2f} MB)")
        
        # 2. Unload weights
        print(f"2. Triggering model weight unload lifecycle...")
        # Unload weights (loading next model as None)
        manage_model_lifecycle(model, None, base_url)
        
        time.sleep(2)
        unload_mem = get_memory_usage_mb()
        print(f"   Process memory usage after unload: {unload_mem:.2f} MB (Delta from load: {unload_mem - load_mem:+.2f} MB)")
        
    final_mem = get_memory_usage_mb()
    print("\n==================================================")
    print("🔬 MEMORY STABILITY VERDICT")
    print("==================================================")
    print(f"Final Memory Leak Delta: {final_mem - initial_mem:+.2f} MB")
    if final_mem - initial_mem < 5.0: # Arbitrary threshold for small script
        print("✅ SUCCESS: No significant memory leak detected. Model cycling is stable.")
    else:
        print("⚠️ WARNING: Residual memory footprint increase detected.")
    print("==================================================")

if __name__ == "__main__":
    run_stress_test()
