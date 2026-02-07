from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/risk", tags=["Risk"])

class RiskRequest(BaseModel):
    image_url: str
    detections: list = [] # Optional: Pass detection results if needed

class RiskResponse(BaseModel):
    gingivitis_prob: float
    periodontal_prob: float
    risk_level: str # normal / attention / danger

@router.post("", response_model=RiskResponse)
def analyze_risk(req: RiskRequest):
    # TODO: Load ML model (sklearn/pytorch) and predict
    # Mocking
    return RiskResponse(
        gingivitis_prob=0.3,
        periodontal_prob=0.1,
        risk_level="normal"
    )
