from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path

from .models import (
    Assumption,
    Concept,
    ConceptStatus,
    Idea,
    ProjectState,
    ProjectSummary,
    ReviewerPersona,
    ReviewRound,
    Stage,
    UnderstandingCheck,
)

STAGE_ORDER: list[Stage] = ["SEED", "PROBLEM", "SURVEY", "SOLUTION", "DEVELOP", "PAPER"]


def _now() -> datetime:
    return datetime.now(UTC)


def _slug(text: str) -> str:
    words = re.sub(r"[^a-z0-9 ]", "", text.lower()).split()[:4]
    return "-".join(words) + "-" + uuid.uuid4().hex[:6]


class ProjectStore:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _project_dir(self, project_id: str) -> Path:
        return self.base_dir / project_id

    # ── Project management ───────────────────────────────────────────────

    def create_project(self, name: str, seed_idea: str, target_venue: str | None = None) -> str:
        project_id = _slug(seed_idea)
        d = self._project_dir(project_id)
        d.mkdir(parents=True, exist_ok=True)
        (d / "sections").mkdir(exist_ok=True)
        (d / "experiments").mkdir(exist_ok=True)
        (d / "review_rounds").mkdir(exist_ok=True)
        (d / "understanding_log").mkdir(exist_ok=True)
        now = _now()
        state = ProjectState(
            project_id=project_id,
            name=name,
            seed_idea=seed_idea,
            target_venue=target_venue,
            current_stage="SEED",
            created_at=now,
            updated_at=now,
        )
        (d / "state.json").write_text(state.model_dump_json(indent=2))
        (d / "assumptions_log.json").write_text("[]")
        (d / "ideas_log.json").write_text("[]")
        (d / "concepts.json").write_text("[]")
        (d / "reviewer_personas.json").write_text("[]")
        stage_history = [{"stage": "SEED", "entered_at": now.isoformat()}]
        (d / "stage_history.json").write_text(json.dumps(stage_history, indent=2))
        return project_id

    def get_project(self, project_id: str) -> ProjectState:
        path = self._project_dir(project_id) / "state.json"
        return ProjectState.model_validate_json(path.read_text())

    def list_projects(self) -> list[ProjectSummary]:
        summaries = []
        for d in sorted(self.base_dir.iterdir()):
            state_file = d / "state.json"
            if state_file.exists():
                state = ProjectState.model_validate_json(state_file.read_text())
                summaries.append(
                    ProjectSummary(
                        project_id=state.project_id,
                        name=state.name,
                        current_stage=state.current_stage,
                        target_venue=state.target_venue,
                        created_at=state.created_at,
                    )
                )
        return summaries

    def advance_stage(self, project_id: str) -> Stage:
        state = self.get_project(project_id)
        idx = STAGE_ORDER.index(state.current_stage)
        if idx >= len(STAGE_ORDER) - 1:
            raise ValueError(f"Already at final stage: {state.current_stage}")
        next_stage = STAGE_ORDER[idx + 1]
        now = _now()
        state.current_stage = next_stage
        state.updated_at = now
        d = self._project_dir(project_id)
        (d / "state.json").write_text(state.model_dump_json(indent=2))
        history = json.loads((d / "stage_history.json").read_text())
        history.append({"stage": next_stage, "entered_at": now.isoformat()})
        (d / "stage_history.json").write_text(json.dumps(history, indent=2))
        return next_stage

    # ── Sections ─────────────────────────────────────────────────────────

    def update_section(self, project_id: str, section: str, content: str) -> None:
        path = self._project_dir(project_id) / "sections" / f"{section}.md"
        path.write_text(content)
        self._touch_updated(project_id)

    def get_section(self, project_id: str, section: str) -> str:
        path = self._project_dir(project_id) / "sections" / f"{section}.md"
        return path.read_text() if path.exists() else ""

    # ── Review rounds ─────────────────────────────────────────────────────

    def log_review_round(self, project_id: str, round_: ReviewRound) -> str:
        path = self._project_dir(project_id) / "review_rounds" / f"{round_.round_id}.json"
        path.write_text(round_.model_dump_json(indent=2))
        return round_.round_id

    def get_review_history(self, project_id: str, stage: str | None = None) -> list[ReviewRound]:
        rounds_dir = self._project_dir(project_id) / "review_rounds"
        rounds = []
        for f in sorted(rounds_dir.glob("*.json")):
            r = ReviewRound.model_validate_json(f.read_text())
            if stage is None or r.stage == stage:
                rounds.append(r)
        return rounds

    # ── Understanding checks ──────────────────────────────────────────────

    def log_understanding_check(self, project_id: str, check: UnderstandingCheck) -> None:
        path = self._project_dir(project_id) / "understanding_log" / f"{check.check_id}.json"
        path.write_text(check.model_dump_json(indent=2))

    def get_understanding_history(self, project_id: str) -> list[UnderstandingCheck]:
        log_dir = self._project_dir(project_id) / "understanding_log"
        return [
            UnderstandingCheck.model_validate_json(f.read_text())
            for f in sorted(log_dir.glob("*.json"))
        ]

    # ── Concepts ──────────────────────────────────────────────────────────

    def get_concept_map(self, project_id: str) -> list[Concept]:
        path = self._project_dir(project_id) / "concepts.json"
        return [Concept.model_validate(c) for c in json.loads(path.read_text())]

    def update_concept_status(
        self, project_id: str, concept_name: str, status: ConceptStatus, stage: Stage
    ) -> None:
        path = self._project_dir(project_id) / "concepts.json"
        concepts = json.loads(path.read_text())
        for c in concepts:
            if c["name"] == concept_name:
                c["status"] = status.value
                path.write_text(json.dumps(concepts, indent=2))
                return
        concepts.append(
            Concept(
                name=concept_name,
                status=status,
                stage_introduced=stage,
                timestamp=_now(),
            ).model_dump(mode="json")
        )
        path.write_text(json.dumps(concepts, indent=2))

    # ── Assumptions ───────────────────────────────────────────────────────

    def log_assumption(self, project_id: str, assumption: Assumption) -> None:
        path = self._project_dir(project_id) / "assumptions_log.json"
        assumptions = json.loads(path.read_text())
        assumptions.append(assumption.model_dump(mode="json"))
        path.write_text(json.dumps(assumptions, indent=2))

    def get_assumptions_log(self, project_id: str) -> list[Assumption]:
        path = self._project_dir(project_id) / "assumptions_log.json"
        return [Assumption.model_validate(a) for a in json.loads(path.read_text())]

    def update_assumption(
        self, project_id: str, assumption_id: str, is_explicit: bool, is_justified: bool
    ) -> None:
        path = self._project_dir(project_id) / "assumptions_log.json"
        assumptions = json.loads(path.read_text())
        for a in assumptions:
            if a["assumption_id"] == assumption_id:
                a["is_explicit"] = is_explicit
                a["is_justified"] = is_justified
        path.write_text(json.dumps(assumptions, indent=2))

    # ── Ideas log ─────────────────────────────────────────────────────────

    def log_idea(self, project_id: str, idea: Idea) -> None:
        path = self._project_dir(project_id) / "ideas_log.json"
        ideas = json.loads(path.read_text())
        ideas.append(idea.model_dump(mode="json"))
        path.write_text(json.dumps(ideas, indent=2))

    def get_ideas_log(self, project_id: str) -> list[Idea]:
        path = self._project_dir(project_id) / "ideas_log.json"
        return [Idea.model_validate(i) for i in json.loads(path.read_text())]

    # ── Reviewer personas ─────────────────────────────────────────────────

    def get_reviewer_personas(self, project_id: str) -> list[ReviewerPersona]:
        path = self._project_dir(project_id) / "reviewer_personas.json"
        return [ReviewerPersona.model_validate(p) for p in json.loads(path.read_text())]

    def add_reviewer_persona(self, project_id: str, persona: ReviewerPersona) -> None:
        path = self._project_dir(project_id) / "reviewer_personas.json"
        personas = json.loads(path.read_text())
        personas.append(persona.model_dump(mode="json"))
        path.write_text(json.dumps(personas, indent=2))

    # ── Experiments ───────────────────────────────────────────────────────

    def add_experiment(
        self, project_id: str, name: str, script: str, results: dict | None = None
    ) -> None:
        exp_dir = self._project_dir(project_id) / "experiments"
        (exp_dir / f"{name}.py").write_text(script)
        if results is not None:
            (exp_dir / f"{name}_results.json").write_text(json.dumps(results, indent=2))

    def update_experiment_results(self, project_id: str, name: str, results: dict) -> None:
        path = self._project_dir(project_id) / "experiments" / f"{name}_results.json"
        path.write_text(json.dumps(results, indent=2))

    # ── Internal helpers ──────────────────────────────────────────────────

    def _touch_updated(self, project_id: str) -> None:
        d = self._project_dir(project_id)
        path = d / "state.json"
        state = ProjectState.model_validate_json(path.read_text())
        state.updated_at = _now()
        path.write_text(state.model_dump_json(indent=2))
