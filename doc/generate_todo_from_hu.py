import os
import re

def compile_todo_from_hu():
    workspace_root = "/Users/eahumada1/Documents/Personal/MTI/taller_de_titulo"
    hu_dir = os.path.join(workspace_root, "doc/USER_HISTORIES")
    todo_path = os.path.join(workspace_root, "doc/TODO/TODO.md")
    
    if not os.path.exists(hu_dir):
        print(f"Error: Directory {hu_dir} does not exist.")
        return
        
    phases = {}
    
    # Read files in sorted order
    files = sorted([f for f in os.listdir(hu_dir) if f.startswith("HU") and f.endswith(".md")], key=lambda x: int(re.search(r"\d+", x).group()))
    
    for filename in files:
        filepath = os.path.join(hu_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        title_match = re.search(r"# Historia de Usuario (HU\d+): (.*)", content)
        phase_match = re.search(r"-\s*\*\*Phase:\*\* (.*)", content)
        reqs_match = re.search(r"-\s*\*\*Mapped Requirements:\*\* (.*)", content)
        
        if not title_match or not phase_match:
            continue
            
        hu_id = title_match.group(1).strip()
        hu_title = title_match.group(2).strip()
        phase = phase_match.group(1).strip()
        
        reqs_str = ""
        if reqs_match:
            # Extract requirement keys (e.g. FR1.1)
            raw_reqs = reqs_match.group(1).strip()
            # Find all keys inside links or raw strings
            req_keys = re.findall(r"\[([A-Z0-9\.\-_]+)\]", raw_reqs)
            if not req_keys:
                req_keys = re.findall(r"\b[A-Z0-9\.\-_]+\b", raw_reqs)
            reqs_str = f" *(Reqs: {', '.join(req_keys)})*" if req_keys else ""
            
        # Parse acceptance criteria section
        ac_section = re.search(r"## Acceptance Criteria\n(.*?)(?=\n##|$)", content, re.DOTALL)
        ac_items = []
        if ac_section:
            ac_content = ac_section.group(1).strip()
            # Match checkboxes
            matches = re.findall(r"-\s*\[([ xX])\]\s*(.*)", ac_content)
            for status, desc in matches:
                checked = "x" if status.lower() == "x" else " "
                ac_items.append(f"- [{checked}] {desc.strip()}")
                
        if phase not in phases:
            phases[phase] = []
            
        phases[phase].append({
            "id": hu_id,
            "title": hu_title,
            "reqs": reqs_str,
            "items": ac_items
        })
        
    # Write the compiled TODO file
    todo_content = []
    todo_content.append("# Comprehensive Project TODO List (User Story Mapped)\n")
    todo_content.append("This document tracks the detailed tasks and acceptance criteria derived from all 18 User Stories, categorized by project phase. Checked items denote completed features.\n")
    
    for phase, stories in phases.items():
        todo_content.append(f"## {phase}")
        for story in stories:
            todo_content.append(f"### {story['id']}: {story['title']}{story['reqs']}")
            for item in story['items']:
                todo_content.append(item)
            todo_content.append("") # Empty line
            
    os.makedirs(os.path.dirname(todo_path), exist_ok=True)
    with open(todo_path, "w", encoding="utf-8") as f:
        f.write("\n".join(todo_content))
        
    print("TODO_GENERATION_FROM_HU_SUCCESS")

if __name__ == "__main__":
    compile_todo_from_hu()
