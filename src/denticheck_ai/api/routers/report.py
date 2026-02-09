from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from denticheck_ai.pipelines.llm.client import LlmClient

router = APIRouter(prefix="/v1/report", tags=["Report"])

# LLM 클라이언트 인스턴스
llm_client = LlmClient()

class ReportRequest(BaseModel):
    risk_level: str
    detections: str
    actions: str
    language: Optional[str] = "ko" # "ko" or "en"

class ReportResponse(BaseModel):
    report: str
    language: str

@router.post("/generate", response_model=ReportResponse)
async def generate_report(req: ReportRequest):
    try:
        report = llm_client.generate_report(
            risk_level=req.risk_level,
            detections=req.detections,
            actions=req.actions,
            language=req.language
        )
        return ReportResponse(report=report, language=req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
