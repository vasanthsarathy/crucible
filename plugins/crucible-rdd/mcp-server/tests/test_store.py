import json
import pytest
from pathlib import Path
from datetime import datetime, timezone
from crucible.store import ProjectStore
from crucible.models import ReviewRound, ReviewerFeedback, ReviewVerdict, UnderstandingCheck


@pytest.fixture
def store(tmp_path):
    return ProjectStore(base_dir=tmp_path / ".crucible")


def test_create_and_get_project(store):
    project_id = store.create_project(
        name="My Paper",
        seed_idea="What if we challenged the IID assumption?",
        target_venue="NeurIPS",
    )
    assert project_id is not None
    state = store.get_project(project_id)
    assert state.name == "My Paper"
    assert state.current_stage == "SEED"
    assert state.target_venue == "NeurIPS"


def test_create_project_creates_directories(store):
    project_id = store.create_project(name="Test", seed_idea="seed")
    project_dir = store._project_dir(project_id)
    assert (project_dir / "sections").is_dir()
    assert (project_dir / "experiments").is_dir()
    assert (project_dir / "review_rounds").is_dir()
    assert (project_dir / "understanding_log").is_dir()
    assert (project_dir / "assumptions_log.json").exists()
    assert (project_dir / "ideas_log.json").exists()
    assert (project_dir / "stage_history.json").exists()
    assert (project_dir / "concepts.json").exists()
    assert (project_dir / "reviewer_personas.json").exists()


def test_list_projects(store):
    store.create_project(name="Paper A", seed_idea="seed a")
    store.create_project(name="Paper B", seed_idea="seed b")
    projects = store.list_projects()
    assert len(projects) == 2


def test_update_and_get_section(store):
    project_id = store.create_project(name="Test", seed_idea="seed")
    store.update_section(project_id, "problem", "## Problem\n\nLet $X$ be a random variable.")
    content = store.get_section(project_id, "problem")
    assert "random variable" in content


def test_advance_stage(store):
    project_id = store.create_project(name="Test", seed_idea="seed")
    new_stage = store.advance_stage(project_id)
    assert new_stage == "PROBLEM"
    state = store.get_project(project_id)
    assert state.current_stage == "PROBLEM"


def test_advance_stage_progression(store):
    project_id = store.create_project(name="Test", seed_idea="seed")
    stages = ["PROBLEM", "SURVEY", "SOLUTION", "DEVELOP", "PAPER"]
    for expected in stages:
        stage = store.advance_stage(project_id)
        assert stage == expected


def test_log_and_get_review_round(store):
    project_id = store.create_project(name="Test", seed_idea="seed")
    store.advance_stage(project_id)  # → PROBLEM
    reviews = [
        ReviewerFeedback(
            reviewer_id="flash",
            verdict=ReviewVerdict.REJECT,
            concerns=["not novel"],
            suggestions=[],
            feedback_text="REJECT: no hook",
        )
    ]
    round_ = ReviewRound(
        round_id="2026-01-01-120000",
        stage="PROBLEM",
        reviews=reviews,
        devil_advocate_text="worst paper",
        gate_result="fail",
        timestamp=datetime.now(timezone.utc),
    )
    store.log_review_round(project_id, round_)
    history = store.get_review_history(project_id)
    assert len(history) == 1
    assert history[0].reviews[0].reviewer_id == "flash"


def test_log_and_get_understanding_check(store):
    project_id = store.create_project(name="Test", seed_idea="seed")
    check = UnderstandingCheck(
        check_id="2026-01-01-130000",
        stage="PROBLEM",
        question="Why is this hard?",
        answer="Because of NP-hardness",
        assessment="clear",
        timestamp=datetime.now(timezone.utc),
    )
    store.log_understanding_check(project_id, check)
    history = store.get_understanding_history(project_id)
    assert len(history) == 1
    assert history[0].assessment == "clear"
