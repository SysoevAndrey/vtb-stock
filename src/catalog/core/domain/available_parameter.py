from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ParameterType(Enum):
    KEYWORD = "string"
    NUMBER = "number"


@dataclass(frozen=True)
class ParameterStats:
    minimum: float
    maximum: float
    average: float
    total_sum: float


@dataclass(frozen=True)
class AvailableValue:
    id: str
    label: str
    doc_count: str


@dataclass(frozen=True)
class AvailableParameter:
    id: str
    label: str
    type: ParameterType
    stats: Optional[ParameterStats]
    available_values: list[AvailableValue]
