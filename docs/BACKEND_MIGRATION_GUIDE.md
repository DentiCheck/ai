# 🚀 Backend Migration Guide (v1.0 -> v2.0)

이 문서는 기존 AI 엔진 연동 방식에서 **정제된 3단 소견서 구조** 및 **Decision Record 저장 체계**로 전환하기 위해 백엔드(Spring Boot) 팀원이 수정해야 할 핵심 사항을 정리하고 있습니다.

---

## 📝 4줄 핵심 요약 (TL;DR)
1. **[DB] 테이블 추가**: 원천 데이터 저장을 위한 `ai_decision_records` 테이블 생성.
2. **[DB] 컬럼명 변경**: `ai_reports` 내 `routine_guide` ➔ `details`, `warnings` ➔ `disclaimer`로 Rename.
3. **[App] DTO 수정**: AI 응답이 단일 String에서 **3단 JSON(summary, details, disclaimer)**으로 변경됨, 이를 파싱하도록 수정.
4. **[App] 요청 보강**: AI 호출 시 `yolo/ml/survey/overall` 데이터를 **구조화된 JSON 규격**에 맞춰 전송.

---

---

## 1. API 응답 데이터 구조 변화 (CRITICAL)

AI 엔진의 리포트 생성 응답이 단일 필드에서 **4개 필드**로 분리되었습니다.

- **기존 (v1.0)**: `{ "report": "...", "language": "ko" }`
- **변경 (v2.0)**:
  ```json
  {
    "summary": "한 줄 요약",
    "details": "상세 분석 및 케어 가이드",
    "disclaimer": "면책 고지 및 권고",
    "language": "ko"
  }
  ```
- **액션 아이템**: 백엔드의 `AiReportResponse` DTO에 `summary`, `details`, `disclaimer` 필드를 추가하고 기존 `report` 필드를 제거하거나 매핑을 수정하세요.

---

## 2. 데이터베이스 스키마 및 매핑 변경

### A. `ai_reports` 테이블 컬럼 매핑 (중요)
기존에 작성된 컬럼 이름을 아래와 같이 **변경(Rename)**하셔야 합니다.

| 기존 컬럼명 (이미지) | **변경 후 (v2.0)** | 변경 사유 |
| :--- | :--- | :--- |
| `summary` | **`summary`** | 단순 요약에서 **'한 줄 직관 요약'**으로 전문화 |
| `routine_guide` | **`details`** | 가이드를 넘어 **'상세 분석+케어 루틴'**을 모두 포함 |
| `warnings` | **`disclaimer`** | 주의사항을 **'의학적 면책 고지'** 규격으로 강화 |

- **SQL 액션**: 
  ```sql
  ALTER TABLE ai_reports RENAME COLUMN routine_guide TO details;
  ALTER TABLE ai_reports RENAME COLUMN warnings TO disclaimer;
  ```

### B. `ai_decision_records` 테이블 신설 (NEW)
모든 분석 시점의 원천 데이터(YOLO/ML/Survey 전체)를 저장해야 합니다.
- **액션 아이템**: AI 엔진 호출 직전 혹은 직후에 백엔드에서 생성한 전체 분석 데이터 JSON을 `decision_json` (JSONB) 컬럼에 보관하세요. 이는 추후 히스토리 분석 및 디버깅의 핵심 자산이 됩니다.

---

## 3. 리포트 생성 요청 데이터 (Request Body)

NLG 품질 향상을 위해 더 구체적인 데이터를 요구합니다.

- **엔드포인트**: `POST /v1/report/generate`
- **필수 포함 데이터**:
    - `yolo`: 탐지 객체별 `count`, `area_ratio`, `max_score`
    - `ml`: 질환별 `prob`, `suspect`
    - `survey`: 사용자 설문 응답 객체
    - `overall`: **백엔드 룰 엔진이 계산한** `level` 및 `recommended_actions` (AI는 이를 해석만 합니다.)

---

## 4. 프롬프트 규칙 변경 (참고용)

NLG 톤앤매너가 아래와 같이 고정되었습니다. 백엔드에서 별도의 후처리를 할 필요가 없습니다.
1. **한자(漢字) 미사용**: 모든 답변은 순수 한글입니다.
2. **Markdown 기호 미사용**: 가독성을 위해 `**` 등의 특수 기호가 제거되었습니다.
3. **진단 표현 회피**: '확진' 대신 '소견' 표현을 사용합니다.

---

💡 **도움말**: 상세한 구현 예시는 `docs/integration_bridge_guide.md`의 리졸버(Resolver) 섹션을 참조해 주세요.
