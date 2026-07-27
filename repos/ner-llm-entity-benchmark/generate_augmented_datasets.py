import json
import random

# Load original 30
with open("data/kleptotrace_augmented_30.json", "r", encoding="utf-8") as f:
    original_data = json.load(f)["dataset"]

templates = [
    "The {agency} fined {org} $50 million following an investigation into systemic anti-money laundering compliance failures overseen by {person}.",
    "{agency} announced sanctions against {person}, a procurement agent operating in Dubai, for illegally shipping components from manufacturers through front companies including {org}.",
    "Assistant Attorney General {person} announced that {org} pleaded guilty in federal court for its role in laundering illicit drug proceeds.",
    "The {agency} expanded restrictive measures against {org}, blacklisting CEO {person} for facilitating exports in violation of embargoes.",
    "{agency} imposed a civil penalty on {org} for violating financial sanctions by maintaining active trade finance accounts for {person}.",
    "Following a financial review by {agency}, regulator {person} signed new AML laws to prevent {org} from handling funds associated with illicit networks.",
    "The {agency} settled bribery charges against {org} for violations involving payments made by regional manager {person} to state officials.",
    "{agency} blocked all assets of {person} for exploiting {org} to launder billions through shell companies.",
    "{agency} ordered {org} to implement stricter transaction monitoring controls following a probe led by regulator {person}.",
    "A court ordered the seizure of funds linked to {person}, which were held at {org} under fake company names, as announced by {agency}.",
    "The {agency} convicted {org} of failing to prevent money laundering by a trafficking ring led by {person}.",
    "The {agency} reached a plea agreement with {org}, where the bank pleaded guilty to processing billions under CFO {person}.",
    "{agency} announced a settlement with {org} for violations of sanctions by failing to verify identities, managed by compliance lead {person}."
]

persons = [
    "Elena Rostova", "Michael Chang", "Carlos Mendoza", "David Sterling", "Yuri Volkov", 
    "Sarah Jenkins", "Ahmed Al-Fayed", "Li Wei", "James O'Connor", "Fatima Hassan",
    "John Doe", "Alice Smith", "Robert Brown", "Mohammed Tariq", "Ivan Smirnov",
    "Luis Garcia", "Anna Kowalska", "Chen Xiaoping", "Raj Patel", "Jane Doe",
    "Alexander Petrov", "Maria Gonzalez", "Kenji Sato", "Olga Ivanova", "Thomas Muller",
    "Isabella Rossi", "Hassan Mustafa", "Wei Chen", "Sophie Martin", "Ali Reza"
]

orgs = [
    "Global Trade Bank", "Vertex Financial", "Oceanic Shipping", "Apex Holdings", 
    "Northern Trust Bank", "Eastern Capital", "Summit Securities", "Meridian Trust",
    "Pacific Standard", "Vanguard Logistics", "First National Trust", "EuroBank Group",
    "Global Dynamics", "Stark Industries", "Wayne Enterprises", "LexCorp",
    "Umbrella Corporation", "Cyberdyne Systems", "Massive Dynamic", "Tyrell Corporation",
    "Weyland-Yutani", "Omni Consumer Products", "InGen", "Buy n Large", "Silph Co."
]

agencies = [
    "Department of Treasury", "Financial Conduct Authority (FCA)", "SEC", "DOJ",
    "European Central Bank", "BaFin", "Interpol", "UN Security Council", "OFAC",
    "Monetary Authority of Singapore (MAS)", "FinCEN", "AUSTRAC", "FINMA",
    "Hong Kong SFC", "Dubai FSA"
]

def generate_record(start_id, count):
    records = []
    used_combos = set()
    for i in range(count):
        while True:
            t = random.choice(templates)
            p = random.choice(persons)
            o = random.choice(orgs)
            a = random.choice(agencies)
            combo = (t, p, o, a)
            if combo not in used_combos:
                used_combos.add(combo)
                break
        
        text = t.format(agency=a, org=o, person=p)
        title = f"{a} AML Case {start_id + i}"
        
        records.append({
            "article_id": str(start_id + i),
            "title": title,
            "text": text,
            "name_entities": [p],
            "organizations": [a, o]
        })
    return records

# Generate 60
data_60 = original_data.copy()
data_60.extend(generate_record(31, 30))
with open("data/kleptotrace_augmented_60.json", "w", encoding="utf-8") as f:
    json.dump({"dataset": data_60}, f, indent=2)

# Generate 120
data_120 = data_60.copy()
data_120.extend(generate_record(61, 60))
with open("data/kleptotrace_augmented_120.json", "w", encoding="utf-8") as f:
    json.dump({"dataset": data_120}, f, indent=2)

print("Created data/kleptotrace_augmented_60.json and data/kleptotrace_augmented_120.json successfully.")
