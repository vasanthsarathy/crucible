from datetime import UTC, datetime

from crucible.models import (
    Concept,
    ConceptStatus,
    ProjectState,
    ReviewerFeedback,
    ReviewerPersona,
    ReviewRound,
    ReviewVerdict,
)


def test_project_state_roundtrip():
    state = ProjectState(
        project_id="test-abc123",
        name="Test Project",
        seed_idea="A seed idea",
        target_venue="NeurIPS",
        current_stage="SEED",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    json_str = state.model_dump_json()
    restored = ProjectState.model_validate_json(json_str)
    assert restored.project_id == "test-abc123"
    assert restored.current_stage == "SEED"


def test_review_round_gate_result():
    feedback = ReviewerFeedback(
        reviewer_id="flash",
        verdict=ReviewVerdict.REJECT,
        concerns=["not novel"],
        suggestions=[],
        feedback_text="REJECT",
    )
    round_ = ReviewRound(
        round_id="2026-01-01-120000",
        stage="PROBLEM",
        sections_reviewed=["problem"],
        devil_advocate_text="weakest paper ever",
        reviews=[feedback],
        gate_result="fail",
        timestamp=datetime.now(UTC),
    )
    assert round_.gate_result == "fail"
    assert round_.reviews[0].verdict == ReviewVerdict.REJECT


def test_concept_status_enum():
    concept = Concept(
        name="IID assumption",
        status=ConceptStatus.ENCOUNTERED,
        stage_introduced="PROBLEM",
        timestamp=datetime.now(UTC),
    )
    assert concept.status == ConceptStatus.ENCOUNTERED


def test_reviewer_persona_new_fields_have_defaults():
    # Backward compat: legacy persona JSON lacks the new fields.
    p = ReviewerPersona.model_validate(
        {
            "reviewer_id": "legacy",
            "name": "Legacy",
            "lens": "x",
            "evaluation_focus": "y",
            "default_stance": "z",
        }
    )
    assert p.axis == "cross_cutting"
    assert p.role == "reviewer"
    assert p.excellence_signal == ""
    assert p.anti_heuristics == []


def test_reviewer_persona_accepts_new_fields():
    p = ReviewerPersona(
        reviewer_id="t",
        name="T",
        lens="l",
        evaluation_focus="e",
        default_stance="s",
        axis="soundness",
        role="champion",
        excellence_signal="great",
        anti_heuristics=["no SOTA reflex"],
    )
    assert p.axis == "soundness"
    assert p.role == "champion"
    assert p.anti_heuristics == ["no SOTA reflex"]
