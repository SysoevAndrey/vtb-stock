from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    id: str
    label: str
    image: str
    path: str

    sub_categories: list["Category"]
