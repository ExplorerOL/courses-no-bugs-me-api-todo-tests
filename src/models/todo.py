from dataclasses import dataclass


@dataclass
class ToDo:
    id: int
    text: str
    completed: bool
