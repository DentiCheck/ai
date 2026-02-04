from fastapi import FastAPI
from denticheck_ai.api.routers import health, quality, detect

app = FastAPI(title="Denticheck AI Service")

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(quality.router, prefix="/api/v1/quality", tags=["quality"])
app.include_router(detect.router, prefix="/api/v1/detect", tags=["detect"])

@app.get("/")
async def root():
    return {"message": "Denticheck AI API is running"}
