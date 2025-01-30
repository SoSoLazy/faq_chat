from tqdm import tqdm
import pandas as pd

from clients.chroma import ChromaClient

DB_PATH = "chroma.db"
COLLECTION_NAME = "faq_rag"

class RagService:
    """
    chroma client와 연계하여 아래의 동작을 진행합니다.
    RAG DB 구축
    RAG 검색기능 제공
    """
    
    def __init__(self, db_path, collection_name):
        self.chroma_client = ChromaClient(db_path, collection_name)
    
    def set_data(self, file_path="data/final_result.csv"):
        df = pd.read_csv(file_path)

        for idx, row in tqdm(df.iterrows()):
            if self.chroma_client.get(f"rag_doc_{idx}")["ids"]:
                continue
            
            row_dict = row.to_dict()
            
            self.chroma_client.add_document(
                doc_id = f"rag_doc_{idx}",
                key_text=row_dict["question"],
                value_text = f'Q: {row_dict["question"]}\nA: {row_dict["answer"]}'
            )

    def search(self, message):
        return self.chroma_client.search(message)

rag_service = RagService(DB_PATH, COLLECTION_NAME)
rag_service.set_data()
