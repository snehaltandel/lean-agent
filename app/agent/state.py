"""Definitions for the LangGraph state used by the Lean Concepts Agent."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Representation of a tool invocation request."""

    tool_name: str = Field(..., description="Name of the tool to invoke.")
    arguments: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSON-serialisable arguments passed to the tool.",
    )


class AgentState(BaseModel):
    """Shared state flowing between LangGraph nodes."""

    user_goal: str = Field(..., description="Primary objective provided by the user.")
    mode: str = Field(
        "optimizer",
        description="Selected user mode. Either 'optimizer' or 'analyst'.",
    )
    conversation_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Chronological log of interactions and tool results.",
    )
    pending_tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="Queue of tool invocations produced by the planner node.",
    )
    final_response: Optional[str] = Field(
        default=None,
        description="Natural language answer returned to the client UI.",
    )

    class Config:
        arbitrary_types_allowed = True
