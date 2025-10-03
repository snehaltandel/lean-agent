"""Implementation of the WasteDetector tool for Lean waste identification."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from pydantic import BaseModel, Field

from .base import BaseTool

TIMWOODS_CATEGORIES: Dict[str, List[str]] = {
    "transportation": ["transport", "move", "shipment", "handoff"],
    "inventory": ["inventory", "stock", "warehouse", "backlog"],
    "motion": ["motion", "walk", "travel", "reach"],
    "waiting": ["waiting", "delay", "idle", "queue"],
    "overproduction": ["overproduce", "excess", "too many"],
    "overprocessing": ["rework", "duplicate", "overprocess", "manual"],
    "defects": ["defect", "error", "scrap", "bug"],
    "skills": ["skill", "underutilized", "talent", "expertise"],
}


class WasteDetectorInput(BaseModel):
    """Input schema for the WasteDetector tool."""

    process_description: str = Field(..., description="Narrative of the process to analyse.")
    metrics: Dict[str, float] | None = Field(
        default=None,
        description="Optional key metrics such as cycle time or defect rate.",
    )


class WasteInsight(BaseModel):
    """Structured description of a detected waste instance."""

    category: str = Field(..., description="TIMWOODS waste category.")
    supporting_evidence: str = Field(..., description="Excerpt from the process description.")
    recommended_action: str = Field(..., description="Suggested quick win countermeasure.")


class WasteDetectorOutput(BaseModel):
    """Output schema for the WasteDetector tool."""

    wastes: List[WasteInsight] = Field(
        default_factory=list,
        description="Detected wastes grouped by TIMWOODS categories.",
    )
    summary: str = Field(..., description="Narrative summary of quick win opportunities.")


class WasteDetector(BaseTool[WasteDetectorInput, WasteDetectorOutput]):
    """Rule-based Lean waste detector suitable for quick prototyping."""

    name = "waste_detector"
    description = "Identify Lean wastes from process narratives using TIMWOODS keywords."
    input_schema = WasteDetectorInput
    output_schema = WasteDetectorOutput

    action_templates: Dict[str, str] = {
        "transportation": "Streamline handoffs or co-locate teams to reduce movement.",
        "inventory": "Right-size batch sizes and introduce pull signals to cut inventory.",
        "motion": "Rearrange workspace to minimise unnecessary motion.",
        "waiting": "Balance workloads or add cross-training to shrink wait times.",
        "overproduction": "Adopt pull-based scheduling to match demand.",
        "overprocessing": "Standardise work and remove redundant steps.",
        "defects": "Implement root-cause analysis and mistake-proofing.",
        "skills": "Provide upskilling or redesign roles to leverage talent.",
    }

    def _run(self, parsed_input: WasteDetectorInput) -> WasteDetectorOutput:
        description = parsed_input.process_description.lower()
        detected: Dict[str, List[str]] = defaultdict(list)

        for category, keywords in TIMWOODS_CATEGORIES.items():
            for keyword in keywords:
                if keyword in description:
                    detected[category].append(keyword)

        wastes: List[WasteInsight] = []
        for category, evidence in detected.items():
            snippet = ", ".join(sorted(set(evidence)))
            action = self.action_templates.get(
                category,
                "Run a rapid Kaizen event to identify the best countermeasure.",
            )
            wastes.append(
                WasteInsight(
                    category=category,
                    supporting_evidence=f"Keywords identified: {snippet}.",
                    recommended_action=action,
                )
            )

        if wastes:
            summary = (
                "Detected potential wastes across the process. Prioritise the listed "
                "improvement opportunities to achieve immediate impact."
            )
        else:
            summary = (
                "No obvious wastes detected using the lightweight heuristic. Consider "
                "collecting more data for deeper analysis."
            )

        return WasteDetectorOutput(wastes=wastes, summary=summary)
