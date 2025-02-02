from tqdm import tqdm
import pandas as pd
import pickle

from clients.chroma import ChromaClient
from config import RAG_DATA_FILE_PATH, RAG_DB_PATH, RAG_COLLECTION_NAME

class RagService:
    """
    chroma client와 연계하여 아래의 동작을 진행합니다.
    RAG DB 구축
    RAG 검색기능 제공
    """
    
    _instance = None

    def __init__(self, db_path, collection_name):
        self.chroma_client = ChromaClient(db_path, collection_name)
        self.rag_data_file_path = RAG_DATA_FILE_PATH

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RagService(RAG_DB_PATH, RAG_COLLECTION_NAME)
        return cls._instance
    
    def preprocessing(self) -> pd.DataFrame:
        """
        데이터 전처리 클래스
        """

        data = pickle.load(open(self.rag_data_file_path, 'rb'))
        df = pd.DataFrame(data.items(), columns=['question', 'answer'])
        
        preprocessed_answer_list = []
        additional_request_list = []
        for ans in df['answer'].values:
            preprocessed_answer_list.append(ans.split("위 도움말이 도움이 되었나요?")[0].strip())

        
            additional_request_list.append(
                ans.split("관련 도움말/키워드")[-1].replace("도움말 닫기", "").strip()
                if "관련 도움말/키워드" in ans
                else ""
            )

        df['preprocessed_answer'] = preprocessed_answer_list
        df['additional_request'] = additional_request_list
        return df

    def set_data(self):
        df = self.preprocessing()

        for idx, row in tqdm(df.iterrows()):
            if self.chroma_client.get(f"rag_doc_{idx}")["ids"]:
                continue
            
            row_dict = row.to_dict()

            value_text = f'질문: {row_dict["question"]}\n응답: {row_dict["preprocessed_answer"]}'
            if row_dict["additional_request"]:
                value_text += f"\n추가적인 질문: {row_dict['additional_request']}"

            self.chroma_client.add_document(
                doc_id = f"rag_doc_{idx}",
                key_text=row_dict["question"],
                value_text = value_text
            )

    def search(self, message):
        return self.chroma_client.search(message)