from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/quality", tags=["Quality"])

class QualityRequest(BaseModel):
    image_url: str

class QualityResponse(BaseModel):
    status: str # pass / fail
    blur_score: float
    brightness_mean: float
    message: str = "Good quality"

@router.post("/check", response_model=QualityResponse)
def check_quality(req: QualityRequest):
    # TODO: Implement actual OpenCV logic here
    # Mocking for initial contract
    return QualityResponse(
        status="pass",
        blur_score=120.5,
        brightness_mean=100.0,
        message="Image is clear"
    )
