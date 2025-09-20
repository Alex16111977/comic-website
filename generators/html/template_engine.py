"""Render journey pages using the shared template."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, TYPE_CHECKING

from .head_generator import HeadContext

if TYPE_CHECKING:  # pragma: no cover
    from generators.base import BaseGenerator


@dataclass
class TemplateContext:
    character: Dict[str, Any]
    phases: List[Dict[str, Any]]
    exercises: List[Dict[str, Any]]
    quizzes: List[Dict[str, Any]]
    quizzes_json: str
    head: HeadContext
    relations_metadata: Dict[str, Dict[str, bool]]
    js_bundle: str


class JourneyTemplateEngine:
    """Adapter around the base generator renderer."""

    def __init__(self, base_generator: "BaseGenerator") -> None:
        self.base_generator = base_generator

    def render(self, context: TemplateContext) -> str:
        return self.base_generator.render_template(
            "journey.html",
            character=context.character,
            journey_phases=context.phases,
            exercises=context.exercises,
            quizzes=context.quizzes,
            quizzes_json=context.quizzes_json,
            initial_description=context.head.initial_description,
            initial_progress=context.head.initial_progress,
            first_phase_title=context.head.first_phase_title,
            relations_metadata=context.relations_metadata,
            js=context.js_bundle,
        )
