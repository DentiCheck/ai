from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from denticheck_ai.api.routers import quality, detect, risk
# from denticheck_ai.api.routers import health # If health.py exists we can keep it, but I'll add a simple one here if likely missing or just define it inline

app = FastAPI(title="DentiCheck AI Service", version="0.1.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
# Note: Prefixes are already defined in the routers themselves (e.g., /v1/quality)
app.include_router(quality.router)
app.include_router(detect.router)
app.include_router(risk.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "denticheck-ai"}

@app.get("/")
async def root():
    return {"message": "Denticheck AI Service is running. Documentation: /docs"}
