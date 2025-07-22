from dataclasses import dataclass


@dataclass
class CredsUsernamePassword:
    username: str
    password: str
