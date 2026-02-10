from datetime import datetime
from uuid import uuid4
from denticheck_ai.pipelines.decision.decision_model import (
    DecisionRecord, DecisionMeta, GateResult, GateMetrics,
    YoloResult, ClassSummary, DetectionBox,
    MlResult, GingivitisResult, PeriodontalResult,
    SurveyResult
)
from denticheck_ai.pipelines.decision.rules import evaluate_overall_risk

def create_mock_record(
    calculus_present=False,
    caries_count=0,
    lesion_present=False,
    gingivitis_suspect=False,
    periodontal_prob=0.1
):
    """Factory to create a DecisionRecord with specific conditions."""
    return DecisionRecord(
        meta=DecisionMeta(
            session_id=uuid4(), user_id=uuid4(), image_id=uuid4(),
            image_url="http://test", captured_at=datetime.now(),
            model_versions={"yolo": "v1"}
        ),
        gate=GateResult(status="pass", metrics=GateMetrics(
            oral_present_prob=0.9, blur_score=100, brightness_mean=100,
            clipping_ratio=0, contrast_std=10
        )),
        yolo=YoloResult(
            summary={
                "calculus": ClassSummary(present=calculus_present, max_score=0.9, count=1 if calculus_present else 0, area_ratio=0),
                "caries": ClassSummary(present=caries_count > 0, max_score=0.9, count=caries_count, area_ratio=0),
                "lesion": ClassSummary(present=lesion_present, max_score=0.9, count=1 if lesion_present else 0, area_ratio=0),
            },
            detections=[]
        ),
        ml=MlResult(
            gingivitis=GingivitisResult(prob=0.8 if gingivitis_suspect else 0.2, suspect=gingivitis_suspect, threshold=0.5),
            periodontal=PeriodontalResult(prob=periodontal_prob, suspect=periodontal_prob > 0.65, threshold=0.65)
        ),
        survey=SurveyResult(answers={})
    )

def test_rules():
    print("--- Testing Rule Engine ---")

    # Case 1: Normal
    r1 = create_mock_record()
    res1 = evaluate_overall_risk(r1)
    print(f"Case 1 (Clean): Level={res1.level}, Actions={[a.code for a in res1.recommended_actions]}")
    assert res1.level == "normal"

    # Case 2: Calculus -> Attention
    r2 = create_mock_record(calculus_present=True)
    res2 = evaluate_overall_risk(r2)
    print(f"Case 2 (Calculus): Level={res2.level}, Actions={[a.code for a in res2.recommended_actions]}")
    assert res2.level == "attention"
    assert "scaling_consult" in [a.code for a in res2.recommended_actions]

    # Case 3: Lesion -> Recommend Visit
    r3 = create_mock_record(lesion_present=True)
    res3 = evaluate_overall_risk(r3)
    print(f"Case 3 (Lesion): Level={res3.level}, Actions={[a.code for a in res3.recommended_actions]}")
    assert res3.level == "recommend_visit"
    assert res3.safety_flags["lesion_caution_text_required"] == True

    print("--- All Tests Passed! ---")

if __name__ == "__main__":
    test_rules()
