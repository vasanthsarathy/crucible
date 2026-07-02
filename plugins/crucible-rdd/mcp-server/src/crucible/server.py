from __future__ import annotations

import json
import os
import uuid
from datetime import UTC, datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .landscape import search_literature
from .models import (
    Assumption,
    ConceptStatus,
    Idea,
    PivotEvaluation,
    ReviewerPersona,
    ReviewRound,
    Stage,
    UnderstandingCheck,
)
from .reviewer_personas import get_active_personas
from .store import ProjectStore


def _now() -> datetime:
    return datetime.now(UTC)


def create_server(base_dir: Path | None = None) -> FastMCP:
    if base_dir is None:
        base_dir = Path(os.environ.get("CRUCIBLE_DIR", ".crucible"))
    store = ProjectStore(base_dir=Path(base_dir))
    mcp = FastMCP("crucible")

    # ── Project management ────────────────────────────────────────────────

    @mcp.tool()
    def crucible_create_project(name: str, seed_idea: str, target_venue: str | None = None) -> str:
        """Create a new research project. Returns the project_id."""
        return store.create_project(name=name, seed_idea=seed_idea, target_venue=target_venue)

    @mcp.tool()
    def crucible_get_project(project_id: str) -> str:
        """Get full project state as JSON."""
        return store.get_project(project_id).model_dump_json(indent=2)

    @mcp.tool()
    def crucible_list_projects() -> str:
        """List all research projects as JSON array."""
        return json.dumps([p.model_dump(mode="json") for p in store.list_projects()], indent=2)

    @mcp.tool()
    def crucible_advance_stage(project_id: str) -> str:
        """Advance project to the next stage. Returns the new stage name."""
        return store.advance_stage(project_id)

    # ── Sections ──────────────────────────────────────────────────────────

    @mcp.tool()
    def crucible_update_section(project_id: str, section: str, content: str) -> str:
        """Write or update a paper section (abstract, problem, survey, solution, method, experiments, results, related_work, conclusion)."""
        store.update_section(project_id, section, content)
        return f"Section '{section}' updated."

    @mcp.tool()
    def crucible_get_section(project_id: str, section: str) -> str:
        """Read a paper section. Returns empty string if section has no content yet."""
        return store.get_section(project_id, section)

    # ── Experiments ───────────────────────────────────────────────────────

    @mcp.tool()
    def crucible_add_experiment(
        project_id: str, name: str, script: str, results: str | None = None
    ) -> str:
        """Add or update an experiment script. results is an optional JSON string."""
        results_dict = json.loads(results) if results else None
        store.add_experiment(project_id, name, script, results_dict)
        return f"Experiment '{name}' saved."

    @mcp.tool()
    def crucible_update_experiment_results(project_id: str, name: str, results: str) -> str:
        """Update experiment results. results is a JSON string."""
        store.update_experiment_results(project_id, name, json.loads(results))
        return f"Results for '{name}' updated."

    # ── Reviewer personas ─────────────────────────────────────────────────

    @mcp.tool()
    def crucible_get_reviewer_personas(project_id: str) -> str:
        """Get active reviewer personas (builtins + any project-specific additions) as JSON."""
        personas = get_active_personas(project_id, store)
        return json.dumps([p.model_dump(mode="json") for p in personas], indent=2)

    @mcp.tool()
    def crucible_add_reviewer_persona(project_id: str, persona_json: str) -> str:
        """Add a custom reviewer persona to this project. persona_json is a ReviewerPersona JSON object."""
        persona = ReviewerPersona.model_validate_json(persona_json)
        persona.is_custom = True
        store.add_reviewer_persona(project_id, persona)
        return f"Custom reviewer '{persona.name}' added."

    # ── Review rounds ─────────────────────────────────────────────────────

    @mcp.tool()
    def crucible_log_review_round(project_id: str, round_json: str) -> str:
        """Persist a completed review round. round_json is a ReviewRound JSON object."""
        round_ = ReviewRound.model_validate_json(round_json)
        return store.log_review_round(project_id, round_)

    @mcp.tool()
    def crucible_get_review_history(project_id: str, stage: str | None = None) -> str:
        """Get review round history as JSON. Optionally filter by stage."""
        history = store.get_review_history(project_id, stage)
        return json.dumps([r.model_dump(mode="json") for r in history], indent=2)

    # ── Understanding tracking ────────────────────────────────────────────

    @mcp.tool()
    def crucible_log_understanding_check(project_id: str, check_json: str) -> str:
        """Persist a Socratic understanding check. check_json is an UnderstandingCheck JSON object."""
        check = UnderstandingCheck.model_validate_json(check_json)
        store.log_understanding_check(project_id, check)
        return "Understanding check logged."

    @mcp.tool()
    def crucible_get_understanding_history(project_id: str) -> str:
        """Get all understanding check history as JSON."""
        history = store.get_understanding_history(project_id)
        return json.dumps([c.model_dump(mode="json") for c in history], indent=2)

    @mcp.tool()
    def crucible_get_concept_map(project_id: str) -> str:
        """Get the concept map (all tracked concepts and their understanding status) as JSON."""
        concepts = store.get_concept_map(project_id)
        return json.dumps([c.model_dump(mode="json") for c in concepts], indent=2)

    @mcp.tool()
    def crucible_update_concept_status(
        project_id: str, concept_name: str, status: str, stage: Stage
    ) -> str:
        """Update or add a concept's understanding status (encountered, explained, applied)."""
        store.update_concept_status(project_id, concept_name, ConceptStatus(status), stage)
        return f"Concept '{concept_name}' set to {status}."

    # ── Assumptions ───────────────────────────────────────────────────────

    @mcp.tool()
    def crucible_log_assumption(project_id: str, assumption_json: str) -> str:
        """Log a surfaced assumption. assumption_json is an Assumption JSON object."""
        assumption = Assumption.model_validate_json(assumption_json)
        store.log_assumption(project_id, assumption)
        return "Assumption logged."

    @mcp.tool()
    def crucible_update_assumption(
        project_id: str, assumption_id: str, is_explicit: bool, is_justified: bool
    ) -> str:
        """Mark an assumption as explicitly stated and/or justified in the paper."""
        store.update_assumption(project_id, assumption_id, is_explicit, is_justified)
        return "Assumption updated."

    @mcp.tool()
    def crucible_get_assumptions_log(project_id: str) -> str:
        """Get all surfaced assumptions as JSON."""
        assumptions = store.get_assumptions_log(project_id)
        return json.dumps([a.model_dump(mode="json") for a in assumptions], indent=2)

    # ── Research navigation ───────────────────────────────────────────────

    @mcp.tool()
    def crucible_log_idea(project_id: str, idea_text: str) -> str:
        """Log a tangent idea to the ideas backlog without interrupting the current project."""
        state = store.get_project(project_id)
        idea = Idea(
            idea_id=uuid.uuid4().hex[:8],
            text=idea_text,
            source_stage=state.current_stage,
            timestamp=_now(),
        )
        store.log_idea(project_id, idea)
        return (
            f"Idea captured: '{idea_text[:60]}...'"
            if len(idea_text) > 60
            else f"Idea captured: '{idea_text}'"
        )

    @mcp.tool()
    def crucible_get_ideas_log(project_id: str) -> str:
        """Get all captured ideas as JSON."""
        ideas = store.get_ideas_log(project_id)
        return json.dumps([i.model_dump(mode="json") for i in ideas], indent=2)

    # ── Pivot evaluation ──────────────────────────────────────────────────

    @mcp.tool()
    def crucible_log_pivot_evaluation(
        project_id: str, new_direction: str, outcome: str, rationale: str
    ) -> str:
        """Log a pivot evaluation decision. outcome must be 'pivot' or 'capture_and_continue'."""
        state = store.get_project(project_id)
        evaluation = PivotEvaluation(
            eval_id=uuid.uuid4().hex[:8],
            stage=state.current_stage,
            new_direction=new_direction,
            outcome=outcome,  # type: ignore[arg-type]
            rationale=rationale,
            timestamp=_now(),
        )
        path = store._project_dir(project_id) / "pivot_log.json"
        existing = json.loads(path.read_text()) if path.exists() else []
        existing.append(evaluation.model_dump(mode="json"))
        path.write_text(json.dumps(existing, indent=2))
        return f"Pivot evaluation logged: {outcome}"

    # ── Landscape search ──────────────────────────────────────────────────

    @mcp.tool()
    async def crucible_search_literature(query: str, limit: int = 10) -> str:
        """Search arXiv and Semantic Scholar for papers matching the query. Returns JSON array of Paper objects."""
        papers = await search_literature(query, limit)
        return json.dumps([p.model_dump(mode="json") for p in papers], indent=2)

    return mcp


def main() -> None:
    base_dir = Path(os.environ.get("CRUCIBLE_DIR", ".crucible"))
    server = create_server(base_dir=base_dir)
    server.run()


if __name__ == "__main__":
    main()
