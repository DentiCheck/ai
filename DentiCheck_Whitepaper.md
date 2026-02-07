# DentiCheck AI System Whitepaper (RAG & LLM Part)

이 문서는 **DentiCheck** 프로젝트에서 이정륜(팀원)이 담당한 **RAG(Retrieval-Augmented Generation) 엔진 및 로컬 LLM 통합**에 관한 기술 명세와 구현 성과를 기록한 시스템 백서입니다.

---

## 📑 개정 이력 (Revision History)

| 버전 | 날짜 | 작성자 | 설명 | 상태 |
| :--- | :--- | :--- | :--- | :--- |
| **v1.6** | 2026-02-08 | 이정륜 | 작성자(이정륜) 담당 파트인 RAG/LLM 중심의 기술 명세 최적화 | **Latest** |
| **v1.2** | 2026-02-08 | 이정륜 | 크롤러 명세 통합 및 로컬 RAG 시스템 완성 | Superseded |

---

## 1. 담당 역할 및 핵심 기술

### 1-1. 담당 역할 (Role: AI - Knowledge/LLM)
- **데이터 엔진**: 서울대치과병원(SNUDH) 전문 지식 데이터 수집 및 정제.
- **검색 엔진**: Milvus Lite 벡터 DB를 활용한 로컬 지식 검색(RAG) 파이프라인 구축.
- **생성 엔진**: 로컬 Ollama(Llama 3.1) 모델 최적화 및 치과 전문 페르소나 설계.
- **통합 서비스**: AI 분석 결과(YOLO/ML)를 취합하여 최종 LLM 리포트를 생성하는 비즈니스 로직 구현.

### 1-2. 핵심 기술 스택 (Tech Stack)
- **Framework**: LangChain, FastAPI (Gateway), BeautifulSoup4
- **Vector DB**: Milvus Lite (Local file-based)
- **Embedding**: HuggingFace (`jhgan/ko-sroberta-multitask`)
- **LLM Engine**: Ollama (`llama3.1:latest`)

---

## 2. 시스템 동작 프로세스 (Workflow)

이정륜 님이 구축한 파이프라인의 핵심 동작 순서입니다.

1. **`snudh_crawler.py`**: 서울대치과병원의 FAQ, 치아상식 등 총 **323건**의 신뢰도 높은 데이터를 수집하여 JSON으로 보관.
2. **`ingest.py`**: 수집된 데이터를 CPU 기반 로컬 임베딩 후 `Milvus Lite` 벡터 DB에 적재.
3. **`retrieve.py`**: 사용자 질문을 벡터화하여 가장 유사한 지식 조각을 검색하고, 코사인 유사도 기반 **신뢰도(Confidence %)** 산출.
4. **`service.py`**: 검색된 지식을 Ollama 모델에 주입하여 "할루시네이션(환각)" 없는 전문 답변 생성.
5. **`rag_demo.py`**: 위 모든 과정을 실구매 비용 없이 로컬에서 무제한 스트리밍으로 테스트할 수 있는 인터페이스 제공.

---

## 3. 주요 구현 상세 및 결과 규격

### 3-1. 지능형 상담 (Knowledge Chat)
- **특징**: 단순 일반 상식이 아닌, 수집된 **전문 치과 문서**에 기반한 답변만 하도록 프롬프트를 설계하여 신뢰성 확보.
- **결과 규격**:
```json
{
  "status": "success",
  "data": {
    "question": "교정하려면 꼭 이를 발치해야 하나요?",
    "answer": "치아 교정 시 발치 여부는 구강 내 공간 확보 정도에 따라 달라집니다. 검색된 지식에 따르면...",
    "confidence_score": 75.5,
    "sources": [
      {
        "title": "교정 치료와 발치 안내",
        "url": "https://snudh.org/knowledge/102",
        "distance": 0.7
      }
    ]
  }
}
```

### 3-2. 최종 AI 소견 생성 (LLM Opinion)
- **특징**: 타 파트(YOLO 탐지 결과, ML 위험도 점수)의 결과값을 컨텍스트로 받아 사용자 친화적인 자연어 리포트 및 관리 루틴 생성.
- **결과 규격**:
```json
{
  "ai_opinion": "탐지된 영상 분석 결과, 어금니 안쪽의 치석 침착이 관찰됩니다. 현재 방치 시 치주염으로 발전할 가능성이 높습니다.",
  "dental_routine": "치간 칫솔 사용을 생활화하고, 1주일 내 스케일링을 위해 치과 방문을 권장합니다."
}
```

---

## 4. 실행 및 검증 가이드 (Execution)
본 프로젝트의 RAG 엔진을 시연하기 위한 절차입니다.

1. **모델 준비**: `ollama pull llama3.1`
2. **데이터 적재**: `python3 src/denticheck_ai/pipelines/rag/ingest.py`
3. **통합 테스트**: `python3 rag_demo.py`

---

## 5. 협업 및 운영 가이드 (이정륜 파트)
- **DB 원칙**: AI 엔진은 추론만 담당하며, 모든 결과 기록 및 관리는 `denticheck-api`를 통하여 수행하도록 설계.
- **스트리밍**: 긴 답변의 경우 사용자 경험을 위해 SSE(Server-Sent Events) 프로토콜을 통한 스트리밍 인터페이스 지원.
- **보안**: 모델과 데이터가 모두 로컬 시스템 내에 머물도록 하여 의료 데이터의 유출 위험성 원천 차단.
