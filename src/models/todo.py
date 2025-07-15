from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ToDo:
    id: int
    text: str
    completed: bool
