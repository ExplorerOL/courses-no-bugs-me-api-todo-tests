from dataclasses import dataclass


@dataclass
class CredsUsernamePassword:
    username: str
    password: str


@dataclass
class ToDo:
    id: int
    text: str
    completed: bool
