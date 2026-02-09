from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from denticheck_ai.pipelines.llm.client import LlmClient

router = APIRouter(prefix="/v1/report", tags=["Report"])

# LLM 클라이언트 인스턴스
llm_client = LlmClient()

# 아키텍처 설계 사양: NLG용 투영본(Projection) 데이터 모델
class YoloSummary(BaseModel):
    present: bool
    count: int
    area_ratio: Optional[float] = 0.0
    max_score: Optional[float] = 0.0

class MlResult(BaseModel):
    suspect: bool
    prob: float

class OverallAction(BaseModel):
    code: str
    priority: str

class OverallInfo(BaseModel):
    level: str
    recommended_actions: List[OverallAction]
    safety_flags: Dict[str, bool]

class ReportRequest(BaseModel):
    yolo: Dict[str, YoloSummary]
    ml: Dict[str, MlResult]
    survey: Dict[str, Any]
    history: Dict[str, Any]
    overall: OverallInfo
    disclaimer_version: str = "v1.0"
    language: Optional[str] = "ko" # "ko" or "en"

class ReportResponse(BaseModel):
    summary: str
    details: str
    disclaimer: str
    language: str

@router.post("/generate", response_model=ReportResponse)
async def generate_report(req: ReportRequest):
    try:
        # 구조화된 JSON 데이터를 분석하여 3단 구조(요약/상세/고지) 문장 생성
        result = llm_client.generate_report(data=req, language=req.language)
        return ReportResponse(
            summary=result["summary"],
            details=result["details"],
            disclaimer=result["disclaimer"],
            language=req.language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
