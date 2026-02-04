from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("")
async def detect_lesions(file: UploadFile = File(...)):
    # Placeholder for YOLO object detection
    return {
        "detections": [
            {
                "class": "tooth",
                "confidence": 0.95,
                "bbox": [100, 100, 200, 200]
            },
            {
                "class": "cavity",
                "confidence": 0.88,
                "bbox": [150, 150, 180, 180]
            }
        ]
    }
