"""Common utilities for defining Lean Concepts Agent tools."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel

InputSchema = TypeVar("InputSchema", bound=BaseModel)
OutputSchema = TypeVar("OutputSchema", bound=BaseModel)


class ToolExecutionError(RuntimeError):
    """Raised when a tool fails to generate a valid response."""


class BaseTool(ABC, Generic[InputSchema, OutputSchema]):
    """Abstract base class that all tools must inherit from."""

    name: str
    description: str
    input_schema: Type[InputSchema]
    output_schema: Type[OutputSchema]

    def parse_input(self, data: Dict[str, Any]) -> InputSchema:
        """Validate raw input data against the tool's input schema."""

        return self.input_schema.model_validate(data)

    @abstractmethod
    def _run(self, parsed_input: InputSchema) -> OutputSchema:
        """Execute the tool and return the validated output."""

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with validated input and output schemas."""

        parsed_input = self.parse_input(data)
        result = self._run(parsed_input)
        return result.model_dump()
