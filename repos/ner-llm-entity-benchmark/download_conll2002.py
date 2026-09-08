import urllib.request
import json
import os
import ssl

def download_and_convert_conll2002():
    url = "https://raw.githubusercontent.com/teropa/nlp/master/resources/corpora/conll2002/esp.train"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    print("Downloading CoNLL-2002 Spanish Training Data...")
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            content = response.read().decode('ISO-8859-1')
    except Exception as e:
        print(f"Error downloading: {e}")
        return

    lines = content.split('\n')
    dataset = []
    
    current_words = []
    current_persons = set()
    current_orgs = set()
    current_locs = set()

    current_entity_words = []
    current_entity_type = None

    article_count = 0

    # Fix 2026-09-08 (encargo §2.bis.2): CoNLL-2002 anota PER, ORG, LOC y MISC. La versión anterior
    # descartaba LOC, lo que dejaba el campo Locations vacío en los 105 artículos de este origen y hacía
    # que toda localización devuelta por el modelo se contara como falso positivo. Ahora se captura LOC.
    def save_entity():
        if current_entity_words:
            entity_name = " ".join(current_entity_words)
            if current_entity_type == "PER":
                current_persons.add(entity_name)
            elif current_entity_type == "ORG":
                current_orgs.add(entity_name)
            elif current_entity_type == "LOC":
                current_locs.add(entity_name)
            current_entity_words.clear()

    # We will group roughly every 10 sentences into a "document" to simulate an article
    sentence_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            sentence_count += 1
            if sentence_count >= 10:  # Create a document every 10 sentences
                if current_words:
                    article_count += 1
                    dataset.append({
                        "article_id": f"conll2002_es_{article_count}",
                        "title": f"Spanish News Snippet {article_count}",
                        "text": " ".join(current_words),
                        "name_entities": list(current_persons),
                        "organizations": list(current_orgs),
                        "locations": list(current_locs)
                    })
                    current_words = []
                    current_persons = set()
                    current_orgs = set()
                    current_locs = set()
                    sentence_count = 0
            continue
            
        parts = line.split()
        if len(parts) >= 3:
            word = parts[0]
            tag = parts[-1]
            
            # Reconstruct text spacing simply
            current_words.append(word)
            
            if tag.startswith("B-"):
                save_entity()
                current_entity_type = tag[2:]
                if current_entity_type in ["PER", "ORG", "LOC"]:
                    current_entity_words.append(word)
            elif tag.startswith("I-"):
                if current_entity_type in ["PER", "ORG", "LOC"]:
                    current_entity_words.append(word)
            else:
                save_entity()
                current_entity_type = None
    
    # Save any remaining
    save_entity()
    if current_words:
        article_count += 1
        dataset.append({
            "article_id": f"conll2002_es_{article_count}",
            "title": f"Spanish News Snippet {article_count}",
            "text": " ".join(current_words),
            "name_entities": list(current_persons),
            "organizations": list(current_orgs),
            "locations": list(current_locs)
        })

    output_path = 'data/conll2002_es.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"dataset": dataset}, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(dataset)} documents to {output_path}")

if __name__ == '__main__':
    download_and_convert_conll2002()
