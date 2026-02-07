from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter(prefix="/v1/detect", tags=["Detection"])

class DetectRequest(BaseModel):
    image_url: str

class DetectionBox(BaseModel):
    label: str # caries/calculus
    confidence: float
    bbox: List[float] # [x, y, w, h]

class DetectResponse(BaseModel):
    detections: List[DetectionBox]
    summary: Dict[str, int]

@router.post("", response_model=DetectResponse)
def detect_objects(req: DetectRequest):
    # TODO: Load YOLO model and predict
    # Mocking
    return DetectResponse(
        detections=[
            DetectionBox(label="calculus", confidence=0.88, bbox=[100, 100, 50, 50])
        ],
        summary={"calculus": 1, "caries": 0}
    )
