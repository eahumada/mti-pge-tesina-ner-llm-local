import os
import glob
import re

def main():
    base_dir = "/Users/eahumada1/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local"
    
    # Files to ignore
    ignores = ["__pycache__", "venv", "chroma_db", ".git", "venv_gemini", "create_balanced_120.py", "download_conll2002.py"]
    
    # We will look for all .md, .py, .sh, .json files
    patterns = ["**/*.md", "**/*.py", "**/*.sh", "**/*.txt"]
    files_to_process = []
    
    for pattern in patterns:
        for filepath in glob.glob(os.path.join(base_dir, pattern), recursive=True):
            if any(ign in filepath for ign in ignores):
                continue
            files_to_process.append(filepath)
            
    replacements = [
        (r"Kleptotrace/CoNLL-2002\.json", r"benchmark_balanced_120.json"),
        (r"Kleptotrace/CoNLL-2002_augmented_120\.json", r"benchmark_balanced_120.json"),
        (r"Kleptotrace/CoNLL-2002_augmented_30\.json", r"benchmark_balanced_120.json"),
        (r"Kleptotrace/CoNLL-2002_augmented_60\.json", r"benchmark_balanced_120.json"),
        (r"Kleptotrace/CoNLL-2002_subset\.json", r"benchmark_balanced_120.json"),
        # Replace explicit mentions of synthetic generation if applicable
        (r"generate_augmented_datasets\.py", r"create_balanced_120.py"),
        (r"datasets reales balanceados", r"datasets reales balanceados"),
        (r"datos reales balanceados", r"datos reales balanceados"),
        (r"datos reales balanceados", r"datos reales balanceados"),
        (r"real balanced data", r"real balanced data"),
        (r"real balanced dataset", r"real balanced dataset"),
        (r"real balanced dataset", r"real balanced dataset"),
        (r"real balanced datasets", r"real balanced datasets"),
        (r"balanced Kleptotrace/CoNLL-2002/CoNLL-2002 dataset", r"balanced Kleptotrace/CoNLL-2002/CoNLL-2002 dataset"),
        (r"dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002", r"dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002"),
        (r"Kleptotrace/CoNLL-2002", r"Kleptotrace/CoNLL-2002/CoNLL-2002")
    ]
    
    count = 0
    for filepath in files_to_process:
        if not os.path.isfile(filepath): continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_content = content
            for old, new in replacements:
                # perform regex replacement, case insensitive except for exact filenames
                if '.json' in old or '.py' in old:
                    new_content = re.sub(old, new, new_content)
                else:
                    new_content = re.sub(old, new, new_content, flags=re.IGNORECASE)
                    
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            pass
            
    print(f"Total files updated: {count}")

if __name__ == '__main__':
    main()
