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
    
    # 1. 가상의 분석 데이터 (YOLO 및 ML 엔진의 결과라고 가정)
    dummy_data = {
        "risk_level": "위험 (Urgent)",
        "detections": "상악 우측 제2대구치 깊은 충치(Caries) 1건, 하악 전치부 치석(Calculus) 다량 관찰",
        "actions": "조속한 치과 방문 및 정밀 엑스레이 촬영, 충치 치료 및 스케일링 필요"
    }

    print("="*50)
    print("DentiCheck AI 전문 소견 리포트 생성 테스트")
    print("="*50)
    print(f"입력 데이터:")
    print(f"- 위험도: {dummy_data['risk_level']}")
    print(f"- 분석결과: {dummy_data['detections']}")
    print(f"- 추천조치: {dummy_data['actions']}\n")
    
    print("AI 의사가 소견서를 작성 중입니다...\n")
    print("-" * 50)
    
    # 리포트 생성 (Markdown 기호 제거 가이드라인 적용됨)
    report = client.generate_report(
        risk_level=dummy_data["risk_level"],
        detections=dummy_data["detections"],
        actions=dummy_data["actions"]
    )
    
    print(report)
    print("-" * 50)
    print("\n[테스트 완료] Markdown 기호(**) 없이 깔끔하게 출력되는지 확인하세요.")

if __name__ == "__main__":
    test_report_generation()
