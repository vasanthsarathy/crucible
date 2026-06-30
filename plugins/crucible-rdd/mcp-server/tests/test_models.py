from crucible.models import (
    ProjectState, ReviewRound, ReviewerFeedback, ReviewVerdict,
    UnderstandingCheck, Assumption, Idea, Concept, ConceptStatus,
    ReviewerPersona, VenueProfile, Paper,
)
from datetime import datetime, timezone


def test_project_state_roundtrip():
    state = ProjectState(
        project_id="test-abc123",
        name="Test Project",
        seed_idea="A seed idea",
        target_venue="NeurIPS",
        current_stage="SEED",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
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
        timestamp=datetime.now(timezone.utc),
    )
    assert round_.gate_result == "fail"
    assert round_.reviews[0].verdict == ReviewVerdict.REJECT


def test_concept_status_enum():
    concept = Concept(
        name="IID assumption",
        status=ConceptStatus.ENCOUNTERED,
        stage_introduced="PROBLEM",
        timestamp=datetime.now(timezone.utc),
    )
    assert concept.status == ConceptStatus.ENCOUNTERED
