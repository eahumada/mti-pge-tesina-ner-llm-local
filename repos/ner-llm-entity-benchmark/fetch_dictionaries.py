import urllib.request
import json
import os

# Create data/dictionaries if it doesn't exist
os.makedirs('data/dictionaries', exist_ok=True)

print("Downloading Spanish names dictionary...")
try:
    # A public list of common Spanish names
    url = "https://raw.githubusercontent.com/jvalhondo/spanish-names-surnames/master/male_names.csv"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    
    names = []
    for line in content.splitlines()[1:1001]: # Take top 1000
        parts = line.split(',')
        if len(parts) > 0 and parts[0].strip():
            names.append(parts[0].strip().title())
            
    # Append to existing
    existing_names = []
    if os.path.exists('data/dictionaries/persons.json'):
        with open('data/dictionaries/persons.json', 'r') as f:
            existing_names = json.load(f)
            
    all_names = list(set(existing_names + names))
    with open('data/dictionaries/persons.json', 'w') as f:
        json.dump(all_names, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_names)} person names.")
except Exception as e:
    print(f"Error fetching names: {e}")

print("Downloading Global Organizations dictionary...")
try:
    # A public list of companies (Nasdaq/NYSE tickers)
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-02-26/small_train.csv"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    
    orgs = []
    # This might not be the best list, let's just generate some standard orgs
    # or fetch a fortune 500 list
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        
    for line in content.splitlines()[1:]: 
        parts = line.split(',')
        if len(parts) > 1 and parts[1].strip():
            # The company name is the second column usually
            name = parts[1].strip().replace('"', '')
            orgs.append(name)
            
    existing_orgs = []
    if os.path.exists('data/dictionaries/organizations.json'):
        with open('data/dictionaries/organizations.json', 'r') as f:
            existing_orgs = json.load(f)
            
    all_orgs = list(set(existing_orgs + orgs))
    with open('data/dictionaries/organizations.json', 'w') as f:
        json.dump(all_orgs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_orgs)} organizations.")
except Exception as e:
    print(f"Error fetching orgs: {e}")
