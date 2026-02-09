"""
[파일 역할]
로컬 LLM (Ollama) 호출을 담당하는 클라이언트 모듈입니다.
Llama 3.1 모델을 사용하여 텍스트 생성, 요약, 소견 작성 등의 작업을 수행합니다.
비용이 들지 않으며 모든 데이터는 로컬에서 처리됩니다.

[실행 순서]
1. 로컬에 Ollama가 설치되어 있고 llama3.1 모델이 있어야 합니다.
2. LlmClient 클래스를 인스턴스화합니다.
3. generate_report() 또는 stream_chat() 메서드를 호출하여 응답을 받습니다.

[사용 예시]
client = LlmClient()
response = client.simple_chat("치석이 생기는 이유가 뭐야?")
print(response)
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from src.denticheck_ai.pipelines.llm import prompts

class LlmClient:
    """
    Ollama API와 통신하여 로컬 LLM 기능을 제공하는 클래스입니다.
    """

    def __init__(self, model_name: str = "llama3.1:latest"):
        """
        초기화 메서드입니다. 로컬 Ollama 클라이언트를 설정합니다.
        
        Args:
            model_name (str): 사용할 모델 이름. 기본값은 'llama3.1:latest'.
        """
        # Ollama 서버 주소 설정 (Docker 및 로컬 환경 대응)
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        self.model = model_name
        self.llm = ChatOllama(
            model=self.model,
            base_url=base_url,
            temperature=0.2, # 전문적인 답변을 위해 창의성을 낮춤
        )
        self.parser = StrOutputParser()

    def simple_chat(self, user_message: str, language: str = "ko", system_prompt: str = None) -> str:
        """
        간단한 챗봇 대화를 수행합니다 (일괄 응답).

        Args:
            user_message (str): 사용자가 입력한 질문이나 메시지
            language (str): 답변 언어 ('ko' 또는 'en')
            system_prompt (str): 직접 지정할 페르소나 (None일 경우 의사 페르소나 자동 선택)

        Returns:
            str: AI의 응답 텍스트
        """
        if system_prompt is None:
            system_prompt = prompts.get_system_persona_doctor(language=language)
            
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            response = self.llm.invoke(messages)
            return self.parser.invoke(response)
        except Exception as e:
            return f"에러 발생: {str(e)}"

    def stream_chat(self, user_message: str, language: str = "ko", system_prompt: str = None):
        """
        실시간 스트리밍으로 답변을 생성합니다.

        Args:
            user_message (str): 사용자가 입력한 메시지
            language (str): 답변 언어 ('ko' 또는 'en')
            system_prompt (str): 직접 지정할 페르소나
        """
        if system_prompt is None:
            system_prompt = prompts.get_system_persona_doctor(language=language)
            
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        return (self.llm | self.parser).stream(messages)

    def generate_report(self, risk_level: str, detections: str, actions: str, language: str = "ko") -> str:
        """
        AI 분석 결과를 바탕으로 전문 소견 리포트를 생성합니다.

        Args:
            risk_level (str): 위험도 레벨
            detections (str): 탐지된 증상 목록
            actions (str): 추천 관리 행동
            language (str): 리포트 언어 ('ko' 또는 'en')

        Returns:
            str: 완성된 리포트 내용
        """
        template = prompts.get_report_generation_template(language=language)
        prompt_text = template.format(
            risk_level=risk_level,
            detections=detections,
            actions=actions
        )
        return self.simple_chat(prompt_text, language=language)
