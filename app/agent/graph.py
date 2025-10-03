"""LangGraph orchestration skeleton for the Lean Concepts Agent."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from langgraph.graph import END, StateGraph

from app.config import get_settings
from app.tools import WasteDetector

from .state import AgentState

PROMPT_FILES = {
    "system": "system_v1.jinja",
    "planner": "planner_v1.jinja",
    "critic": "critic_v1.jinja",
    "finalizer": "finalizer_v1.jinja",
}


def _build_jinja_env() -> Environment:
    settings = get_settings()
    loader = FileSystemLoader(Path(settings.prompt_dir))
    return Environment(loader=loader, autoescape=select_autoescape(enabled_extensions=("jinja", "yaml")))


def load_prompt(name: str) -> str:
    env = _build_jinja_env()
    template_name = PROMPT_FILES[name]
    template = env.get_template(template_name)
    return template.render()


def build_graph() -> StateGraph:
    """Return a configured LangGraph state machine."""

    graph = StateGraph(AgentState)

    def planner(state: AgentState) -> AgentState:
        prompt = load_prompt("planner")
        _ = prompt
        state.pending_tool_calls.append(
            {
                "tool_name": WasteDetector.name,
                "arguments": {"process_description": state.user_goal},
            }
        )
        return state

    def tool_router(state: AgentState) -> AgentState:
        catalogue: Dict[str, WasteDetector] = {WasteDetector.name: WasteDetector()}
        next_calls = []
        for call in state.pending_tool_calls:
            tool = catalogue.get(call["tool_name"])
            if tool is None:
                continue
            result = tool.run(call["arguments"])
            state.conversation_history.append({"tool": call["tool_name"], "result": result})
        state.pending_tool_calls = next_calls
        return state

    def finalizer(state: AgentState) -> AgentState:
        prompt = load_prompt("finalizer")
        _ = prompt
        if state.conversation_history:
            last_tool = state.conversation_history[-1]
            summary = last_tool["result"].get("summary", "")
        else:
            summary = "No tools were executed."
        state.final_response = summary
        return state

    graph.add_node("planner", planner)
    graph.add_node("tool_router", tool_router)
    graph.add_node("finalizer", finalizer)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "tool_router")
    graph.add_edge("tool_router", "finalizer")
    graph.add_edge("finalizer", END)

    return graph
