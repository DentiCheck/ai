"""
[파일 역할]
RAG (Retrieval-Augmented Generation) 파이프라인의 핵심인 '문서 검색' 모듈입니다.
사용자의 질문과 관련된 치과 의학 지식을 Vector DB (Milvus)에서 찾아오는 역할을 합니다.

[실행 순서]
1. 사전에 Milvus DB에 치의학 문서들이 임베딩되어 저장되어 있어야 합니다.
2. retrieve_context() 함수에 사용자 질문을 입력합니다.
3. 질문을 임베딩(벡터화)하여 DB에서 가장 유사한 문서 조각들을 반환합니다.

[주의사항]
현재는 Milvus 연결 코드가 주석 처리되어 있으며(Mock), 실제 연동 시 주석을 해제해야 합니다.
"""

from typing import List

class MilvusRetriever:
    """
    Milvus 벡터 데이터베이스에서 관련 문서를 검색하는 클래스입니다.
    """
    
    def __init__(self):
        """
        초기화 메서드입니다.
        Milvus 연결 설정을 수행합니다.
        """
        self.collection_name = "dental_knowledge"
        # TODO: 실제 Milvus 연결 코드 추가
        # connections.connect("default", host="localhost", port="19530")
        print("MilvusRetriever 초기화 완료 (Mock Mode)")

    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """
        사용자 질문과 관련된 문서 내용을 검색하여 반환합니다.

        Args:
            query (str): 사용자의 질문 (예: "충치는 왜 생기나요?")
            top_k (int): 검색할 관련 문서의 개수 (기본값: 3개)

        Returns:
            List[str]: 검색된 문서 내용들의 리스트
        """
        print(f"검색어: {query} 로 벡터 DB 검색을 시작합니다...")
        
        # TODO: 실제 임베딩 및 검색 로직 구현 필요
        # 1. query -> vector embedding
        # 2. collection.search(vector, top_k)
        
        # 현재는 테스트를 위해 가짜(Dummy) 데이터를 반환합니다.
        mock_results = [
            f"[참고문헌 1] {query}에 대한 답변은 구강 위생 관리 미흡이 주 원인입니다.",
            f"[참고문헌 2] 정기적인 스케일링이 {query} 예방에 가장 효과적입니다.",
            "[참고문헌 3] 올바른 칫솔질(회전법)이 중요합니다."
        ]
        
        return mock_results
