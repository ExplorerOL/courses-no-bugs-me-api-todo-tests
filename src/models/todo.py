from dataclasses import dataclass


@dataclass(slots=True)
class ToDo:
    id: int
    text: str
    completed: bool
