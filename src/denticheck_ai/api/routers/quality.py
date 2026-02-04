from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/check")
async def check_quality(file: UploadFile = File(...)):
    # Placeholder for brightness, blur, framing checks
    return {
        "is_valid": True,
        "metrics": {
            "brightness": 0.8,
            "blur": 0.1,
            "framing": "ok"
        }
    }
