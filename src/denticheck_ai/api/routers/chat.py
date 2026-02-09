from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from denticheck_ai.pipelines.rag.service import RagService

router = APIRouter(prefix="/v1/chat", tags=["Chat"])

# 서비스 인스턴스 싱글톤
rag_service = RagService()

class ChatRequest(BaseModel):
    question: str
    language: Optional[str] = "ko" # "ko" or "en"
    stream: Optional[bool] = False

@router.post("/ask")
async def ask_question(req: ChatRequest):
    if not req.question:
        raise HTTPException(status_code=400, detail="Question is required")

    if req.stream:
        def generate():
            for chunk in rag_service.stream_ask(req.question, language=req.language):
                yield chunk
        return StreamingResponse(generate(), media_type="text/plain")
    else:
        answer = rag_service.ask(req.question, language=req.language)
        return {"answer": answer, "language": req.language}
