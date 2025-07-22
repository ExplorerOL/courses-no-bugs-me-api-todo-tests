from dataclasses import dataclass
from typing import Callable


@dataclass
class Endpoint:
    enpoint: str
    version_or_get_version_func: str | Callable[..., str]

    def __str__(self) -> str:
        return f'{self.enpoint}{self.__get_version()}'

    def __get_version(self) -> str:
        if isinstance(self.version_or_get_version_func, Callable):
            return self.version_or_get_version_func()
        else:
            return self.version_or_get_version_func
