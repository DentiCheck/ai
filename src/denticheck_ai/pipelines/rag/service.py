"""
[파일 역할]
RAG 검색 결과와 Ollama(로컬 LLM)를 하나로 묶어 최종 답변을 생성하는 '서비스 레이어'입니다.
검색된 지식 조각들을 바탕으로 AI가 자연스러운 문장으로 답변을 구성합니다.

[실행 방법]
1. 로컬에 Ollama가 설치되어 있고 `llama3.1` 모델이 다운로드되어 있어야 합니다.
2. `RagService` 클래스를 인스턴스화하여 `ask(질문)` 메서드를 호출합니다.

[동작 순서]
1. `MilvusRetriever`를 통해 질문과 관련된 치과 지식을 검색합니다.
2. 검색된 지식과 사용자 질문을 결합하여 전용 프롬프트를 구성합니다.
3. Ollama 모델에 프롬프트를 전달하여 최종 답변 문장을 생성합니다.
"""

import os
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.denticheck_ai.pipelines.rag.retrieve import MilvusRetriever
from src.denticheck_ai.pipelines.llm import prompts

class RagService:
    """
    RAG 검색 결과와 Ollama(Llama 3.1)를 결합하여 최종 지식 답변을 생성하는 통합 서비스 클래스입니다.
    비용 0원으로 로컬에서 작동하는 지능형 치과 상담 엔진입니다.
    """
    
    def __init__(self, model_name: str = "llama3.1:latest"):
        """
        서비스를 초기화합니다. 검색기(Milvus)와 생성기(Ollama)를 설정합니다.
        
        Args:
            model_name (str): 사용할 Ollama 모델명. 기본값은 'llama3.1'.
        """
        # 1. 문서 검색기 초기화
        self.retriever = MilvusRetriever()
        
        # 2. 로컬 LLM (Ollama) 초기화
        # Ollama 서버 주소 설정 (Docker 및 로컬 환경 대응)
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # 0원에 무제한으로 사용 가능한 로컬 모델입니다.
        self.llm = ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.2, # 일관된 답변을 위해 낮게 설정
        )
        
        self.output_parser = StrOutputParser()

    def _get_chain(self, language: str = "ko"):
        """언어별로 최적화된 프롬프트 체인을 생성합니다."""
        system_prompt = f"""당신은 친절하고 전문적인 치과 의사 '덴티체크 점검봇'입니다.
아래 제공된 [검색된 지식]만을 근거로 사용자의 질문에 답변하세요.
만약 [검색된 지식]에 질문에 대한 직접적인 답이 없다면, 아는 범위 내에서 구강 건강 상식으로 답변하되 전문적인 진료는 치과 방문이 필요함을 반드시 안내하세요.

[검색된 지식]
{{context}}

{prompts.get_common_rules(language=language)}"""

        # 영어일 경우 시스템 프롬프트 번역본 적용
        if language == "en":
            system_prompt = f"""You are a friendly and professional dentist 'DentiCheck Bot'.
Answer the user's question based ONLY on the [Retrieved Knowledge] provided below.
If there is no direct answer in the [Retrieved Knowledge], answer with general oral health knowledge but ALWAYS state that a dental visit is required for a professional diagnosis.

[Retrieved Knowledge]
{{context}}

{prompts.get_common_rules(language=language)}"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}"),
        ])
        
        return prompt | self.llm | self.output_parser

    def ask(self, question: str, language: str = "ko") -> str:
        """
        질문에 대해 RAG를 거쳐 최종 답변을 한꺼번에 생성합니다.
        """
        # 1. 관련 지식 검색
        contexts = self.retriever.retrieve_context(question, top_k=3)
        context_text = "\n\n".join(contexts)
        
        # 2. 언어별 체인 획득 및 실행
        chain = self._get_chain(language=language)
        response = chain.invoke({
            "context": context_text,
            "question": question
        })
        
        return response

    def stream_ask(self, question: str, language: str = "ko"):
        """
        질문에 대해 RAG 결과와 함께 답변을 한 글자씩 스트리밍으로 반환합니다.
        """
        # 1. 관련 지식 검색
        contexts = self.retriever.retrieve_context(question, top_k=3)
        context_text = "\n\n".join(contexts)
        
        # 2. 언어별 체인 획득 및 스트리밍 실행
        chain = self._get_chain(language=language)
        print(f"🤖 Ollama({self.llm.model})가 답변({language})을 생성 중입니다...\n")
        return chain.stream({
            "context": context_text,
            "question": question
        })

if __name__ == "__main__":
    # 간단한 연동 테스트
    service = RagService()
    test_question = "사랑니 뽑고 나서 술 마셔도 돼?"
    answer = service.ask(test_question)
    
    print("\n" + "="*50)
    print(f"질문: {test_question}")
    print(f"답변: {answer}")
    print("="*50)
