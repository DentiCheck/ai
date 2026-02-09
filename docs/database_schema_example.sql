-- 1) AI 소견서 테이블 (ai_reports)
-- AI가 생성한 전문 리포트 결과를 저장합니다.
CREATE TABLE ai_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL UNIQUE,          -- 진단 세션 ID와 1:1 매핑
    summary TEXT NOT NULL,                   -- 한 줄 요약 및 상세 분석 결과
    routine_guide TEXT NOT NULL,             -- 사용자 맞춤형 관리 루틴
    warnings TEXT,                           -- 치과 방문 권고 및 주의사항
    language VARCHAR(10) NOT NULL DEFAULT 'ko', -- 생성된 언어 (ko, en)
    disclaimer_version VARCHAR(30),          -- 면책 고지문 버전
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_check_session FOREIGN KEY (session_id) REFERENCES ai_check_sessions(id) -- 기존 세션 테이블과 연결
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
