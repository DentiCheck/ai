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

class RagService:
    """
    RAG 검색 결과와 Ollama(Llama 3.1)를 결합하여 최종 지식 답변을 생성하는 통합 서비스 클래스입니다.
    비용 0원으로 로컬에서 작동하는 지능형 치과 상담 엔진입니다.
    """
    
    def __init__(self, model_name: str = "llama3.1"):
        """
        서비스를 초기화합니다. 검색기(Milvus)와 생성기(Ollama)를 설정합니다.
        
        Args:
            model_name (str): 사용할 Ollama 모델명. 기본값은 'llama3.1'.
        """
        # 1. 문서 검색기 초기화
        self.retriever = MilvusRetriever()
        
        # 2. 로컬 LLM (Ollama) 초기화
        # 0원에 무제한으로 사용 가능한 로컬 모델입니다.
        self.llm = ChatOllama(
            model=model_name,
            temperature=0.2, # 일관된 답변을 위해 낮게 설정
        )
        
        # 3. 프롬프트 템플릿 설정 (치과 전문가 페르소나 부여)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 친절하고 전문적인 치과 의사 '덴티체크 점검봇'입니다.
아래 제공된 [검색된 지식]만을 근거로 사용자의 질문에 답변하세요.
만약 [검색된 지식]에 질문에 대한 직접적인 답이 없다면, 아는 범위 내에서 구강 건강 상식으로 답변하되 전문적인 진료는 치과 방문이 필요함을 반드시 안내하세요.

[검색된 지식]
{context}

답변 규칙:
1. 한국어로 답변하세요.
2. 친절하고 신뢰감 있는 말투를 사용하세요.
3. 답변 끝에는 항상 "정확한 진단은 치과 방문을 직접 권장드립니다."라는 문구를 포함하세요."""),
            ("human", "{question}"),
        ])
        
        # 4. 체인 구성
        self.chain = self.prompt | self.llm | StrOutputParser()

    def ask(self, question: str) -> str:
        """
        질문에 대해 RAG를 거쳐 최종 답변을 생성합니다.
        """
        # 1. 관련 지식 검색
        # 신뢰도 점수를 포함해서 가져오지만, LLM에는 텍스트 내용만 전달합니다.
        contexts = self.retriever.retrieve_context(question, top_k=3)
        context_text = "\n\n".join(contexts)
        
        # 2. LLM 답변 생성
        print(f"🤖 Ollama({self.llm.model})가 답변을 생성 중입니다...")
        response = self.chain.invoke({
            "context": context_text,
            "question": question
        })
        
        return response

if __name__ == "__main__":
    # 간단한 연동 테스트
    service = RagService()
    test_question = "사랑니 뽑고 나서 술 마셔도 돼?"
    answer = service.ask(test_question)
    
    print("\n" + "="*50)
    print(f"질문: {test_question}")
    print(f"답변: {answer}")
    print("="*50)
