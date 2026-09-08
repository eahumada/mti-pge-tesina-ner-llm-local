from __future__ import annotations
import json
import os
from pathlib import Path

def download_sample_data(output_path: str = "data/sample_sanctions.json"):
    """
    Ensures the data directory exists. In production, this would load/download
    the OpenSanctions dataset or connect to an upstream repository.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        print(f"Please place your OpenSanctions data at {output_path}")
    return path

import logging

logger = logging.getLogger("ner_benchmark.data_loader")

def validate_record_schema(record: dict) -> bool:
    """
    Validates that the record has the required fields and correct data types
    to prevent pipeline crashes during LLM processing and metrics evaluation (FR5.1).
    """
    if not isinstance(record, dict):
        logger.error("Record is not a dictionary/object.")
        return False
        
    required = ["id", "schema", "caption", "properties"]
    for field in required:
        if field not in record:
            logger.error(f"Record is missing required field: '{field}'")
            return False
            
    # Validate types and values
    if not isinstance(record["id"], (str, int)) or not str(record["id"]).strip():
        logger.error("Record field 'id' must be a non-empty string or integer.")
        return False
        
    if not isinstance(record["schema"], str) or not record["schema"].strip():
        logger.error("Record field 'schema' must be a non-empty string.")
        return False
        
    if not isinstance(record["caption"], str) or not record["caption"].strip():
        logger.error("Record field 'caption' (text) must be a non-empty string.")
        return False
        
    if not isinstance(record["properties"], dict):
        logger.error("Record field 'properties' must be a dictionary.")
        return False
        
    # Validate properties.name structure if present
    if "name" in record["properties"]:
        if not isinstance(record["properties"]["name"], list):
            logger.error("Record properties 'name' field must be a list of strings.")
            return False
            
    # Validate ground_truth if present (e.g. from Kleptotrace/CoNLL-2002/annotated formats)
    if "ground_truth" in record:
        gt = record["ground_truth"]
        if not isinstance(gt, dict):
            logger.error("Record 'ground_truth' must be a dictionary.")
            return False
        for category in ["Persons", "Organizations", "Locations"]:
            if category not in gt:
                logger.error(f"Record 'ground_truth' is missing key: '{category}'")
                return False
            if not isinstance(gt[category], list):
                logger.error(f"Record 'ground_truth[\"{category}\"]' must be a list of strings.")
                return False
                
    return True

def extract_ground_truth(record: dict) -> dict:
    """
    Extracts ground truth entities categorized into Persons, Organizations, and Locations.
    Maps FollowTheMoney schemas:
    - Person -> Persons
    - Company, Organization, LegalEntity, Asset, Bank -> Organizations
    - Address, Country, Location -> Locations
    """
    schema = record.get("schema", "")
    names = record.get("properties", {}).get("name", [])
    
    gt = {"Persons": [], "Organizations": [], "Locations": []}
    
    if not isinstance(names, list):
        names = [names]
        
    for name in names:
        if schema == "Person":
            gt["Persons"].append(name)
        elif schema in ["Company", "Organization", "LegalEntity", "Asset", "Bank", "Vessel"]:
            gt["Organizations"].append(name)
        elif schema in ["Address", "Country", "Location"]:
            gt["Locations"].append(name)
        else:
            # Fallback based on schema keyword matching
            schema_lower = schema.lower()
            if "person" in schema_lower:
                gt["Persons"].append(name)
            elif any(k in schema_lower for k in ["company", "org", "bank", "corp", "firm", "association"]):
                gt["Organizations"].append(name)
            else:
                gt["Locations"].append(name)
                
    return gt

def adapt_kleptotrace_record(record: dict) -> dict:
    """Adapts a Kleptotrace/CoNLL-2002 record to the internal FollowTheMoney schema."""
    return {
        "id": str(record.get("article_id", "")),
        "schema": "Article",
        "caption": record.get("text", ""),
        "properties": {"name": [record.get("title", "")]},
        "ground_truth": {
            "Persons": record.get("name_entities", []),
            "Organizations": record.get("organizations", []),
            # Fix 2026-09-08 (encargo §2.bis.2): antes era la constante [], que borraba las localizaciones
            # anotadas por CoNLL-2002 y convertía en falso positivo toda localización devuelta. Ahora se
            # lee el campo `locations` del registro; queda [] solo si el origen no lo aporta (p. ej. los 15
            # artículos de Kleptotrace, que no anotan localizaciones).
            "Locations": record.get("locations", [])
        }
    }


def parse_iob_ground_truth(content: str) -> list[dict]:
    """
    Parses IOB (Inside-Outside-Beginning) annotated text into standard records.
    Expects token-per-line format with words and tags separated by whitespace.
    Double newlines separate documents.
    """
    documents = []
    current_tokens = []
    current_tags = []
    
    lines = content.split("\n")
    doc_idx = 1
    
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            if current_tokens:
                doc_text, gt = _reconstruct_from_iob(current_tokens, current_tags)
                documents.append({
                    "id": f"iob-{doc_idx}",
                    "schema": "Article",
                    "caption": doc_text,
                    "properties": {"name": [f"IOB Doc {doc_idx}"]},
                    "ground_truth": gt
                })
                doc_idx += 1
                current_tokens = []
                current_tags = []
            continue
            
        parts = line_strip.split()
        if len(parts) >= 2:
            current_tokens.append(parts[0])
            current_tags.append(parts[1])
            
    if current_tokens:
        doc_text, gt = _reconstruct_from_iob(current_tokens, current_tags)
        documents.append({
            "id": f"iob-{doc_idx}",
            "schema": "Article",
            "caption": doc_text,
            "properties": {"name": [f"IOB Doc {doc_idx}"]},
            "ground_truth": gt
        })
        
    return documents

def _reconstruct_from_iob(tokens: list[str], tags: list[str]) -> tuple[str, dict]:
    """Reconstructs text and extracts entities from tokens and IOB tags."""
    text = " ".join(tokens)
    gt = {"Persons": [], "Organizations": [], "Locations": []}
    
    current_entity = []
    current_type = None
    
    for token, tag in zip(tokens, tags):
        if tag.startswith("B-") or tag == "O":
            if current_entity and current_type:
                entity_name = " ".join(current_entity)
                if current_type == "PER":
                    gt["Persons"].append(entity_name)
                elif current_type == "ORG":
                    gt["Organizations"].append(entity_name)
                elif current_type in ["LOC", "GPE"]:
                    gt["Locations"].append(entity_name)
                current_entity = []
                current_type = None
            
            if tag.startswith("B-"):
                current_type = tag.split("-")[1]
                current_entity.append(token)
        elif tag.startswith("I-"):
            entity_type = tag.split("-")[1]
            if current_type == entity_type:
                current_entity.append(token)
                
    if current_entity and current_type:
        entity_name = " ".join(current_entity)
        if current_type == "PER":
            gt["Persons"].append(entity_name)
        elif current_type == "ORG":
            gt["Organizations"].append(entity_name)
        elif current_type in ["LOC", "GPE"]:
            gt["Locations"].append(entity_name)
            
    return text, gt

def parse_xml_ground_truth(content: str) -> list[dict]:
    """
    Parses XML annotated text into standard records.
    Looks for tags like <PER>...</PER>, <ORG>...</ORG>, <LOC>...</LOC>.
    """
    import re
    docs = re.findall(r'<doc[^>]*>(.*?)</doc>', content, re.DOTALL)
    if not docs:
        docs = [content]
        
    documents = []
    for idx, doc_content in enumerate(docs):
        clean_text = re.sub(r'<[^>]+>', ' ', doc_content)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        persons = re.findall(r'<PER>(.*?)</PER>', doc_content)
        orgs = re.findall(r'<ORG>(.*?)</ORG>', doc_content)
        locs = re.findall(r'<LOC>(.*?)</LOC>', doc_content)
        
        documents.append({
            "id": f"xml-{idx+1}",
            "schema": "Article",
            "caption": clean_text,
            "properties": {"name": [f"XML Doc {idx+1}"]},
            "ground_truth": {
                "Persons": [p.strip() for p in persons if p.strip()],
                "Organizations": [o.strip() for o in orgs if o.strip()],
                "Locations": [l.strip() for l in locs if l.strip()]
            }
        })
    return documents

def load_all_records(filepath: str) -> list[dict]:
    """Loads all records from a JSON, XML, IOB, or JSONL file and standardizes them."""
    if not os.path.exists(filepath):
        return []
    
    # Check by file extensions
    ext = os.path.splitext(filepath)[1].lower()
    
    # 0. Parse CSV format
    if ext == ".csv":
        import csv
        records = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader):
                    properties = {"name": [row.get("name", "")]} if "name" in row else {}
                    records.append({
                        "id": row.get("id", f"csv-{idx+1}"),
                        "schema": row.get("schema", "Article"),
                        "caption": row.get("caption", row.get("text", "")),
                        "properties": properties,
                        "ground_truth": {
                            "Persons": [p.strip() for p in row.get("Persons", "").split(",") if p.strip()] if row.get("Persons") else [],
                            "Organizations": [o.strip() for o in row.get("Organizations", "").split(",") if o.strip()] if row.get("Organizations") else [],
                            "Locations": [l.strip() for l in row.get("Locations", "").split(",") if l.strip()] if row.get("Locations") else []
                        }
                    })
            return records
        except Exception as e:
            print(f"Error loading CSV file {filepath}: {e}")
            return []
            
    # Try reading file content
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []

    # 1. Parse XML format
    if ext == ".xml" or (content.strip().startswith("<") and "</doc>" in content):
        return parse_xml_ground_truth(content)
        
    # 2. Parse IOB format
    if ext in [".iob", ".tsv"] or ("O\n" in content or "B-PER" in content):
        # Verify it has columns
        lines = content.strip().split("\n")
        if any(len(l.split()) >= 2 for l in lines[:10] if l.strip()):
            return parse_iob_ground_truth(content)

    # 3. Try reading as standard JSON array first
    try:
        data = json.loads(content)
        # If it's a dict containing a dataset list (e.g. Kleptotrace/CoNLL-2002)
        if isinstance(data, dict) and "dataset" in data:
            records = data["dataset"]
        elif isinstance(data, list):
            records = data
        else:
            records = [data]
        
        # Adapt/standardize if they are Kleptotrace/CoNLL-2002 format
        adapted = []
        for r in records:
            if isinstance(r, dict):
                if "article_id" in r and "text" in r:
                    adapted.append(adapt_kleptotrace_record(r))
                else:
                    adapted.append(r)
        return adapted
    except json.JSONDecodeError:
        # Fall back to JSONL
        pass
        
    records = []
    try:
        for line in content.split("\n"):
            if line.strip():
                try:
                    r = json.loads(line)
                    if isinstance(r, dict):
                        if "article_id" in r and "text" in r:
                            records.append(adapt_kleptotrace_record(r))
                        else:
                            records.append(r)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error parsing JSONL contents: {e}")
        
    return records

def load_data_batch(filepath: str, batch_size: int = 10, offset: int = 0) -> list[dict]:
    """Loads a batch of records starting from offset."""
    records = load_all_records(filepath)
    return records[offset:offset + batch_size]

class DatasetIterator:
    """Iterates through batches of a JSON, XML, IOB, or JSONL file to manage parsing and resumability."""
    def __init__(self, filepath: str, batch_size: int = 10):
        self.filepath = filepath
        self.batch_size = batch_size
        self.records = load_all_records(filepath)
        self.total_records = len(self.records)
            
    def get_batch(self, batch_idx: int) -> list[dict]:
        offset = batch_idx * self.batch_size
        return self.records[offset:offset + self.batch_size]
        
    @property
    def total_batches(self) -> int:
        if self.total_records == 0:
            return 0
        return (self.total_records + self.batch_size - 1) // self.batch_size

def create_sample_dataset(output_path: str, num_records: int = 20):
    """Generates a realistic sample dataset in FollowTheMoney JSONL format."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    samples = [
        {
            "id": "san-01",
            "schema": "Person",
            "caption": "Vladimir Petrov, a prominent financier, was sanctioned by the EU for money laundering.",
            "properties": {"name": ["Vladimir Petrov"]}
        },
        {
            "id": "san-02",
            "schema": "Company",
            "caption": "Alpha Holdings Corp in London has been blacklisted due to ties with prohibited weapon trade.",
            "properties": {"name": ["Alpha Holdings Corp"]}
        },
        {
            "id": "san-03",
            "schema": "Location",
            "caption": "New investigations focus on offshore accounts in Cayman Islands that funneled PEP wealth.",
            "properties": {"name": ["Cayman Islands"]}
        },
        {
            "id": "san-04",
            "schema": "Person",
            "caption": "Maria Lopez, director of Zenith Bank, is currently under house arrest in Madrid.",
            "properties": {"name": ["Maria Lopez"]}
        },
        {
            "id": "san-05",
            "schema": "Company",
            "caption": "Vortex International received severe sanctions from the OFAC department.",
            "properties": {"name": ["Vortex International"]}
        },
        {
            "id": "san-06",
            "schema": "Location",
            "caption": "Assets belonging to illegal smuggling cartels were seized in Switzerland.",
            "properties": {"name": ["Switzerland"]}
        },
        {
            "id": "san-07",
            "schema": "Person",
            "caption": "The prosecutor named Zhang Wei as the mastermind behind the cyber espionage operation.",
            "properties": {"name": ["Zhang Wei"]}
        },
        {
            "id": "san-08",
            "schema": "Company",
            "caption": "SinoTech Industries is accused of violating dual-use technology export bans.",
            "properties": {"name": ["SinoTech Industries"]}
        },
        {
            "id": "san-09",
            "schema": "Location",
            "caption": "Illicit gold transfers were traced back to refineries in Venezuela.",
            "properties": {"name": ["Venezuela"]}
        },
        {
            "id": "san-10",
            "schema": "Person",
            "caption": "Ali Al-Mansoor was added to the UN security council sanctions list this morning.",
            "properties": {"name": ["Ali Al-Mansoor"]}
        },
        {
            "id": "san-11",
            "schema": "Company",
            "caption": "Consulting group Orion Group Ltd was banned from operating in the US.",
            "properties": {"name": ["Orion Group Ltd"]}
        },
        {
            "id": "san-12",
            "schema": "Location",
            "caption": "Suspicious transactions were reported between shell companies registered in Panama.",
            "properties": {"name": ["Panama"]}
        },
        {
            "id": "san-13",
            "schema": "Person",
            "caption": "Hans Gruber, former intelligence analyst, is wanted for cyber fraud in Berlin.",
            "properties": {"name": ["Hans Gruber"]}
        },
        {
            "id": "san-14",
            "schema": "Company",
            "caption": "Global Maritime Logistics was penalized for docking blocked vessels.",
            "properties": {"name": ["Global Maritime Logistics"]}
        },
        {
            "id": "san-15",
            "schema": "Location",
            "caption": "The central government frozen operations in Cyprus after a AML investigation.",
            "properties": {"name": ["Cyprus"]}
        },
        {
            "id": "san-16",
            "schema": "Person",
            "caption": "Elena Rostova faced assets freezing charges initiated by the UK government.",
            "properties": {"name": ["Elena Rostova"]}
        },
        {
            "id": "san-17",
            "schema": "Company",
            "caption": "Nouveau Softwares was sanctioned by OFAC for doing business with blocked governments.",
            "properties": {"name": ["Nouveau Softwares"]}
        },
        {
            "id": "san-18",
            "schema": "Location",
            "caption": "A high-profile money laundering hub was raided in Singapore last night.",
            "properties": {"name": ["Singapore"]}
        },
        {
            "id": "san-19",
            "schema": "Person",
            "caption": "Kenji Sato was indicted by the Tokyo district court for illegal crypto wash-trading.",
            "properties": {"name": ["Kenji Sato"]}
        },
        {
            "id": "san-20",
            "schema": "Company",
            "caption": "Apex Petrochemicals was caught routing oil sales through hidden entities.",
            "properties": {"name": ["Apex Petrochemicals"]}
        }
    ]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for r in samples[:num_records]:
            # Add ground_truth mapping explicitly for easy validation during pipeline
            r["ground_truth"] = extract_ground_truth(r)
            f.write(json.dumps(r) + "\n")
