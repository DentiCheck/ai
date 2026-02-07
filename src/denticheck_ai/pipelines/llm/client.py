"""
[파일 역할]
LLM (Large Language Model) API 호출을 담당하는 클라이언트 모듈입니다.
OpenAI GPT-4 등의 모델을 사용하여 텍스트 생성, 요약, 소견 작성 등의 작업을 수행합니다.

[실행 순서]
1. .env 파일에 OPENAI_API_KEY가 설정되어 있어야 합니다.
2. LlmClient 클래스를 인스턴스화합니다.
3. generate_report() 또는 simple_chat() 메서드를 호출하여 응답을 받습니다.

[사용 예시]
client = LlmClient()
response = client.simple_chat("치석이 생기는 이유가 뭐야?")
print(response)
"""

import os
from openai import OpenAI

class LlmClient:
    """
    OpenAI API와 통신하여 LLM 기능을 제공하는 클래스입니다.
    """

    def __init__(self):
        """
        초기화 메서드입니다.
        환경 변수에서 API 키를 로드하고 OpenAI 클라이언트를 설정합니다.
        """
        # API 키는 환경 변수에서 가져옵니다. 보안을 위해 코드에 직접 적지 마세요.
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("경고: OPENAI_API_KEY가 환경 변수에 없습니다. LLM 기능이 작동하지 않을 수 있습니다.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o" # 기본 모델 설정 (비용에 따라 gpt-3.5-turbo 등 변경 가능)

    def simple_chat(self, user_message: str, system_prompt: str = "You are a helpful dental assistant.") -> str:
        """
        간단한 챗봇 대화를 수행합니다.

        Args:
            user_message (str): 사용자가 입력한 질문이나 메시지
            system_prompt (str): AI의 페르소나나 역할을 정의하는 프롬프트 (기본값: 치과 조수)

        Returns:
            str: AI의 응답 텍스트
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7 # 창의성 조절 (0~2)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"에러 발생: {str(e)}"

    def generate_report(self, decision_data: dict) -> str:
        """
        AI 분석 결과(Decision Record)를 바탕으로 사용자가 읽기 편한 종합 리포트를 생성합니다.

        Args:
            decision_data (dict): 룰 엔진에서 판단한 위험도 및 탐지 결과 데이터

        Returns:
            str: 생성된 종합 리포트 텍스트
        """
        # TODO: prompts.py에서 템플릿을 가져와서 포맷팅해야 함
        prompt = f"""
        다음 치아 분석 데이터를 바탕으로 환자에게 전달할 친절한 소견서를 작성해주세요.
        데이터: {decision_data}
        """
        return self.simple_chat(prompt, system_prompt="당신은 친절하고 전문적인 치과 의사입니다.")
