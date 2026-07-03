from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class ReviewVerdict(StrEnum):
    ACCEPT = "accept"
    REVISE = "revise"
    REJECT = "reject"
    FINDINGS = "findings"  # for Linnaeus and Socrates


class ConceptStatus(StrEnum):
    ENCOUNTERED = "encountered"
    EXPLAINED = "explained"
    APPLIED = "applied"


Stage = Literal["SEED", "PROBLEM", "SURVEY", "SOLUTION", "DEVELOP", "PAPER"]
GateResult = Literal["pass", "fail"]
ReviewAxis = Literal["soundness", "significance", "cross_cutting"]
ReviewerRole = Literal["reviewer", "champion", "ethics"]


class ProjectState(BaseModel):
    project_id: str
    name: str
    seed_idea: str
    target_venue: str | None = None
    current_stage: Stage = "SEED"
    created_at: datetime
    updated_at: datetime


class ProjectSummary(BaseModel):
    project_id: str
    name: str
    current_stage: Stage
    target_venue: str | None = None
    created_at: datetime


class ReviewerFeedback(BaseModel):
    reviewer_id: str
    verdict: ReviewVerdict
    concerns: list[str] = []
    suggestions: list[str] = []
    feedback_text: str


class ReviewRound(BaseModel):
    round_id: str
    stage: Stage
    sections_reviewed: list[str] = []
    devil_advocate_text: str = ""
    reviews: list[ReviewerFeedback] = []
    gate_result: GateResult | None = None
    timestamp: datetime


class UnderstandingCheck(BaseModel):
    check_id: str
    stage: Stage
    concept: str | None = None
    question: str
    answer: str
    assessment: Literal["clear", "partial", "gap"]
    gaps: list[str] = []
    timestamp: datetime


class Assumption(BaseModel):
    assumption_id: str
    stage: Stage
    assumption: str
    source: str  # reviewer_id or "Socrates"
    is_explicit: bool = False
    is_justified: bool = False
    timestamp: datetime


class Idea(BaseModel):
    idea_id: str
    text: str
    source_stage: Stage
    timestamp: datetime


class Concept(BaseModel):
    name: str
    status: ConceptStatus = ConceptStatus.ENCOUNTERED
    stage_introduced: Stage
    timestamp: datetime


class ReviewerPersona(BaseModel):
    reviewer_id: str
    name: str
    lens: str
    evaluation_focus: str
    default_stance: str
    axis: ReviewAxis = "cross_cutting"
    role: ReviewerRole = "reviewer"
    excellence_signal: str = ""
    anti_heuristics: list[str] = []
    is_voting: bool = True  # False for findings-only, champion, and ethics
    is_custom: bool = False  # True if added per-project


class VenueProfile(BaseModel):
    venue: str
    reviewer_weights: dict[str, float]  # reviewer_id → weight multiplier
    notes: str = ""


class Paper(BaseModel):
    title: str
    authors: list[str] = []
    abstract: str = ""
    url: str
    arxiv_id: str | None = None
    year: int | None = None
    venue: str | None = None


class PivotEvaluation(BaseModel):
    eval_id: str
    stage: Stage
    new_direction: str
    outcome: Literal["pivot", "capture_and_continue"]
    rationale: str
    timestamp: datetime
