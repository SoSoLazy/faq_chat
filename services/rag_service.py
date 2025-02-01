from tqdm import tqdm
import pandas as pd

from clients.chroma import ChromaClient

DB_PATH = "chroma.db"
COLLECTION_NAME = "faq_rag"
FILE_PATH="data/final_result.csv"

class RagService:
    """
    chroma client와 연계하여 아래의 동작을 진행합니다.
    RAG DB 구축
    RAG 검색기능 제공
    """
    
    _instance = None

    def __init__(self, db_path, collection_name):
        self.chroma_client = ChromaClient(db_path, collection_name)
        self.file_path = FILE_PATH

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RagService(DB_PATH, COLLECTION_NAME)
            cls._instance.set_data()
        return cls._instance
    
    def set_data(self):
        df = pd.read_csv(self.file_path)

        for idx, row in tqdm(df.iterrows()):
            if self.chroma_client.get(f"rag_doc_{idx}")["ids"]:
                continue
            
            row_dict = row.to_dict()
            
            self.chroma_client.add_document(
                doc_id = f"rag_doc_{idx}",
                key_text=row_dict["question"],
                value_text = f'질문: {row_dict["question"]}\n응답: {row_dict["answer"]}'
            )

    def search(self, message):
        return self.chroma_client.search(message)

    def preprocessing(self):
        """
        데이터 전처리 클래스
        """

        pass