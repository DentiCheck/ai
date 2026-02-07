"""
[파일 역할]
DentiCheck 로컬 RAG 시스템의 전체 동작을 한눈에 확인할 수 있는 '대화형 데모 스크립트'입니다.
질문을 입력하면 [지식 검색 ➔ 신뢰도 산출 ➔ AI 답변 생성] 과정을 실시간으로 보여줍니다.

[실행 방법]
프로젝트 루트에서 아래 명령어를 실행합니다.
$ export PYTHONPATH=$PYTHONPATH:.
$ python3 rag_demo.py

[특징]
- 완전 오프라인 모드: 외부 API 호출 없이 로컬 자원만 사용합니다.
- 대화형 인터페이스: 'exit'을 입력하기 전까지 연속적인 질문이 가능합니다.
"""

import os
from src.denticheck_ai.pipelines.rag.service import RagService

def main():
    """
    데모 루프를 실행하는 메인 함수입니다.
    """
    print("="*50)
    print("🦷 DentiCheck RAG 지식 검색 테스트 데모")
    print("="*50)
    print("설명: 입력하신 질문과 가장 유사한 치과 지식을 로컬 DB에서 찾아옵니다.")
    print("(종료하려면 'exit' 또는 'q'를 입력하세요.)\n")

    try:
        service = RagService()
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        return

    while True:
        query = input("\n🤔 질문을 입력하세요: ").strip()
        
        if query.lower() in ['exit', 'q', 'quit']:
            print("👋 테스트를 종료합니다.")
            break
        
        if not query:
            continue

        print(f"🔍 지식 기반 답변을 생성 중입니다... (Ollama 로컬 처리)")

        # 2. AI 답변 생성 및 스트리밍 출력
        print("-" * 50)
        print("🤖 AI 덴티체크 답변:")
        full_answer = ""
        for chunk in service.stream_ask(query):
            print(chunk, end="", flush=True)
            full_answer += chunk
        print("\n" + "-" * 50)
        
        print(f"✅ 답변 생성이 완료되었습니다.")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
