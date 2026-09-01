import json
import random
import os

random.seed(42)

def main():
    klepto_path = 'data/kleptotrace.json'
    conll_path = 'data/conll2002_es.json'
    output_path = 'data/benchmark_balanced_120.json'
    
    with open(klepto_path, 'r', encoding='utf-8') as f:
        klepto_data = json.load(f)['dataset']
        
    with open(conll_path, 'r', encoding='utf-8') as f:
        conll_data = json.load(f)['dataset']
        
    print(f"Loaded {len(klepto_data)} Kleptotrace items.")
    print(f"Loaded {len(conll_data)} CoNLL-2002 items.")
    
    # Take all Kleptotrace
    selected_klepto = klepto_data
    
    # Calculate how many we need to reach 120
    needed = 120 - len(selected_klepto)
    
    # Sample from CoNLL
    selected_conll = random.sample(conll_data, min(needed, len(conll_data)))
    
    combined = selected_klepto + selected_conll
    random.shuffle(combined)
    
    # Re-assign IDs for sequential cleanliness
    for i, item in enumerate(combined):
        item['article_id'] = f"real_mixed_{i+1}"
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"dataset": combined}, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(combined)} real items to {output_path}")

if __name__ == '__main__':
    main()
