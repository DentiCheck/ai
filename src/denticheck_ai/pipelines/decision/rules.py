from typing import List, Dict
from .decision_model import (
    DecisionRecord, OverallResult, RecommendedAction
)

def evaluate_overall_risk(record: DecisionRecord) -> OverallResult:
    """
    Combines YOLO, ML, and Survey results to determine the overall risk level and recommendations.
    This is a deterministic Rule-Based System.
    """
    yolo = record.yolo
    ml = record.ml
    survey = record.survey

    reasons = []
    actions = []
    safety_flags = {"lesion_caution_text_required": False}
    
    level = "normal"

    # 1. Check Lesions (Highest Priority)
    if yolo.summary.get("lesion", {}).get("present"):
        reasons.append("lesion_detected")
        level = "recommend_visit"
        safety_flags["lesion_caution_text_required"] = True
        actions.append(RecommendedAction(code="hospital_visit_lesion", priority="high"))

    # 2. Check Periodontal Risk
    if ml.periodontal.prob > 0.65: # Threshold example
        reasons.append("periodontal_high_risk")
        if level != "recommend_visit":
            level = "recommend_visit"
        actions.append(RecommendedAction(code="hospital_visit_periodontal", priority="high"))
    elif ml.gingivitis.suspect:
        reasons.append("gingivitis_suspect")
        if level == "normal":
            level = "attention"
        actions.append(RecommendedAction(code="gum_care_routine", priority="medium"))

    # 3. Check Calculus (Tartar)
    if yolo.summary.get("calculus", {}).get("present"):
        reasons.append("calculus_present")
        if level == "normal":
            level = "attention"
        actions.append(RecommendedAction(code="scaling_consult", priority="medium"))
    
    # 4. Check Caries
    if yolo.summary.get("caries", {}).get("present"):
        reasons.append("caries_detected")
        if level == "normal":
            level = "attention"
        # If count is high, escalate
        if yolo.summary["caries"].count >= 3:
             level = "recommend_visit"
        actions.append(RecommendedAction(code="cavity_care", priority="medium"))

    # Default action if normal
    if level == "normal":
        actions.append(RecommendedAction(code="maintain_routine", priority="low"))

    return OverallResult(
        level=level,
        reasons=reasons,
        recommended_actions=actions,
        safety_flags=safety_flags
    )
