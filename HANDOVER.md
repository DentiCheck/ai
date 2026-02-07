# Lee Jung-ryun's Project Workspace (AI & Backend Domain)

이 문서는 **이정륜(AI 개발자 / LLM & Backend 담당)** 님의 작업 환경 세팅 및 프로젝트 인수인계를 위한 가이드입니다.
새로운 컴퓨터에서 작업을 시작할 때 이 문서를 참고하세요.

---

## 1. 담당 역할 (Role & Responsibility)

### **AI Part Developer (LLM & Backend)**
*   **AI Engine (`denticheck-ai`)**:
    *   **LLM/RAG**: OpenAI GPT 연동, 프롬프트 엔지니어링, RAG 파이프라인(크롤러, 임베딩, 검색) 구현
    *   **Decision Logic**: 룰 베이스 위험도 판정(`rules.py`), 데이터 모델 설계
*   **AI Backend (`denticheck-api`)**:
    *   **Domain Design**: `ai_check` (검사 요청/결과), `knowledge` (지식 챗봇) 도메인 설계 및 구현
    *   **Integration**: AI 서비스 호출 및 결과 DB 저장 로직 담당

---

## 2. 프로젝트 현황 (Current Progress)

### ✅ 완료된 작업 (2026-02-07 기준)
#### 1. `denticheck-ai` (Python) - **RAG 파이프라인 완성** 🚀
*   **Knowledge Base**: 서울대치과병원 데이터 **323건 전수 수집** 완료 (`snudh_knowledge.json`)
*   **Local Embedding**: OpenAI 없이 로컬에서 작동하는 한국어 임베딩 구축 (`ko-sroberta-multitask`)
*   **Vector DB**: **Milvus Lite** 도입 (별도 서버 없이 `./data/milvus_dental.db` 파일로 관리)
*   **Search Engine**: 실제 지식 기반 벡터 검색 기능(`retrieve.py`) 검증 완료

#### 2. `denticheck-ai` Core Logic
*   **Decision Engine**:
    *   `DecisionRecord`: YOLO, Risk, Survey 통합 데이터 모델 설계
    *   `rules.py`: 탐지 결과 기반 종합 판정 로직 스켈레톤 구현
*   **LLM Integration**:
    *   OpenAI GPT 연동 클라이언트 및 전문 리포트 생성 프롬프트 구축

#### 3. Configuration & DevOps
*   **Git Workflow**: `feature/rag-implementation` 브랜치 운용 및 원격 저장소(`ai`) 연동
*   **Dependency**: 로컬 임베딩 및 Milvus Lite를 위한 의존성 정리 (`pyproject.toml`)

### 🚧 진행 중 / 예정 작업 (To-Do)
1.  **[1순위] Decision Engine 정교화 (`rules.py`)** 🎯
    *   YOLO 탐지 결과와 설문 데이터를 결합한 최종 판정 로직 실제화
2.  **[2순위] 품질 체크 로직 구현 (`quality.py`)**
    *   OpenCV 등을 활용하여 이미지의 분석 적합성(초점, 각도 등) 자동 판정
3.  **[3순위] Java-Python 연동 및 통합 테스트**
    *   API 서버(`denticheck-api`)에서 AI 서비스를 호출하고 결과를 DB에 저장하는 전 과정 검증

---

## 3. 개발 가이드 & 스펙 (Development Specs)

### 3-1. AI 서비스 흐름 (Pipeline)
1.  **이미지 업로드** (App -> S3)
2.  **Job 생성** (API -> DB): `ai_check_job` 생성 (status: `PENDING`)
3.  **분석 요청** (API -> AI): `POST /v1/analyze`
4.  **AI 처리**:
    *   `Quality Check` -> `YOLO Detection` -> `Risk Analysis` -> `LLM Report`
5.  **결과 반환**: AI -> API (JSON) -> DB 저장

### 3-2. RAG (지식 챗봇)
*   **Source**: 서울대학교치과병원 FAQ/건강정보
*   **Flow**: 질문 -> 임베딩 -> Milvus 검색 -> GPT 생성 (with 출처)
*   **Rule**: 할루시네이션 방지를 위해 검색된 문서 내에서만 답변 생성

---

## 4. 새 컴퓨터 세팅 가이드 (Setup Guide)

### Step 1. 필수 도구 설치
1.  **Git / VS Code** 설치
2.  **Java 17 (JDK)**: `JAVA_HOME` 환경 변수 설정
3.  **Python 3.11**: **설치 시 `Add Python to PATH` 필수 체크**
4.  **Docker Desktop** (선택 사항)

### Step 2. 프로젝트 클론
```bash
mkdir denticheck-workspace
cd denticheck-workspace
git clone <denticheck-ai-repo-url>
git clone <denticheck-api-repo-url>
```

### Step 3. Python 환경 설정 (`denticheck-ai`)
```bash
cd denticheck-ai
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\Activate.ps1
# (CMD 사용 시: venv\Scripts\activate.bat)

# 의존성 설치 (로컬 임베딩 및 RAG 필수)
pip install fastapi uvicorn openai beautifulsoup4 requests
pip install langchain-milvus langchain-huggingface sentence-transformers milvus-lite
```

### Step 4. Java 빌드 (`denticheck-api`)
```bash
cd ../denticheck-api
./gradlew clean build -x test
```

---

## 5. 프로젝트 구조 및 환경변수 (Added)

### 5-1. 디렉토리 구조 (Directory Structure)
```
denticheck-ai
├── src
│   └── denticheck_ai
│       ├── api
│       │   ├── routers       # quality.py, detect.py, risk.py
│       │   └── main.py       # FastAPI Entry Point
│       └── pipelines
│           ├── decision      # rules.py (Rule Engine)
│           ├── llm           # client.py, prompts.py (OpenAI)
│           └── rag           # crawler/, ingest.py, retrieve.py
├── data                      # 크롤링 결과 저장 폴더 (snudh_knowledge.json)
└── pyproject.toml            # Poetry 의존성 설정 파일
```

### 5-2. 환경 변수 (.env)
`denticheck-ai/.env` 파일을 생성하고 아래 내용을 입력해야 합니다.
```ini
# OpenAI API Key (LLM 필수)
OPENAI_API_KEY=sk-proj-...

# Milvus (RAG DB)
MILVUS_URI=http://localhost:19530
MILVUS_TOKEN=root:Milvus

# Service Config
LOG_LEVEL=INFO
```

---

## 6. 트러블슈팅 (Troubleshooting)

### Q1. `python` 명령어를 찾을 수 없다고 뜹니다.
*   **원인**: Python 설치 시 `Add to PATH`를 체크하지 않았거나, 리부팅이 필요할 수 있습니다.
*   **해결**: 설치 프로그램을 다시 실행해 `Modify` -> `Add Python to environment variables`를 체크하세요.

### Q2. `poetry` 명령어가 실행되지 않습니다.
*   **원인**: 전역 설치가 되어있지 않거나 권한 문제입니다.
*   **해결**: 가상환경(`venv`)을 사용하고 `python -m pip install poetry`로 설치하거나, 위 가이드처럼 `pip install -r requirements.txt` (또는 개별 설치) 방식을 사용하세요.

### Q3. 크롤러 실행 시 `ModuleNotFoundError` 발생
*   **원인**: 가상환경이 활성화되지 않았거나 라이브러리 설치가 안 된 경우입니다.
*   **해결**: `.\venv\Scripts\Activate.ps1` 실행 후 `pip install requests beautifulsoup4`를 다시 수행하세요.

---

## 7. 작업 시작 (Action Item)

가장 먼저 **크롤러가 정상 작동하는지** 확인해주세요.

```bash
# denticheck-ai 폴더, 가상환경 켜진 상태
python src/denticheck_ai/pipelines/rag/crawler/snudh_crawler.py
```
*   `data/snudh_knowledge.json` 파일 생성 여부 확인
*   성공 시 다음 작업(`ingest.py`) 시작
