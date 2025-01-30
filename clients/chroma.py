from typing import Optional, List

import chromadb
from clients.open_ai import open_ai_client

class ChromaClient:
    def __init__(self, db_path, collection_name):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embed_function = open_ai_client.embedding
    
    def add_document(self, doc_id: str, key_text, value_text: str, metadata: Optional[dict] = None):
        embedding = self.embed_function(key_text)
        self.collection.add(ids=[doc_id], embeddings=[embedding], documents=[value_text], metadatas=[metadata])
    
    def search(self, query: str, n_results: int = 4) -> List[str]:
        query_embedding = self.embed_function(query)
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
        return results["documents"]

    def get(self, doc_id:str):
        return self.collection.get(doc_id)