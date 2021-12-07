from dataclasses import dataclass


@dataclass(frozen=True)
class SortKey:
    id: str
    label: str
