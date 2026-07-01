from __future__ import annotations
import math
import numpy as np
import scipy.stats as stats

def calculate_cohens_kappa(annotator1_labels: list, annotator2_labels: list) -> float:
    """
    Calculates Cohen's Kappa for categorical agreement.
    Supports list of categories/extractions.
    """
    try:
        from sklearn.metrics import cohen_kappa_score
        return float(cohen_kappa_score(annotator1_labels, annotator2_labels))
    except Exception:
        # Simplified manual calculation fallback
        if len(annotator1_labels) != len(annotator2_labels) or len(annotator1_labels) == 0:
            return 0.0
            
        labels = list(set(annotator1_labels + annotator2_labels))
        n = len(annotator1_labels)
        
        # Agreement matrix
        agree = sum(1 for a, b in zip(annotator1_labels, annotator2_labels) if a == b)
        po = agree / n
        
        # Expected agreement pe
        pe = 0.0
        for label in labels:
            p1 = sum(1 for x in annotator1_labels if x == label) / n
            p2 = sum(1 for x in annotator2_labels if x == label) / n
            pe += p1 * p2
            
        if pe >= 1.0:
            return 1.0
        return float((po - pe) / (1.0 - pe))

def run_anova_test(groups: dict[str, list[float]], metric_name: str = "F1-Score") -> dict:
    """Runs a one-way ANOVA test across multiple model result groups."""
    model_names = list(groups.keys())
    arrays = [groups[name] for name in model_names]
    
    # Filter empty groups
    arrays = [arr for arr in arrays if len(arr) > 0]
    if len(arrays) < 2:
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "significant": False,
            "metric": metric_name,
            "num_groups": len(arrays)
        }
        
    try:
        f_stat, p_val = stats.f_oneway(*arrays)
        return {
            "statistic": float(f_stat) if not np.isnan(f_stat) else 0.0,
            "p_value": float(p_val) if not np.isnan(p_val) else 1.0,
            "significant": bool(p_val < 0.05) if not np.isnan(p_val) else False,
            "metric": metric_name,
            "num_groups": len(arrays)
        }
    except Exception as e:
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "significant": False,
            "metric": metric_name,
            "error": str(e),
            "num_groups": len(arrays)
        }

def run_tukey_posthoc(groups: dict[str, list[float]], alpha: float = 0.05) -> list[dict]:
    """
    Performs Tukey HSD pairwise comparisons.
    Falls back to pairwise t-tests with Bonferroni correction if statsmodels is not available.
    """
    model_names = list(groups.keys())
    results = []
    
    # Check if we can use statsmodels HSD
    try:
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        # Flatten data for statsmodels input
        data = []
        labels = []
        for name, vals in groups.items():
            data.extend(vals)
            labels.extend([name] * len(vals))
            
        if len(set(labels)) < 2:
            return []
            
        tukey = pairwise_tukeyhsd(endog=data, groups=labels, alpha=alpha)
        
        # Parse summary table
        # Structure: group1, group2, meandiff, p-adj, lower, upper, reject
        for row in tukey.summary().data[1:]:
            results.append({
                "group1": str(row[0]),
                "group2": str(row[1]),
                "mean_diff": float(row[2]),
                "p_value": float(row[3]),
                "significant": bool(row[6]),
                "ci_lower": float(row[4]),
                "ci_upper": float(row[5])
            })
        return results
    except Exception:
        # Fallback to pairwise t-tests with Bonferroni correction
        pairs = []
        for i in range(len(model_names)):
            for j in range(i + 1, len(model_names)):
                pairs.append((model_names[i], model_names[j]))
                
        num_comparisons = len(pairs)
        if num_comparisons == 0:
            return []
            
        bonferroni_alpha = alpha / num_comparisons
        
        for g1, g2 in pairs:
            v1 = groups[g1]
            v2 = groups[g2]
            
            if len(v1) == 0 or len(v2) == 0:
                continue
                
            try:
                t_stat, p_val = stats.ttest_ind(v1, v2, equal_var=False)
                mean_diff = float(np.mean(v1) - np.mean(v2))
                
                # Standard error of the difference
                se = math.sqrt(np.var(v1)/len(v1) + np.var(v2)/len(v2))
                # Critical value approximation
                crit = 1.96
                
                results.append({
                    "group1": g1,
                    "group2": g2,
                    "mean_diff": mean_diff,
                    "p_value": float(p_val) if not np.isnan(p_val) else 1.0,
                    "significant": bool(p_val < bonferroni_alpha) if not np.isnan(p_val) else False,
                    "ci_lower": mean_diff - (crit * se),
                    "ci_upper": mean_diff + (crit * se)
                })
            except Exception:
                continue
                
        return results

def calculate_confidence_intervals(data: list[float], confidence: float = 0.95) -> dict:
    """Calculates confidence interval for model stats."""
    n = len(data)
    if n == 0:
        return {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "std": 0.0, "n": 0}
        
    mean = float(np.mean(data))
    std = float(np.std(data, ddof=1)) if n > 1 else 0.0
    
    if n > 1:
        se = std / math.sqrt(n)
        h = se * stats.t.ppf((1 + confidence) / 2., n-1)
        ci_lower = mean - h
        ci_upper = mean + h
    else:
        ci_lower = mean
        ci_upper = mean
        
    return {
        "mean": mean,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "std": std,
        "n": n
    }

def run_sensitivity_analysis(all_results: list[dict], data_file: str) -> str:
    """
    Performs sensitivity analysis on model F1 scores by excluding 'difficult' records
    (e.g., extremely long news articles).
    """
    from src.data_loader import load_all_records
    
    records = {r["id"]: r for r in load_all_records(data_file)}
    if not records:
        return "\n## 4. Sensitivity Analysis\nNo source data found to perform sensitivity analysis.\n"
        
    lengths = [len(r.get("caption", "")) for r in records.values()]
    avg_len = sum(lengths) / len(lengths) if lengths else 0
    length_threshold = avg_len + 500
    
    report = ["\n## 4. Sensitivity Analysis (Outlier Filtering)"]
    report.append(f"- **Difficulty Criteria:** Article length > {length_threshold:.1f} characters.")
    
    import pandas as pd
    df = pd.DataFrame(all_results)
    if df.empty:
        return "\n## 4. Sensitivity Analysis\nNo model results to analyze.\n"
        
    def is_difficult(row):
        rid = row["record_id"]
        rec = records.get(rid)
        if not rec:
            return False
        return len(rec.get("caption", "")) > length_threshold
        
    df["difficult"] = df.apply(is_difficult, axis=1)
    num_difficult = df[df["difficult"] == True]["record_id"].nunique() if "difficult" in df.columns else 0
    report.append(f"- **Outlier Records Identified:** {num_difficult} records.")
    
    report.append("\n| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |")
    report.append("| :--- | :---: | :---: | :---: | :---: |")
    
    for model, group in df.groupby("model"):
        standard_f1 = group["f1"].mean()
        cleaned_group = group[group["difficult"] == False] if "difficult" in group.columns else pd.DataFrame()
        cleaned_f1 = cleaned_group["f1"].mean() if not cleaned_group.empty else standard_f1
        delta = cleaned_f1 - standard_f1
        status = "📈 Improved" if delta > 0.0001 else ("📉 Decreased" if delta < -0.0001 else "⚖️ Stable")
        report.append(f"| {model} | {standard_f1:.4f} | {cleaned_f1:.4f} | {delta:+.4f} | {status} |")
        
    return "\n".join(report)

def generate_statistical_report(model_results: dict[str, list[dict]], data_file: str = "data/sample_sanctions.json") -> str:
    """Generates a complete statistical ANOVA + Tukey + Sensitivity markdown report."""
    report = ["# 📈 Statistical Validation Report\n"]
    
    # 1. Setup groups data
    f1_groups = {}
    precision_groups = {}
    recall_groups = {}
    all_flat_results = []
    
    for model, records in model_results.items():
        f1_groups[model] = [r.get("f1", 0.0) for r in records]
        precision_groups[model] = [r.get("precision", 0.0) for r in records]
        recall_groups[model] = [r.get("recall", 0.0) for r in records]
        all_flat_results.extend(records)
        
    # 2. ANOVA on F1-Score
    f1_anova = run_anova_test(f1_groups, "F1-Score")
    
    report.append("## 1. Analysis of Variance (ANOVA) - F1-Score")
    report.append(f"- **F-Statistic:** {f1_anova.get('statistic', 0.0):.4f}")
    report.append(f"- **p-Value:** {f1_anova.get('p_value', 1.0):.4e}")
    
    if f1_anova.get("significant", False):
        report.append("\n> [!IMPORTANT]\n> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.")
    else:
        report.append("\n> [!NOTE]\n> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \\ge 0.05$).")
        
    # 3. Confidence Intervals Table
    report.append("\n## 2. Model Performance Intervals (95% Confidence)")
    report.append("| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |")
    report.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
    
    for model in f1_groups:
        ci = calculate_confidence_intervals(f1_groups[model])
        report.append(f"| {model} | {ci['n']} | {ci['mean']:.4f} | {ci['ci_lower']:.4f} | {ci['ci_upper']:.4f} | {ci['std']:.4f} |")
        
    # 4. Tukey HSD Pairwise comparisons
    report.append("\n## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)")
    tukey_results = run_tukey_posthoc(f1_groups)
    
    if tukey_results:
        report.append("| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |")
        report.append("| :--- | :---: | :---: | :---: | :---: |")
        for row in tukey_results:
            sig_str = "✅ Yes" if row["significant"] else "❌ No"
            report.append(f"| {row['group1']} vs {row['group2']} | {row['mean_diff']:.4f} | {row['p_value']:.4e} | {sig_str} | [{row['ci_lower']:.4f}, {row['ci_upper']:.4f}] |")
    else:
        report.append("No comparisons run (insufficient models or samples).")
        
    # 5. Sensitivity Analysis
    sensitivity_rep = run_sensitivity_analysis(all_flat_results, data_file)
    report.append(sensitivity_rep)
        
    return "\n".join(report)
