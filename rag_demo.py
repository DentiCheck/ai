import os
from src.denticheck_ai.pipelines.rag.service import RagService

def main():
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
        answer = service.ask(query)

        print("\n" + "·"*30)
        print("🤖 AI 덴티체크 답변")
        print("·"*30)
        print(f"\n{answer}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
