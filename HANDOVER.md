# DentiCheck AI Integration Handover Document (Full Edition)

이 문서는 DentiCheck AI 엔진 고도화 작업의 모든 기술적 맥락, 설계 결정, 그리고 구현 상세를 기록한 통합 핸도버 문서입니다. 다음 세션의 AI와 개발자가 이 문서를 통해 모든 작업 내역을 100% 동기화할 수 있도록 상세히 서술되었습니다.

---

## 1. 프로젝트 아키텍처 및 미션
- **미션**: 치과 자가진단 이미지와 설문 데이터를 기반으로 전문적인 소견을 도출하고, 신뢰할 수 있는 의학 지식(RAG)을 제공하는 지능형 엔진 구축.
- **핵심 철학**: "데이터의 자산화와 추론의 구조화". 모든 AI 의사결정은 재현 가능해야 하며, 결과물은 사용자에게 친절하고 안전해야 함.

## 2. 주요 작업 상세 내역

### 2-1. NLG(자연어 생성) 및 리포트 엔진
- **3단(4부분) 구조화 응답**:
    1. **SUMMARY**: 현재 상태를 직관적으로 파악할 수 있는 한 줄 요약.
    2. **DETAILS**: 탐지된 객체(YOLO)와 수치(ML) 기반의 상세 분석 + 케어 가이드 + 추천 루틴.
    3. **DISCLAIMER**: 법적/의학적 가이드라인을 준수한 면책 고지 및 전문가 진료 권고.
- **프롬프트 가드레일 (Safe-Guard)**:
    - **한자 사용 금지**: 한국어 답변 시 가독성 및 할루시네이션 방지를 위해 순수 한글로만 작성.
    - **Markdown 기호 제거**: PDF 생성 엔진과의 호환성을 위해 `**bold**` 등 특수 기호 일체 배제.
    - **확정 진단 회피**: '확진', '진단' 대신 '소견', '분석 결과' 등의 중립적이고 전문적인 용어 사용 강제.
    - **Persona**: 친절하면서도 전문적인 '치과 주치의' 페르소나 적용.

### 2-2. 데이터 인터페이스: Decision Record & Projection
- **Decision Record (Master JSON)**: 
    - 세션의 모든 원천 데이터(YOLO Raw Bbox, ML Probability, Survey Raw Answers, Metrics)를 포함.
    - **목적**: 데이터 자산화, 재현성 확보, 감사 추적, 디버깅.
- **LLM Input (NLG Projection)**:
    - Decision Record에서 NLG 생성에 꼭 필요한 정보만 추출한 투영본.
    - **목적**: 컨텍스트 윈도우 절약, LLM 추론 정확도 향상.

### 2-3. RAG (Retrieval-Augmented Generation) 시스템
- **데이터 소스**: 서울대학교치과병원(SNUDH) 공식 FAQ, 치아상식, 질병정보 데이터 323건.
- **수집 전략**: Throttling(1.5초 간격)과 Exponential Backoff를 적용한 지능형 크롤러 구현.
- **저장 및 검색**: 
    - 중간 데이터를 JSON 파일로 관리하여 데이터 신뢰성 검토 단계 확보.
    - Milvus Standalone을 이용한 벡터 인덱싱 및 코사인 유사도 기반 시맨틱 검색 구현 (Docker Compose 기반).
- **UX**: Generator 기반의 토큰 스트리밍 기술로 대기 시간 최소화.

### 2-4. 데이터베이스 및 스키마 설계 (`docs/`)
- **`ai_reports`**: 소견서를 3개 영역(`summary`, `details`, `disclaimer`)으로 분리하여 DB 컬럼에 직접 매핑.
- **`ai_decision_records`**: `decision_json` (JSONB) 컬럼을 통해 모든 분석 시점의 스냅샷 보관.
- **인덱싱**: `session_id` 기반 인덱스를 추가하여 대량 데이터 조회 성능 최적화.

### 2-5. 백엔드 통합 가이드
- **GraphQL Proxy 구조**: 백엔드(Spring Boot)가 AI 엔진 전면에서 인증, 저장, API 오케스트레이션을 담당하는 구조 확립.
- **API Spec**: `POST /v1/report/generate`를 통해 구조화된 JSON을 주고받는 규격 정의.
### 2-6. 백엔드 팀용 마이그레이션 가이드
- **상세**: `docs/BACKEND_MIGRATION_GUIDE.md`

### 2-7. PDF 생성 팀원용 가이드
- **핵심**: AI가 생성한 텍스트(`summary`, `details`, `disclaimer`)와 원천 데이터(`Decision Record`)를 PDF 템플릿에 매핑하는 방법 정의.
- **상세**: `docs/PDF_GENERATION_GUIDE.md` 참조.

---

## 3. 핵심 의사결정 근거 (ADR)
- **왜 로컬 LLM인가?**: 민감한 의료 데이터의 외부 유출 방지(Privacy) 및 운영 비용 0원 달성.
- **왜 JSON 중간 저장인가?**: 크롤링 서버 부하 방지 및 인덱싱 전 human-in-the-loop 검토를 위함.
- **왜 3단 구성인가?**: 사용자의 인지 부하를 줄이고, 앱 UI 및 PDF 리포트에서 데이터 재활용도를 높이기 위함.

---

## 4. 향후 로드맵 (Next Action Items)
- [ ] **Foxit PDF Bridge**: 생성된 3단 데이터를 PDF 템플릿에 자동 주입하는 로직 완성.
- [ ] **History Delta Algorithm**: Decision Record 간의 차이점(예: 치석 수 증가 등)을 수치화하여 소견서에 반영.
- [ ] **Multimodal Expansion**: 이미지 자체의 특징 리스트를 Decision Record에 추가하여 더 정밀한 소견 도출.

---
**주의**: 본 문서는 익명화 작업을 완료하였으며, 모든 파일 및 주석에서 개인 정보는 제거되었습니다. 아키텍처와 로직의 연속성만을 참조하십시오.
