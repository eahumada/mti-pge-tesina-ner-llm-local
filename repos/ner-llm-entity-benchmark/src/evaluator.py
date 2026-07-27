from __future__ import annotations
import re
from rapidfuzz import fuzz
import json
import os

# Global cache for dictionaries to avoid loading them repeatedly
_GLOBAL_DICTIONARIES = None

def _get_dictionaries() -> set:
    global _GLOBAL_DICTIONARIES
    if _GLOBAL_DICTIONARIES is not None:
        return _GLOBAL_DICTIONARIES
        
    _GLOBAL_DICTIONARIES = set()
    for file_name in ["persons.json", "organizations.json"]:
        path = os.path.join("data", "dictionaries", file_name)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        _GLOBAL_DICTIONARIES.add(item.lower().strip())
            except:
                pass
    return _GLOBAL_DICTIONARIES


def calculate_fuzzy_match(extracted_entity: str, ground_truth_entities: list[str], threshold: int = 85) -> bool:
    """Checks if extracted entity matches ground truth list based on fuzzy ratio."""
    if not extracted_entity or not isinstance(extracted_entity, str):
        return False
        
    for gt_entity in ground_truth_entities:
        score = fuzz.ratio(extracted_entity.lower(), gt_entity.lower())
        if score >= threshold:
            return True
    return False

def evaluate_extraction_by_type(extracted: dict, ground_truth: dict, threshold: int = 85) -> dict:
    """
    Computes per-type metrics and macro-averaged metrics.
    Inputs are dicts with keys 'Persons', 'Organizations', 'Locations'.
    """
    types = ["Persons", "Organizations", "Locations"]
    result = {"per_type": {}, "overall": {}}
    
    overall_tp = 0
    overall_fp = 0
    overall_fn = 0
    
    oov_tp = 0
    oov_gt_total = 0
    
    dict_cache = _get_dictionaries()
    
    for t in types:
        ext_list = extracted.get(t, [])
        gt_list = ground_truth.get(t, [])
        
        tp = 0
        fp = 0
        fn = 0
        matched_gts = set()
        
        if not ext_list and not gt_list:
            # Empty list matches
            precision = 1.0
            recall = 1.0
            f1 = 1.0
        elif not ext_list:
            precision = 0.0
            recall = 0.0
            f1 = 0.0
            fn = len(gt_list)
        elif not gt_list:
            # LLM extracted entities but no GT exists → all are hallucinations
            precision = 0.0
            recall = 0.0  # Undefined; 0.0 by convention (no GT → cannot satisfy any recall)
            f1 = 0.0
            fp = len(ext_list)
        else:
            # Standard TP count using fuzzy match
            for entity in ext_list:
                matched = False
                for gt in gt_list:
                    if fuzz.ratio(entity.lower(), gt.lower()) >= threshold:
                        tp += 1
                        matched = True
                        matched_gts.add(gt)
                        break
                if not matched:
                    fp += 1
            fn = len(gt_list) - len(matched_gts)
            
            precision = tp / len(ext_list) if len(ext_list) > 0 else 0.0
            recall = tp / len(gt_list) if len(gt_list) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
        result["per_type"][t] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": tp,
            "fp": fp,
            "fn": fn
        }
        
        # Calculate OOV metrics for this type
        for gt in gt_list:
            is_oov = True
            for d_item in dict_cache:
                if fuzz.ratio(gt.lower(), d_item) >= threshold:
                    is_oov = False
                    break
            if is_oov:
                oov_gt_total += 1
                if gt in matched_gts:
                    oov_tp += 1
        
        overall_tp += tp
        overall_fp += fp
        overall_fn += fn
        
    # Micro/macro metrics calculation
    overall_precision = overall_tp / (overall_tp + overall_fp) if (overall_tp + overall_fp) > 0 else 1.0
    overall_recall = overall_tp / (overall_tp + overall_fn) if (overall_tp + overall_fn) > 0 else 1.0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 1.0
    
    # If there were no entities anywhere, defaults to 1.0
    if overall_tp == 0 and overall_fp == 0 and overall_fn == 0:
        overall_precision = 1.0
        overall_recall = 1.0
        overall_f1 = 1.0
        
    result["overall"] = {
        "precision": overall_precision,
        "recall": overall_recall,
        "f1": overall_f1,
        "tp": overall_tp,
        "fp": overall_fp,
        "fn": overall_fn,
        "oov_recall": (oov_tp / oov_gt_total) if oov_gt_total > 0 else 1.0
    }
    
    return result

def calculate_hallucination_rate(extracted_entities: dict, source_text: str, threshold: int = 70) -> dict:
    """
    Checks if extracted entities exist in the original text (via partial match).
    Calculates Hallucination Rate = Count of Hallucinations / Total Extracted Entities.
    """
    hallucinated = []
    total_count = 0
    hallucinated_count = 0
    
    text_clean = re.sub(r'\s+', ' ', source_text.lower())
    
    for t, entities in extracted_entities.items():
        for entity in entities:
            total_count += 1
            ent_lower = entity.lower()
            
            # Direct match check
            if ent_lower in text_clean:
                continue
                
            # Fuzzy substring match check
            # Find the best match score among sliding windows or check sub-tokens
            words = text_clean.split()
            ent_words_len = len(ent_lower.split())
            best_score = 0
            
            # Sliding window of similar length in source text
            if len(words) >= ent_words_len:
                for idx in range(len(words) - ent_words_len + 1):
                    window = " ".join(words[idx : idx + ent_words_len])
                    score = fuzz.ratio(ent_lower, window)
                    if score > best_score:
                        best_score = score
                        
            if best_score < threshold:
                hallucinated_count += 1
                hallucinated.append(entity)
                
    rate = (hallucinated_count / total_count) if total_count > 0 else 0.0
    
    return {
        "hallucination_rate": rate,
        "hallucinated_entities": hallucinated,
        "total_extracted": total_count,
        "hallucinated_count": hallucinated_count
    }

def calculate_fine_grained_errors(extracted: dict, ground_truth: dict, source_text: str, threshold: int = 85) -> dict:
    """
    Categorizes extraction failures into boundary mismatches, category type confusion,
    and abbreviation omissions to provide deep qualitative failure analysis (REQ40 / HU19).
    """
    errors = {
        "boundary_errors": [],
        "type_confusion": [],
        "abbreviation_misses": [],
        "extrinsic_hallucinations": []
    }
    
    types = ["Persons", "Organizations", "Locations"]
    
    # 1. Type Confusion & Boundary Errors Check
    for t in types:
        ext_list = extracted.get(t, [])
        for entity in ext_list:
            ent_lower = entity.lower()
            
            # Check if this exact entity was placed in a DIFFERENT category in Ground Truth
            found_confusion = False
            for other_t in types:
                if other_t == t:
                    continue
                gt_list_other = ground_truth.get(other_t, [])
                for gt in gt_list_other:
                    if fuzz.ratio(ent_lower, gt.lower()) >= threshold:
                        errors["type_confusion"].append({
                            "entity": entity,
                            "extracted_type": t,
                            "correct_type": other_t,
                            "matched_ground_truth": gt
                        })
                        found_confusion = True
                        break
                if found_confusion:
                    break
            
            if found_confusion:
                continue
                
            # Boundary Error check: Levenshtein ratio is between 50% and 85% with some ground truth entity
            gt_list_same = ground_truth.get(t, [])
            for gt in gt_list_same:
                ratio = fuzz.ratio(ent_lower, gt.lower())
                if 50 <= ratio < threshold:
                    errors["boundary_errors"].append({
                        "entity": entity,
                        "ground_truth_target": gt,
                        "ratio": ratio
                    })
                    break
                    
    # 2. Abbreviation Misses Check:
    # Ground truth entities with length <= 5 that are not extracted in any category
    all_extracted_flat = [e.lower() for cat in types for e in extracted.get(cat, [])]
    for t in types:
        gt_list = ground_truth.get(t, [])
        for gt in gt_list:
            if len(gt) <= 5 and gt.lower() not in all_extracted_flat:
                # Check if it was missed completely (no fuzzy match >= threshold)
                was_extracted = False
                for ext in all_extracted_flat:
                    if fuzz.ratio(gt.lower(), ext) >= threshold:
                        was_extracted = True
                        break
                if not was_extracted:
                    errors["abbreviation_misses"].append({
                        "ground_truth_entity": gt,
                        "category": t
                    })
                    
    # 3. Extrinsic Hallucinations Check:
    # Extracted entities that have very low substring score with the source text (fuzz < 50%)
    text_clean = re.sub(r'\s+', ' ', source_text.lower())
    for t in types:
        ext_list = extracted.get(t, [])
        for entity in ext_list:
            ent_lower = entity.lower()
            if ent_lower not in text_clean:
                # Calculate best sliding window match
                words = text_clean.split()
                ent_words_len = len(ent_lower.split())
                best_score = 0
                if len(words) >= ent_words_len:
                    for idx in range(len(words) - ent_words_len + 1):
                        window = " ".join(words[idx : idx + ent_words_len])
                        score = fuzz.ratio(ent_lower, window)
                        if score > best_score:
                            best_score = score
                if best_score < 50:
                    errors["extrinsic_hallucinations"].append({
                        "entity": entity,
                        "category": t,
                        "text_match_ratio": best_score
                    })
                    
    return errors

def evaluate_single_record(extracted: dict, ground_truth: dict, source_text: str, threshold: int = 85) -> dict:
    """Runs all evaluation metrics on a single record extraction trace."""
    extraction_results = evaluate_extraction_by_type(extracted, ground_truth, threshold)
    hallucination_results = calculate_hallucination_rate(extracted, source_text)
    error_taxonomy = calculate_fine_grained_errors(extracted, ground_truth, source_text, threshold)
    
    return {
        "metrics": extraction_results,
        "hallucination": hallucination_results,
        "error_taxonomy": error_taxonomy
    }

def build_confusion_matrix(all_results: list[dict]) -> dict:
    """Aggregates confusion matrix parameters segmented by entity type."""
    matrix = {
        "Persons": {"TP": 0, "FP": 0, "FN": 0},
        "Organizations": {"TP": 0, "FP": 0, "FN": 0},
        "Locations": {"TP": 0, "FP": 0, "FN": 0}
    }
    
    for record in all_results:
        # Check if record has typed metrics
        metrics = record.get("metrics", {}).get("per_type", {})
        for t in matrix:
            t_metrics = metrics.get(t, {})
            matrix[t]["TP"] += t_metrics.get("tp", 0)
            matrix[t]["FP"] += t_metrics.get("fp", 0)
            matrix[t]["FN"] += t_metrics.get("fn", 0)
            
    return matrix

def aggregate_model_results(results: list[dict]) -> dict:
    """Aggregates and averages metric statistics per model, including system telemetry and throughput."""
    import pandas as pd
    if not results:
        return {}
        
    df = pd.DataFrame(results)
    summary = {}
    
    for model, group in df.groupby("model"):
        tokens_per_sec = float(group["tokens_per_sec"].mean()) if "tokens_per_sec" in group.columns else 0.0
        
        # Calculate wall time (total execution time) for this model
        total_time_sec = 0.0
        if "latency_sec" in group.columns:
            total_time_sec = float(group["latency_sec"].sum())

        # Average system resource metrics
        cpu_avg = float(group["cpu_avg_pct"].mean()) if "cpu_avg_pct" in group.columns else 0.0
        cpu_peak = float(group["cpu_peak_pct"].max()) if "cpu_peak_pct" in group.columns else 0.0
        proc_cpu_avg = float(group["proc_cpu_avg_pct"].mean()) if "proc_cpu_avg_pct" in group.columns else 0.0
        mem_avg = float(group["mem_avg_mb"].mean()) if "mem_avg_mb" in group.columns else 0.0
        mem_peak = float(group["mem_peak_mb"].max()) if "mem_peak_mb" in group.columns else 0.0
        vram_mb = float(group["vram_mb"].mean()) if "vram_mb" in group.columns else 0.0
        model_disk_mb = float(group["model_disk_mb"].max()) if "model_disk_mb" in group.columns else 0.0
        
        # Throughput (Transactions / Requests per second)
        num_records = len(group)
        throughput_req_per_sec = float(num_records / total_time_sec) if total_time_sec > 0 else 0.0

        summary[model] = {
            "f1": float(group["f1"].mean()),
            "precision": float(group["precision"].mean()),
            "recall": float(group["recall"].mean()),
            "hallucination_rate": float(group["hallucination_rate"].mean()),
            "oov_recall": float(group["oov_recall"].mean()) if "oov_recall" in group.columns else 0.0,
            "latency_sec": float(group["latency_sec"].mean()),
            "tokens_per_sec": tokens_per_sec,
            "total_records": int(num_records),
            # Telemetry metrics added
            "total_execution_time_sec": round(total_time_sec, 2),
            "cpu_avg_pct": round(cpu_avg, 2),
            "cpu_peak_pct": round(cpu_peak, 2),
            "proc_cpu_avg_pct": round(proc_cpu_avg, 2),
            "mem_avg_mb": round(mem_avg, 2),
            "mem_peak_mb": round(mem_peak, 2),
            "vram_mb": round(vram_mb, 2),
            "model_disk_mb": round(model_disk_mb, 2),
            "throughput_req_per_sec": round(throughput_req_per_sec, 4)
        }
    return summary
