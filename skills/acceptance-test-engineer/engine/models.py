"""Shared dataclass schema for the acceptance-test-engineer engine."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RequirementSentence:
    index: int
    text: str
    source_line: int


@dataclass
class TestabilityFlag:
    pattern_id: str
    category: str  # "vague-term" | "weak-modal" | "unstated-signal"
    severity: str  # "low" | "medium" | "high"
    sentence_index: int | None  # None for whole-document absence checks
    description: str
    matched_text: str


@dataclass
class RequirementStats:
    sentence_count: int
    word_count: int
    vague_term_count: int
    weak_modal_count: int
    numeric_quantifier_count: int
    existing_criteria_markers: int


@dataclass
class RequirementContext:
    raw_text: str
    sentences: list[RequirementSentence] = field(default_factory=list)


@dataclass
class AcceptanceTestabilityReport:
    """The deterministic pre-review packet handed to the agent's
    acceptance-test-derivation workflow (SKILL.md Step 3)."""

    stats: RequirementStats
    testability_flags: list[TestabilityFlag]
    sentences: list[RequirementSentence]
    warnings: list[str] = field(default_factory=list)
