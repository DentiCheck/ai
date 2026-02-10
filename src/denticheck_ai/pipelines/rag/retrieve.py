"""
[파일 역할]
RAG (Retrieval-Augmented Generation) 파이프라인의 핵심인 '문서 검색' 모듈입니다.
사용자의 질문과 관련된 치과 의학 지식을 Vector DB (Milvus)에서 찾아오는 역할을 합니다.

[실행 방법]
단독 실행하여 검색 성능을 테스트할 수 있습니다.
$ export PYTHONPATH=$PYTHONPATH:.
$ python3 src/denticheck_ai/pipelines/rag/retrieve.py

[동작 순서]
1. 사전에 `ingest.py`를 통해 Milvus DB에 지식이 적재되어 있어야 합니다.
2. 질문을 임베딩(벡터화)하여 DB(Milvus Standalone/Lite)에서 가장 유사한 문서 조각(Top-K)을 찾습니다.
3. 거리 점수를 계산하여 '신뢰도(%)'와 함께 관련 문서를 반환합니다.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings

# 환경 변수 로드
load_dotenv()

class MilvusRetriever:
    """
    Milvus 벡터 데이터베이스에서 관련 문서를 검색하는 클래스입니다.
    """
    
    def __init__(self):
        """
        초기화 메서드입니다.
        Milvus 및 임베딩 모델 연결 설정을 수행합니다.
        """
        self.collection_name = os.getenv("COLLECTION_NAME", "dental_knowledge")
        
        # 로컬 임베딩 모델 설정
        self.embeddings = HuggingFaceEmbeddings(
            model_name="jhgan/ko-sroberta-multitask",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Milvus 연결 URI 설정 (Standalone URL 또는 Lite 파일 경로)
        self.milvus_uri = os.getenv("MILVUS_URI", "./data/milvus_dental.db")
        
        self.vector_db = None
        try:
            self.vector_db = Milvus(
                embedding_function=self.embeddings,
                connection_args={
                    "uri": self.milvus_uri,
                },
                collection_name=self.collection_name
            )
            print(f"MilvusRetriever 초기화 완료 (URI: {self.milvus_uri})")
        except Exception as e:
            print(f"MilvusRetriever 연결 실패: {e}")

    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """
        사용자 질문과 관련된 문서 내용을 검색하여 반환합니다.

        Args:
            query (str): 사용자의 질문
            top_k (int): 검색할 관련 문서의 개수

        Returns:
            List[str]: 검색된 문서 내용들의 리스트
        """
        if not self.vector_db:
            return ["지식 베이스 연결에 실패하여 기본 답변만 제공 가능합니다."]

        print(f"검색어: {query} 로 실제 벡터 DB 검색을 시작합니다...")
        
        try:
            # 유사도 검색 수행 (점수 포함)
            # score는 거리값이므로 낮을수록 유사도가 높음 (L2 거리 기준)
            docs_with_scores = self.vector_db.similarity_search_with_score(query, k=top_k)
            
            # 검색 결과 가공
            results = []
            for doc, score in docs_with_scores:
                content = doc.page_content
                # Milvus의 L2 거리를 코사인 유사도(Cosine Similarity)로 변환 (정규화된 벡터 기준)
                # 공식: CosineSimilarity = 1 - (score^2 / 2)
                cosine_sim = 1 - (score**2 / 2)
                confidence = max(0, cosine_sim * 100)
                
                source_info = f"[출처: {doc.metadata.get('title', '상세정보')}] (신뢰도: {confidence:.1f}%)"
                results.append(f"{source_info}\n{content}")
            
            return results
        except Exception as e:
            print(f"검색 중 오류 발생: {e}")
            return [f"검색 오류가 발생했습니다: {e}"]

if __name__ == "__main__":
    # 간단한 테스트 실행
    retriever = MilvusRetriever()
    test_query = "임플란트 수술 후 주의사항이 뭐야?"
    contexts = retriever.retrieve_context(test_query)
    for i, ctx in enumerate(contexts):
        print(f"\n--- 결과 {i+1} ---\n{ctx}")
