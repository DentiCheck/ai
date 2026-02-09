-- 1) AI 소견서 테이블 (ai_reports)
-- AI가 생성한 전문 리포트 결과를 구조화하여 저장합니다.
CREATE TABLE ai_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL UNIQUE,          -- 진단 세션 ID와 1:1 매핑
    summary TEXT NOT NULL,                   -- [NLG 1단계] 현재 상태 한 줄 요약
    details TEXT NOT NULL,                   -- [NLG 2,3단계] 상세 분석 및 관리 가이드
    disclaimer TEXT NOT NULL,                -- [NLG 4단계] 면책 고지 및 권고 사항
    language VARCHAR(10) NOT NULL DEFAULT 'ko', -- 생성된 언어 (ko, en)
    disclaimer_version VARCHAR(30) DEFAULT 'v1.0',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_check_session FOREIGN KEY (session_id) REFERENCES ai_check_sessions(id)
);

-- 2) AI 의사결정 기록 테이블 (ai_decision_records)
-- [설계 사양 2-4] 재현/감사/디버깅을 위한 YOLO, ML, 설문 등의 원천 데이터를 통째로 저장합니다.
CREATE TABLE ai_decision_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL UNIQUE,
    decision_json JSONB NOT NULL,             -- YOLO/ML/Survey/Overall 전체 데이터 (JSON 형태)
    captured_at TIMESTAMPTZ NOT NULL,         -- 이미지 촬영/분석 시점
    model_versions JSONB,                     -- 분석에 사용된 모델 버전들
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_decision_session FOREIGN KEY (session_id) REFERENCES ai_check_sessions(id)
);

-- 2) AI 챗봇 메시지 테이블 (ai_chat_messages)
-- 사용자와 AI 간의 질문 답변 내역을 저장합니다.
CREATE TABLE ai_chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL,                -- 채팅/진단 세션 ID
    role VARCHAR(20) NOT NULL,               -- 'user' 또는 'assistant'
    content TEXT NOT NULL,                   -- 메시지 내용
    language VARCHAR(10) NOT NULL,           -- 사용된 언어
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_chat_session FOREIGN KEY (session_id) REFERENCES ai_check_sessions(id)
);

-- 인덱스 추가 (조회 성능 최적화)
CREATE INDEX idx_ai_reports_session ON ai_reports(session_id);
CREATE INDEX idx_ai_chat_messages_session ON ai_chat_messages(session_id);
CREATE INDEX idx_ai_decision_records_session ON ai_decision_records(session_id);
