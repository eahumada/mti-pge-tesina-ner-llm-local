import os
import re

def check_and_create_remaining_stories():
    workspace_root = "/Users/eahumada1/Documents/personal/MTI/taller_de_titulo"
    req_dir = os.path.join(workspace_root, "doc/REQUERIMENTS")
    us_dir = os.path.join(workspace_root, "doc/USER-HISTORIES")
    
    # 1. Read all requirement files to get their IDs and titles
    all_reqs = {}
    if os.path.exists(req_dir):
        for f in os.listdir(req_dir):
            if f.startswith("REQ") and f.endswith(".md"):
                path = os.path.join(req_dir, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                # Find ID and Title from content
                id_match = re.search(r"-\s*\*\*ID:\*\* (.*)", content)
                title_match = re.search(r"-\s*\*\*Title:\*\* (.*)", content)
                desc_match = re.search(r"## Description\n(.*)", content, re.DOTALL)
                
                req_id = id_match.group(1).strip() if id_match else f.replace(".md", "")
                req_title = title_match.group(1).strip() if title_match else "Untitled"
                req_desc = desc_match.group(1).strip() if desc_match else ""
                
                all_reqs[req_id] = {
                    "filename": f,
                    "title": req_title,
                    "desc": req_desc
                }
                
    # 2. Existing user stories definitions from the previous script
    # We will parse the mapped reqs from the current user story files
    mapped_req_ids = set()
    if os.path.exists(us_dir):
        for f in os.listdir(us_dir):
            if f.startswith("US") and f.endswith(".md"):
                path = os.path.join(us_dir, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                # Extract requirement links like: [FR1.1](../REQUERIMENTS/FR1.1.md)
                reqs_found = re.findall(r"\[([A-Z0-9\.\-_]+)\]\(\.\./REQUERIMENTS/", content)
                for r in reqs_found:
                    mapped_req_ids.add(r)
                    
    # Also support mappings that don't match the exact pattern or standard mappings
    # Let's check which requirement keys from all_reqs are not in mapped_req_ids
    unmapped = []
    for req_id in all_reqs:
        # Check direct match or normalized versions
        normalized = req_id.replace("RF", "FR")
        matches = [m for m in mapped_req_ids if m.replace("RF", "FR") == normalized or m == req_id]
        if not matches:
            unmapped.append(req_id)
            
    print(f"Total requirements found: {len(all_reqs)}")
    print(f"Mapped requirement IDs: {len(mapped_req_ids)}")
    print(f"Unmapped requirement IDs: {unmapped}")
    
    # Let's see the details of the unmapped ones
    additional_stories = []
    
    # We will create User Stories for:
    # 1. Cost Efficiency (NFR3.2 / RNF2.2) and Hardware bounds:
    #    Let's make a story: US13: Cost & Resource Optimization (NFR3.2, RNF2.2)
    # 2. Latency limits and Benchmarking speeds:
    #    US14: Performance & Processing Speed Bounds (NFR3.1, RNF2.1)
    # 3. Spanish Language dominance and Regional contexts:
    #    US15: Spanish & Latin American Localization (NFR5.1, RNF5.1)
    # 4. Acceptance Criteria validation checks:
    #    US16: Automated System Acceptance Tests (NFR7.1)
    
    # Let's define the additional user stories
    user_stories_extensions = [
        {
            "id": "US13",
            "title": "Cost & Resource Optimization",
            "sequence": 13,
            "phase": "Phase 2: Core Execution & Prompting",
            "reqs": ["NFR3.2", "RNF2.2"],
            "user_story": "As a CFO, I want the system to be designed to run on standard modern hardware (Apple Silicon/local GPUs) without relying on expensive cloud dependencies so that we can reduce compliance processing costs by 60-80%.",
            "acceptance_criteria": [
                "System executes benchmark sweeps locally on standard VRAM limits (under 16GB).",
                "Verify CPU/GPU utilization logs do not trigger memory leaks or swap crashes.",
                "Calculate and log cost comparison estimation (local vs. external API equivalents)."
            ],
            "implementation_notes": "Enforced by local execution configs in `src/config.py` and dynamic VRAM swaps in `src/llm_runner.py`."
        },
        {
            "id": "US14",
            "title": "Performance & Processing Speed Bounds",
            "sequence": 14,
            "phase": "Phase 3: Pub/Sub & Queueing",
            "reqs": ["NFR3.1", "RNF2.1"],
            "user_story": "As an Operations Manager, I want the batch ingestion and extraction to complete within standard operational timeframes (overnight batching) so that we reduce the news processing turnaround from days to minutes.",
            "acceptance_criteria": [
                "Ingestion and LLM extraction latency is tracked per article in detailed metrics.",
                "Ensure batch sizes are configurable to maximize hardware throughput.",
                "Validate that 100+ articles can be processed sequentially within an overnight window (latency statistics shown in dashboard)."
            ],
            "implementation_notes": "Implemented via latency counters in `src/evaluator.py` and batch iterations in `src/main.py`."
        },
        {
            "id": "US15",
            "title": "Spanish & Latin American Localization",
            "sequence": 15,
            "phase": "Phase 2: Core Execution & Prompting",
            "reqs": ["NFR5.1", "RNF5.1"],
            "user_story": "As a Compliance Analyst in Latin America, I want the NER prompt templates and evaluation metrics to be optimized for Spanish language compliance news so that regional names and regulatory terms are processed accurately.",
            "acceptance_criteria": [
                "Verify prompt templates instruct models to process local Latin American terms (e.g., RUT, fraud contexts).",
                "Evaluate Spanish language context entities correctly without dropping accents or casing.",
                "Support localized metrics reporting."
            ],
            "implementation_notes": "Documented in `doc/REQUERIMENTS/non_functional_requirements.md` and supported by model prompt configuration options."
        },
        {
            "id": "US16",
            "title": "Automated System Acceptance Tests",
            "sequence": 16,
            "phase": "Phase 6: Stakeholder Visualization",
            "reqs": ["NFR7.1"],
            "user_story": "As a Quality Assurance Engineer, I want to automatically verify the system performance against our target acceptance criteria (F1 >= 85%, Hallucinations < 5%) so that I can validate whether a release is production-ready.",
            "acceptance_criteria": [
                "A summary JSON output lists overall F1 and hallucination rates.",
                "The dashboard tab highlights whether target F1-Score of 85% is met.",
                "The dashboard tab flags warning notices if hallucination rate is above 5%."
            ],
            "implementation_notes": "Averaged checks implemented in `src/evaluator.py` and displayed in `src/dashboard.py`."
        }
    ]
    
    # Get all existing stories to recreate the README correctly
    existing_stories = []
    for f in sorted(os.listdir(us_dir)):
        if f.startswith("US") and f.endswith(".md"):
            us_id = f.replace(".md", "")
            if int(us_id[2:]) <= 12: # Old stories
                path = os.path.join(us_dir, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                # Parse title, phase, reqs
                title_match = re.search(r"# User Story US\d+: (.*)", content)
                phase_match = re.search(r"-\s*\*\*Phase:\*\* (.*)", content)
                reqs_match = re.findall(r"\[([A-Z0-9\.\-_]+)\]\(\.\./REQUERIMENTS/", content)
                
                title = title_match.group(1).strip() if title_match else "US"
                phase = phase_match.group(1).strip() if phase_match else "Phase"
                
                existing_stories.append({
                    "id": us_id,
                    "title": title,
                    "sequence": int(us_id[2:]),
                    "phase": phase,
                    "reqs": reqs_match
                })

    # Write additional stories
    for story in user_stories_extensions:
        filename = f"{story['id']}.md"
        filepath = os.path.join(us_dir, filename)
        
        # Link mapped requirements to the REQUERIMENTS files
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
        print(f"Created additional user history: {filename}")
        
        existing_stories.append({
            "id": story["id"],
            "title": story["title"],
            "sequence": story["sequence"],
            "phase": story["phase"],
            "reqs": story["reqs"]
        })

    # Sort all stories sequentially by ID number
    existing_stories.sort(key=lambda s: s["sequence"])
    
    # Rewrite index
    index_path = os.path.join(us_dir, "README.md")
    index_lines = [
        "# User Histories (Chronological Implementation Plan)\n",
        "This directory outlines the chronological sequence of user histories mapped from the software requirements, covering 6 core product phases.\n",
        "| ID | Phase | Feature Title | Mapped Reqs | Link |",
        "| :---: | :--- | :--- | :--- | :--- |"
    ]
    for story in existing_stories:
        reqs_str = ", ".join([f"`{r}`" for r in story["reqs"]])
        index_lines.append(f"| {story['id']} | {story['phase']} | {story['title']} | {reqs_str} | [{story['title']}]({story['id']}.md) |")
        
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
    print("Rewrote README.md user histories index including all 16 user stories.")

if __name__ == "__main__":
    check_and_create_remaining_stories()
