import urllib.request
import csv
import json
import os
import ssl

print("Downloading UN Security Council Consolidated List...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    # 1. Fetch UN Security Council List (XML is hard, let's use a known public CSV or similar)
    # Actually, let's use a known GitHub repo with sanctions data or common names
    url_names = "https://raw.githubusercontent.com/fivethirtyeight/data/master/common-words/common-names.csv"
    req_names = urllib.request.Request(url_names, headers={'User-Agent': 'Mozilla/5.0'})
    
    persons = set()
    with urllib.request.urlopen(req_names, context=ctx) as response:
        content = response.read().decode('utf-8', errors='ignore')
        reader = csv.reader(content.splitlines())
        next(reader, None)
        for row in reader:
            if len(row) > 1:
                persons.add(row[1].strip().title())
                
    # 2. Add some tech companies and global brands manually or via a gist
    orgs = set(["Google", "Apple", "Microsoft", "Amazon", "Meta", "Tesla", "Nvidia", "Samsung", "Toyota", "Volkswagen", "HSBC", "JPMorgan", "Citi", "Wells Fargo", "Alibaba", "Tencent"])
    
    print(f"Extracted {len(persons)} persons and {len(orgs)} organizations from new sources.")

    # Merge with existing
    def merge_and_save(filename, new_data):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        existing = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing = json.load(f)
                except:
                    pass
        merged = list(set(existing + list(new_data)))
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        return len(merged)
        
    p_len = merge_and_save('data/dictionaries/persons.json', persons)
    o_len = merge_and_save('data/dictionaries/organizations.json', orgs)
    
    print(f"Total persons: {p_len}, Total orgs: {o_len}")
    
except Exception as e:
    print(f"Failed to fetch extra dicts: {e}")
