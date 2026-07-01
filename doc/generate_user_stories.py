import os

def create_user_histories():
    workspace_root = "/Users/eahumada1/Documents/personal/MTI/taller_de_titulo"
    target_dir = os.path.join(workspace_root, "doc/USER-HISTORIES")
    os.makedirs(target_dir, exist_ok=True)
    
    # Define the sequential user histories
    user_stories = [
        {
            "id": "US01",
            "title": "Dataset Ingestion & Validation",
            "sequence": 1,
            "phase": "Phase 1: Foundation & Data Ingestion",
            "reqs": ["FR1.1", "FR5.1", "FR5.3"],
            "user_story": "As a Compliance System Operator, I want to load news articles from OpenSanctions datasets and validate their schema so that corrupt data does not interrupt the pipeline.",
            "acceptance_criteria": [
                "The system loads JSONL/CSV records matching FollowTheMoney schemas.",
                "Schema validation rejects records missing ID, schema, caption, or properties.",
                "Each record maintains data provenance including timestamp and source ID."
            ],
            "implementation_notes": "Implemented in `src/data_loader.py` with `load_data_batch` and `validate_record_schema`."
        },
        {
            "id": "US02",
            "title": "Ground Truth & Inter-Annotator Agreement",
            "sequence": 2,
            "phase": "Phase 1: Foundation & Data Ingestion",
            "reqs": ["FR1.2", "FR1.3"],
            "user_story": "As an Academic Researcher, I want to manage manually annotated ground-truth datasets and calculate inter-annotator agreement (Cohen's Kappa) so that I can ensure the reliability of the baseline evaluation.",
            "acceptance_criteria": [
                "Support importing IOB/XML annotated compliance ground truth datasets.",
                "Calculate Cohen's Kappa score between two human annotators.",
                "Generate warning if Cohen's Kappa is below 0.75."
            ],
            "implementation_notes": "Implemented in `src/statistics.py` with `calculate_cohens_kappa`."
        },
        {
            "id": "US03",
            "title": "Single-Context RAG & local LLM Runner",
            "sequence": 3,
            "phase": "Phase 2: Core Execution & Prompting",
            "reqs": ["FR2.1", "FR2.2", "FR2.4", "NFR1.1", "NFR1.2", "NFR5.1"],
            "user_story": "As a Privacy Officer, I want to run entity extraction queries locally using open-source weights (Gemma, DeepSeek, LLaMA) with a single news article context so that sensitive compliance data is not leaked to external APIs.",
            "acceptance_criteria": [
                "Execute local inference queries using Ollama API client.",
                "Enforce single-context RAG prompt template to ground model extraction and prevent hallucinations.",
                "Enforce structured JSON output format and parse output with key normalizations."
            ],
            "implementation_notes": "Implemented in `src/llm_runner.py` with `extract_entities_with_ollama` and `parse_llm_response`."
        },
        {
            "id": "US04",
            "title": "VRAM weight management",
            "sequence": 4,
            "phase": "Phase 2: Core Execution & Prompting",
            "reqs": ["NFR3.3", "FR5.2"],
            "user_story": "As a System Engineer, I want the system to actively unload model weights from GPU memory between cycles so that local testing on hardware like Apple M4 does not trigger Out-of-Memory (OOM) crashes.",
            "acceptance_criteria": [
                "Query Ollama API to set model `keep_alive` parameter to 0.",
                "Unload current model weights before loading the next benchmark candidate.",
                "Gracefully sanitize malformed model JSON outputs without crashing execution."
            ],
            "implementation_notes": "Implemented in `src/llm_runner.py` with `manage_model_lifecycle`."
        },
        {
            "id": "US05",
            "title": "Thread-Safe InMemory Queue & Batch Processing",
            "sequence": 5,
            "phase": "Phase 3: Pub/Sub & Queueing",
            "reqs": ["FR1.4", "FR1.5", "NFR4.2"],
            "user_story": "As a Performance Architect, I want the pipeline to process batches via a Publish/Subscribe pattern using a thread-safe task queue so that data ingestion is fully decoupled from LLM execution.",
            "acceptance_criteria": [
                "Decouple batch publisher from subscriber execution node.",
                "Implement a thread-safe InMemoryTaskQueue implementing abstract queue interfaces.",
                "Ensure multiple batches can be scheduled and executed sequentially."
            ],
            "implementation_notes": "Implemented in `src/pub_sub.py` with `InMemoryTaskQueue`."
        },
        {
            "id": "US06",
            "title": "Redis Integration & Crash Resumability",
            "sequence": 6,
            "phase": "Phase 3: Pub/Sub & Queueing",
            "reqs": ["FR1.6", "NFR4.3"],
            "user_story": "As a DevOps Engineer, I want to use a Redis-backed queue and save state checkpoints after every processed batch so that the pipeline can safely resume from crashes without duplicate processing.",
            "acceptance_criteria": [
                "Support RedisTaskQueue connection configuration.",
                "Acknowledge tasks only after successful execution.",
                "Load checkpoint states at launch to skip completed batches when --resume flag is active."
            ],
            "implementation_notes": "Implemented in `src/pub_sub.py` and `src/checkpoint.py`."
        },
        {
            "id": "US07",
            "title": "Fuzzy Entity Matching & Typed Metrics",
            "sequence": 7,
            "phase": "Phase 4: Metrics & Evaluation",
            "reqs": ["FR3.1", "FR3.2", "FR3.3", "RF3.2"],
            "user_story": "As a Data Scientist, I want to calculate Precision, Recall, and F1-Score segmented by entity type using fuzzy string matching so that spelling variations do not artificially lower accuracy scores.",
            "acceptance_criteria": [
                "Utilize Levenshtein fuzzy string matching ratio above 85% to verify extracted names against ground truth.",
                "Report separate Precision, Recall, and F1 metrics for Persons, Organizations, and Locations.",
                "Report macro-averaged overall metric stats."
            ],
            "implementation_notes": "Implemented in `src/evaluator.py` with `evaluate_extraction_by_type`."
        },
        {
            "id": "US08",
            "title": "Hallucination Detection & Confusion Matrix",
            "sequence": 8,
            "phase": "Phase 4: Metrics & Evaluation",
            "reqs": ["FR4.1", "RF3.1"],
            "user_story": "As a Compliance Auditor, I want to compute the hallucination rate and build a multi-type confusion matrix so that I can quantify the risk of models generating false alerts.",
            "acceptance_criteria": [
                "Compare extracted entities against the original source text using a lower fuzzy ratio to identify invented entities.",
                "Calculate overall hallucination rate (hallucinated / total extracted).",
                "Aggregate overall TP, FP, FN elements into a confusion matrix for Persons, Organizations, and Locations."
            ],
            "implementation_notes": "Implemented in `src/evaluator.py` with `calculate_hallucination_rate` and `build_confusion_matrix`."
        },
        {
            "id": "US09",
            "title": "ANOVA & Tukey Post-Hoc Analysis",
            "sequence": 9,
            "phase": "Phase 5: Academic Reporting",
            "reqs": ["FR3.4", "RF3.3"],
            "user_story": "As an Academic Researcher, I want to execute ANOVA significance tests and Tukey HSD post-hoc tests on F1 results so that I can scientifically validate if RAG+LLM outperforms manual baselines.",
            "acceptance_criteria": [
                "Execute one-way ANOVA across different model result groups.",
                "Perform pairwise Tukey HSD post-hoc comparisons to calculate adjusted p-values.",
                "Highlight statistically significant changes ($p < 0.05$)."
            ],
            "implementation_notes": "Implemented in `src/statistics.py` with `run_anova_test` and `run_tukey_posthoc`."
        },
        {
            "id": "US10",
            "title": "Auditable Run Configs & Logs",
            "sequence": 10,
            "phase": "Phase 5: Academic Reporting",
            "reqs": ["NFR5.2", "NFR6.2", "NFR6.1"],
            "user_story": "As a Scientific Reviewer, I want the system to write structured execution logs and store the complete execution configurations so that any benchmark run can be fully reproduced.",
            "acceptance_criteria": [
                "Generate structured logs in results/benchmark.log detailing processing phases.",
                "Save run configuration (seed, temperature, bounds) in results/run_config.json.",
                "Include detailed metadata (timestamp, model version, system prompt hash) on every evaluation record."
            ],
            "implementation_notes": "Implemented in `src/main.py` under `export_results`."
        },
        {
            "id": "US11",
            "title": "Streamlit Interactive Dashboard",
            "sequence": 11,
            "phase": "Phase 6: Stakeholder Visualization",
            "reqs": ["FR4.2", "FR4.3"],
            "user_story": "As a business stakeholder, I want an interactive web dashboard to view top model performance metrics so that I can select the best candidate for deployment.",
            "acceptance_criteria": [
                "Launch a web application using Streamlit.",
                "Display card metrics for best model, F1, precision, and lowest hallucination.",
                "Provide bar charts comparing F1, precision, and recall across evaluated configurations."
            ],
            "implementation_notes": "Implemented in `src/dashboard.py` Tab 1 (Overview) and Tab 2 (Entity Analysis)."
        },
        {
            "id": "US12",
            "title": "Detailed Trace Explorer",
            "sequence": 12,
            "phase": "Phase 6: Stakeholder Visualization",
            "reqs": ["FR4.4", "NFR6.1"],
            "user_story": "As an Analyst, I want to browse individual news articles, extracted entities, and corresponding ground truth side-by-side inside the dashboard so that I can perform qualitative debugging.",
            "acceptance_criteria": [
                "Display a detailed interactive data table containing all processed records.",
                "Provide selectors to filter records by model and entity category.",
                "Plot latency distributions and sum of retry warnings per model."
            ],
            "implementation_notes": "Implemented in `src/dashboard.py` Tab 4 (Detailed Outputs) and Tab 5 (Latency Analysis)."
        }
    ]
    
    for story in user_stories:
        filename = f"{story['id']}.md"
        filepath = os.path.join(target_dir, filename)
        
        # Format requirements links
        req_links = ", ".join([f"[{r}](../REQUERIMENTS/{r}.md)" for r in story["reqs"]])
        acceptance_list = "\n".join([f"- [ ] {ac}" for ac in story["acceptance_criteria"]])
        
        content = f"""# User Story {story['id']}: {story['title']}

## Metadata
- **ID:** {story['id']}
- **Sequence Order:** {story['sequence']}
- **Phase:** {story['phase']}
- **Mapped Requirements:** {req_links}

## User Story
**{story['user_story']}**

## Acceptance Criteria
{acceptance_list}

## Implementation Details
{story['implementation_notes']}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created user history: {filename}")
        
    # Create the README.md index for USER-HISTORIES
    index_path = os.path.join(target_dir, "README.md")
    index_lines = [
        "# User Histories (Chronological Implementation Plan)\n",
        "This directory outlines the chronological sequence of user histories mapped from the software requirements, covering 6 core product phases.\n",
        "| ID | Phase | Feature Title | Mapped Reqs | Link |",
        "| :---: | :--- | :--- | :--- | :--- |"
    ]
    for story in user_stories:
        reqs_str = ", ".join([f"`{r}`" for r in story["reqs"]])
        index_lines.append(f"| {story['id']} | {story['phase']} | {story['title']} | {reqs_str} | [{story['title']}]({story['id']}.md) |")
        
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
    print("Created README.md user histories index.")

if __name__ == "__main__":
    create_user_histories()
