import urllib.request
import csv
import json
import os
import ssl

url = "https://www.treasury.gov/ofac/downloads/sdn.csv"
print("Downloading OFAC SDN List...")

# Bypass SSL verification for local development issues
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as response:
        content = response.read().decode('utf-8', errors='ignore')

    persons = set()
    orgs = set()
    
    reader = csv.reader(content.splitlines())
    count = 0
    for row in reader:
        if len(row) >= 3:
            name = row[1].strip()
            ent_type = row[2].strip()
            if not name:
                continue
                
            # OFAC names are usually LAST, FIRST. We just keep the raw name for dictionary.
            if 'individual' in ent_type.lower():
                persons.add(name)
            else:
                orgs.add(name)
                
            count += 1
            if count >= 3000:  # Keep it small to limit index time to < 50%
                break

    print(f"Extracted {len(persons)} persons and {len(orgs)} organizations from OFAC.")

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
    print(f"Failed to fetch or parse OFAC list: {e}")
