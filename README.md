# Denticheck AI

덴티체크 AI 서비스입니다.

## 📖 상세 문서
RAG 전담 기술 보고서 및 실행 가이드는 **[이곳 (DentiCheck_AI_Knowledge_System.md)](./DentiCheck_AI_Knowledge_System.md)**에서 확인하실 수 있습니다.

## 주요 기능
- 치아 품질 체크 (밝기, 블러, 입벌림 등)
- YOLO를 이용한 치아 및 병변 탐지
- 질환 위험도 분석 (ML)
- 의학 지식 기반 RAG (LLM)

## 시작하기
```bash
poetry install
python -m src.denticheck_ai.api.main
```
