"""Lightweight subset of the Pydantic API for offline execution."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

__all__ = ["BaseModel", "Field"]


@dataclass
class FieldInfo:
    default: Any = ...
    default_factory: Optional[Any] = None
    description: Optional[str] = None


def Field(
    default: Any = ...,
    *,
    default_factory: Any | None = None,
    description: str | None = None,
) -> FieldInfo:
    return FieldInfo(default=default, default_factory=default_factory, description=description)


class BaseModelMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        annotations = namespace.get("__annotations__", {})
        fields: Dict[str, FieldInfo] = {}
        for base in bases:
            if hasattr(base, "__fields__"):
                fields.update(base.__fields__)  # type: ignore[attr-defined]
        for field_name, annotation in annotations.items():
            value = namespace.get(field_name, ...)
            if isinstance(value, FieldInfo):
                field_info = value
            else:
                field_info = Field(default=value)
            fields[field_name] = field_info
        namespace["__fields__"] = fields
        return super().__new__(mcls, name, bases, namespace)


class BaseModel(metaclass=BaseModelMeta):
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any) -> None:
        values = self.__class__._validate_dict(data)
        for key, value in values.items():
            setattr(self, key, value)

    @classmethod
    def _validate_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        values: Dict[str, Any] = {}
        for field_name, info in cls.__fields__.items():  # type: ignore[attr-defined]
            if field_name in data:
                values[field_name] = data[field_name]
            else:
                if info.default is not ...:
                    values[field_name] = info.default
                elif info.default_factory is not None:
                    values[field_name] = info.default_factory()
                else:
                    raise ValueError(f"Missing required field '{field_name}'")
        return values

    @classmethod
    def model_validate(cls, data: Dict[str, Any]) -> "BaseModel":
        values = cls._validate_dict(data)
        instance = cls.__new__(cls)
        for key, value in values.items():
            setattr(instance, key, value)
        return instance

    def model_dump(self) -> Dict[str, Any]:
        def _dump(value: Any) -> Any:
            if isinstance(value, BaseModel):
                return value.model_dump()
            if isinstance(value, list):
                return [_dump(item) for item in value]
            if isinstance(value, dict):
                return {key: _dump(item) for key, item in value.items()}
            return value

        return {field_name: _dump(getattr(self, field_name)) for field_name in self.__fields__}  # type: ignore[attr-defined]
