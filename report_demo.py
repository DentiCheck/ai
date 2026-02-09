"""
[파일 역할]
AI 분석 데이터(위험도, 탐지 결과)를 바탕으로 AI 의사가 전문 소견서를 작성하는 기능을 테스트하는 데모입니다.
LlmClient의 generate_report 기능을 활용합니다.

[실행 방법]
$ export PYTHONPATH=$PYTHONPATH:.
$ python3 report_demo.py
"""

from src.denticheck_ai.pipelines.llm.client import LlmClient

def test_report_generation():
    client = LlmClient()
    
    # 가상의 분석 데이터
    dummy_data = {
        "risk_level": "위험 (Urgent)",
        "detections": "상악 우측 제2대구치 깊은 충치(Caries) 1건, 하악 전치부 치석(Calculus) 다량 관찰",
        "actions": "조속한 치과 방문 및 정밀 엑스레이 촬영, 충치 치료 및 스케일링 필요"
    }

    print("==================================================")
    print("🌍 DentiCheck AI 전문 소견 리포트 다국어 테스트")
    print("==================================================")
    
    # 1. 한국어 리포트 생성
    print("\n[Case 1] 한국어 소견서 생성 중...")
    report_ko = client.generate_report(**dummy_data, language="ko")
    print("-" * 50)
    print(report_ko)
    print("-" * 50)

    # 2. 영어 리포트 생성
    print("\n[Case 2] English Report Generating...")
    report_en = client.generate_report(**dummy_data, language="en")
    print("-" * 50)
    print(report_en)
    print("-" * 50)

    print("\n[테스트 완료] Markdown 기호(**) 없이 깔끔하게 출력되는지 확인하세요.")

if __name__ == "__main__":
    test_report_generation()
