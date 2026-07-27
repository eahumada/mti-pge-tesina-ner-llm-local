import urllib.request
import csv
import json
import os
import ssl

print("Downloading Fortune 500 Orgs and Popular Names...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    # 1. Fetch Fortune 500 from a public source
    url_orgs = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    req_orgs = urllib.request.Request(url_orgs, headers={'User-Agent': 'Mozilla/5.0'})
    
    orgs = set()
    with urllib.request.urlopen(req_orgs, context=ctx) as response:
        content = response.read().decode('utf-8', errors='ignore')
        reader = csv.reader(content.splitlines())
        next(reader, None)  # skip header
        for row in reader:
            if len(row) > 1:
                orgs.add(row[1].strip())
                
    # 2. Fetch Popular Baby Names from US SSA (public github mirror)
    url_names = "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
    req_names = urllib.request.Request(url_names, headers={'User-Agent': 'Mozilla/5.0'})
    
    persons = set()
    with urllib.request.urlopen(req_names, context=ctx) as response:
        content = response.read().decode('utf-8', errors='ignore')
        reader = csv.reader(content.splitlines())
        next(reader, None)
        count = 0
        for row in reader:
            if len(row) > 1:
                persons.add(row[1].strip())
                count += 1
                if count > 5000: # Limit size to keep it small
                    break

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
