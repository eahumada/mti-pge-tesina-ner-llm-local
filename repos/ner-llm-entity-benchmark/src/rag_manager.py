import os
import json
import logging
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class RAGManager:
    def __init__(self, db_path="data/chroma_db"):
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)
        # Use PersistentClient directly
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection_name = "ner_dictionaries"
        
        # Load or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def load_dictionaries(self, dictionaries_dir="data/dictionaries"):
        """Loads dictionaries if they are not already present."""
        try:
            count = self.collection.count()
            if count > 0:
                logger.info(f"[RAG] Vector DB already populated with {count} entities. Skipping load.")
                return
            
            logger.info("[RAG] Populating Vector DB with dictionaries...")
            documents = []
            metadatas = []
            ids = []
            
            # Load persons
            persons_file = os.path.join(dictionaries_dir, "persons.json")
            if os.path.exists(persons_file):
                with open(persons_file, 'r', encoding='utf-8') as f:
                    persons = json.load(f)
                    for i, p in enumerate(persons):
                        documents.append(p)
                        metadatas.append({"type": "Person", "source": "dictionary"})
                        ids.append(f"person_{i}")
                        
            # Load organizations
            orgs_file = os.path.join(dictionaries_dir, "organizations.json")
            if os.path.exists(orgs_file):
                with open(orgs_file, 'r', encoding='utf-8') as f:
                    orgs = json.load(f)
                    for i, org in enumerate(orgs):
                        documents.append(org)
                        metadatas.append({"type": "Organization", "source": "dictionary"})
                        ids.append(f"org_{i}")
                        
            # Load augmented persons
            aug_file = os.path.join(dictionaries_dir, "augmented_persons.json")
            if os.path.exists(aug_file):
                with open(aug_file, 'r', encoding='utf-8') as f:
                    aug_persons = json.load(f)
                    for i, item in enumerate(aug_persons):
                        documents.append(item["entity"])
                        meta = {"type": "Person"}
                        if "metadata" in item:
                            meta.update(item["metadata"])
                        metadatas.append(meta)
                        ids.append(f"aug_person_{i}")
            
            if documents:
                # Add in batches to avoid ChromaDB limits
                batch_size = 5000
                for i in range(0, len(documents), batch_size):
                    self.collection.add(
                        documents=documents[i:i+batch_size],
                        metadatas=metadatas[i:i+batch_size],
                        ids=ids[i:i+batch_size]
                    )
                logger.info(f"[RAG] Successfully loaded {len(documents)} entities into Vector DB.")
            else:
                logger.warning("[RAG] No dictionaries found to load.")
                
        except Exception as e:
            logger.error(f"[RAG] Failed to load dictionaries: {e}")

    def query(self, query_texts, n_results=5):
        """Query the vector database for related entities."""
        try:
            if not query_texts:
                return []
                
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results
            )
            
            retrieved_entities = []
            if results and 'documents' in results and results['documents']:
                for docs, metas in zip(results['documents'], results['metadatas']):
                    for doc, meta in zip(docs, metas):
                        entity_type = meta.get("type", "Unknown")
                        retrieved_entities.append(f"{doc} ({entity_type})")
            
            # Return unique entries
            return list(set(retrieved_entities))
        except Exception as e:
            logger.error(f"[RAG] Query failed: {e}")
            return []
