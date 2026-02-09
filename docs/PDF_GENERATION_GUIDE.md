# 📄 PDF Generation Guide (for Foxit/Report Team)

이 문서는 AI 엔진에서 생성된 **3단 구조 소견서**와 **Decision Record**를 활용하여 최종 PDF 리포트를 생성하는 담당자(강진용 팀원 등)를 위한 기술 가이드입니다.

---

## 1. 데이터 소스 (Input Data)

백엔드에서 PDF 생성 모듈로 전달되는 데이터는 크게 두 가지입니다.

### A. 구조화된 소견서 (NLG Output)
AI가 생성한 3단 텍스트 데이터입니다.
- `summary`: 한 줄로 핵심을 찌르는 제목/요약 (PDF 상단 배치 권장)
- `details`: 분석 내용과 관리 루틴 (PDF 본문 영역)
- `disclaimer`: 법적 면책 고지 및 권고 (PDF 하단/푸터 영역)

### B. Decision Record (Raw Analysis Data)
리포트에 시각적인 지표(그래프, 수치)를 추가하고 싶을 때 사용합니다.
- `yolo`: 객체 탐지 수 및 면적비 (예: "치석 3건 발견"을 배지로 표시)
- `ml`: 위험도 확률 (예: "치주염 위험도 85%" 그래프 생성 시 활용)
- `overall`: 종합 위험 레벨 (`GREEN`, `YELLOW`, `RED`) 및 아이콘 매핑용 코드

---

## 2. PDF 디자인 및 레이아웃 매핑 가이드

| PDF 영역 | 매핑 데이터 | 디자인 팁 |
| :--- | :--- | :--- |
| **헤더/요약** | `summary` | 폰트 크기를 크게 하고, 굵은 폰트를 사용하여 한눈에 들어오게 배치. |
| **상세 분석** | `details` | 줄바꿈(`\n`)을 인식하여 단락을 나누고, 텍스트 상자에 여백을 충분히 확보. |
| **종합 비주얼** | `ml`, `yolo` 수치 | 텍스트보다는 프로그레스 바(Progress Bar)나 치아 맵 배지로 시각화. |
| **면책 고지** | `disclaimer` | 눈에 띄지 않게 작지만 명확한 폰트로 하단 회색 박스 등에 배치. |

---

## 3. 핵심 주의사항 (Pre-processing)

1. **Markdown 기호 처리**:
   - AI 소견서(`summary`, `details`, `disclaimer`)는 이미 **Markdown 기호가 제거된 Plain Text** 상태로 제공됩니다.
   - 따라서 별도의 파싱 없이 그대로 PDF 텍스트 필드에 주입하면 됩니다.

2. **줄바꿈 처리**:
   - `details` 필드 내에는 단락 구분을 위해 `\n\n` 또는 `\n`이 포함되어 있습니다.
   - PDF 라이브러리(Foxit 등) 사용 시 멀티라인 텍스트 지원 여부를 확인하고 렌더링하세요.

3. **언어 설정**:
   - `language` 필드(`ko`, `en`)에 따라 폰트(Noto Sans 등)가 깨지지 않도록 적절한 폰트 임베딩이 필요합니다.

---

## 4. 데이터 활용 예시 (Algorithm)

```python
# 예: 리포트 생성 가상 로직
report_data = get_ai_report_from_db(session_id)
decision_raw = get_decision_record_from_db(session_id)

# 1. 텍스트 주입
pdf_template.fill_field("TEXT_SUMMARY", report_data["summary"])
pdf_template.fill_field("TEXT_DETAILS", report_data["details"])
pdf_template.fill_field("TEXT_FOOTER", report_data["disclaimer"])

# 2. 시각화 지표 주입
if decision_raw["ml"]["periodontitis"]["prob"] > 0.7:
    pdf_template.set_icon_color("RISK_ICON", "RED")
```

---
💡 **문의**: NLG 데이터 구조 및 가이드라인에 대한 문의는 AI 엔진 파트에 요청해 주세요.
