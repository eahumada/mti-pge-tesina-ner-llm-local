import os
import re

def parse_requirements():
    workspace_root = "/Users/eahumada1/Documents/personal/MTI/taller_de_titulo"
    repo_req_dir = os.path.join(workspace_root, "repos/ner-llm-entity-benchmark/doc")
    target_dir = os.path.join(workspace_root, "doc/REQUERIMENTS")
    os.makedirs(target_dir, exist_ok=True)
    
    req_files = [
        os.path.join(repo_req_dir, "REQUERIMENTS/functional_requirements.md"),
        os.path.join(repo_req_dir, "REQUERIMENTS/non_functional_requirements.md"),
        os.path.join(repo_req_dir, "REQUERIMENTS_UPDATED/functional_requirements_enriched.md"),
        os.path.join(repo_req_dir, "REQUERIMENTS_UPDATED/non_functional_requirements_enriched.md")
    ]
    
    all_requirements = []

    # Let's match: - **ID Title:** Description or - **ID:** Description
    # ID is like FR1.1, RF1.1, NFR1.1, etc.
    # Group 1: ID, Group 2: Title, Group 3: Description
    for filepath in req_files:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        category = "Functional" if "functional" in filepath.lower() else "Non-Functional"
        is_enriched = "enriched" in filepath.lower()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # We can split by line or do a global match
        lines = content.split('\n')
        for line in lines:
            line_str = line.strip()
            # Match formats like:
            # - **FR1.1 Dataset Loading:** The system...
            # - **FR1.2 Ground Truth Corpus:** The system...
            # - **NFR1.1 Zero Data Leakage:** Due to...
            # Let's extract ID from the bold section
            if "**" in line_str:
                # Find all between **
                bold_parts = re.findall(r"\*\*(.*?)\*\*", line_str)
                if bold_parts:
                    bold_content = bold_parts[0]
                    # Check if bold content starts with something like FR1.1, RF1.1, NFR1.1
                    id_match = re.match(r"^([A-Z]{2,3}\d+\.\d+)(.*)", bold_content)
                    if id_match:
                        req_id = id_match.group(1).strip()
                        title = id_match.group(2).replace(":", "").strip()
                        if not title:
                            title = "Requirement Details"
                            
                        # Extract description: everything after the bold block (and optional colon)
                        desc_part = line_str.split("**")[-1].strip()
                        if desc_part.startswith(":"):
                            desc_part = desc_part[1:].strip()
                            
                        normalized_id = req_id.replace("RF", "FR")
                        
                        all_requirements.append({
                            "id": req_id,
                            "normalized_id": normalized_id,
                            "title": title,
                            "description": desc_part,
                            "category": category,
                            "source_file": os.path.basename(filepath),
                            "is_enriched": is_enriched
                        })

    # Sort requirements: Functional first, then Non-Functional, sorted by ID numbers
    def sort_key(req):
        cat_order = 0 if req["category"] == "Functional" else 1
        nums = re.findall(r"\d+", req["id"])
        num_tuple = tuple(int(n) for n in nums) if nums else (99, 99)
        return (cat_order, num_tuple, req["id"])
        
    all_requirements.sort(key=sort_key)
    
    # Deduplicate keeping enriched versions
    deduped = []
    seen = set()
    for req in all_requirements:
        norm = req["normalized_id"]
        if norm not in seen:
            seen.add(norm)
            deduped.append(req)
        else:
            # If current is enriched, replace the old one
            idx = next((i for i, r in enumerate(deduped) if r["normalized_id"] == norm), None)
            if idx is not None:
                # If current is enriched, overwrite
                if req["is_enriched"]:
                    deduped[idx] = req
                # If both are enriched or standard, keep the one with longer description
                elif len(req["description"]) > len(deduped[idx]["description"]):
                    deduped[idx] = req

    # Write REQ01.md, REQ02.md...
    for idx, req in enumerate(deduped, start=1):
        filename = f"REQ{idx:02d}.md"
        filepath = os.path.join(target_dir, filename)
        
        content = f"""# Requirement Details: {req['id']}

## Metadata
- **ID:** {req['id']}
- **Category:** {req['category']}
- **Title:** {req['title']}
- **Source File:** {req['source_file']}
- **Enriched:** {'Yes' if req['is_enriched'] else 'No'}

## Description
{req['description']}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Created {filename} -> {req['id']}: {req['title']}")
        
    # Create index
    index_path = os.path.join(target_dir, "README.md")
    index_content = ["# Requirements Index\n", "| Index | ID | Category | Title | File |", "| :--- | :--- | :--- | :--- | :--- |"]
    for idx, req in enumerate(deduped, start=1):
        index_content.append(f"| REQ{idx:02d} | `{req['id']}` | {req['category']} | [{req['title']}](REQ{idx:02d}.md) | {req['source_file']} |")
        
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_content))
    print("Created README.md index file.")

if __name__ == "__main__":
    parse_requirements()
