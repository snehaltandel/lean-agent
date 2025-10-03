"""Application configuration utilities for the Lean Concepts Agent."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    openai_api_key: Optional[str] = Field(
        default=None,
        description="API key used to authenticate against the OpenAI API.",
    )
    database_url: Optional[str] = Field(
        default=None,
        description="Connection string for the Postgres + pgvector instance.",
    )
    tracing_endpoint: Optional[str] = Field(
        default=None,
        description="Destination for LangSmith or OpenTelemetry traces.",
    )
    prompt_dir: Path = Field(
        default=Path("prompts"),
        description="Base directory where prompt templates are stored.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()  # type: ignore[arg-type]
