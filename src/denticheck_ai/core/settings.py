from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    API_URL: str = "http://localhost:8000"
    
    # YOLO Settings
    YOLO_MODEL_PATH: str = "models/yolo/weights/yolov8n.pt"
    
    class Config:
        env_file = ".env"

settings = Settings()
