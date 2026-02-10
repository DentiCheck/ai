from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from uuid import UUID

# --- Gate Models ---
class GateMetrics(BaseModel):
    oral_present_prob: float
    blur_score: float
    brightness_mean: float
    clipping_ratio: float
    contrast_std: float

class GateResult(BaseModel):
    status: str  # pass | recapture
    reasons: List[str] = []
    metrics: GateMetrics

# --- YOLO Models ---
class DetectionBox(BaseModel):
    label: str
    confidence: float
    bbox: Dict[str, float]  # x, y, w, h

class ClassSummary(BaseModel):
    present: bool
    max_score: float
    count: int
    area_ratio: float

class YoloResult(BaseModel):
    summary: Dict[str, ClassSummary] # calculus, caries, lesion
    detections: List[DetectionBox]

# --- ML Models ---
class GingivitisResult(BaseModel):
    prob: float
    suspect: bool
    threshold: float

class PeriodontalResult(BaseModel):
    prob: float
    suspect: bool
    threshold: float

class MlResult(BaseModel):
    gingivitis: GingivitisResult
    periodontal: PeriodontalResult

# --- Survey Models ---
class SurveyResult(BaseModel):
    answers: Dict[str, Any]
    risk_score: Optional[float] = None

# --- Overall Models (Rule-based Output) ---
class RecommendedAction(BaseModel):
    code: str
    priority: str # high, medium, low

class OverallResult(BaseModel):
    level: str # normal, attention, recommend_visit, urgent
    reasons: List[str]
    recommended_actions: List[RecommendedAction]
    safety_flags: Dict[str, bool]

# --- Root Decision Record ---
class DecisionMeta(BaseModel):
    session_id: UUID
    user_id: UUID
    image_id: UUID
    image_url: str
    captured_at: datetime
    model_versions: Dict[str, str]

class DecisionRecord(BaseModel):
    meta: DecisionMeta
    gate: GateResult
    yolo: YoloResult
    ml: MlResult
    survey: Optional[SurveyResult] = None
    history: Optional[Dict[str, Any]] = None
    overall: Optional[OverallResult] = None  # Populated by Rule Engine
