from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from denticheck_ai.api.routers import chat, report

app = FastAPI(title="DentiCheck AI Service", version="0.1.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register AI Role Routers
app.include_router(chat.router)
app.include_router(report.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "denticheck-ai"}

@app.get("/")
async def root():
    return {"message": "Denticheck AI Service is running. Documentation: /docs"}
