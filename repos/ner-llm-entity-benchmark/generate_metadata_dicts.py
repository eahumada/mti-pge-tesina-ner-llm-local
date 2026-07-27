import json
import os
import random
try:
    from faker import Faker
except ImportError:
    print("Please pip install Faker")
    exit(1)

def generate_augmented_dicts():
    # Locales
    locales = {
        'USA': 'en_US',
        'Brazil': 'pt_BR',
        'Mexico': 'es_MX',
        'Venezuela': 'es_ES', # Fallback for spanish
        'Chile': 'es_CL',
        'China': 'zh_CN',
        'Russia': 'ru_RU',
        'Iran': 'fa_IR'
    }
    
    augmented_persons = []
    
    for country, loc in locales.items():
        print(f"Generating names for {country} ({loc})...")
        try:
            fake = Faker(loc)
        except Exception:
            fake = Faker('en_US') # fallback
            
        # Generate 1500 names per country to ensure total size is well under 10MB
        for _ in range(1500):
            name = fake.name()
            augmented_persons.append({
                "entity": name,
                "metadata": {
                    "source": f"censo_simulado_{country.lower()}",
                    "country_of_origin": country
                }
            })
            
    os.makedirs('data/dictionaries', exist_ok=True)
    out_path = 'data/dictionaries/augmented_persons.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(augmented_persons, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(augmented_persons)} augmented names.")
    print(f"Saved to {out_path} (Size: {os.path.getsize(out_path)/1024:.2f} KB)")

if __name__ == '__main__':
    generate_augmented_dicts()
