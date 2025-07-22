from dataclasses import dataclass


@dataclass(slots=True)
class ToDo:
    id: int
    text: str = ''
    completed: bool = False


# Так как в python можно использовать именванные аргументы, то, думаю, нет смысла
# специально создавать отдельный билдер для ToDo


# class ToDoBuilder:
#     id: int
#     text: str | None = None
#     completed: bool | None = None

#     def set_id(self, id: int) -> Self:
#         self.id = id
#         return self

#     def set_text(self, text: str) -> Self:
#         self.text = text
#         return self

#     def set_completed(self, completed: bool) -> Self:
#         self.completed = completed
#         return self

#     def build(self) -> ToDo:
#         return ToDo(id=self.id, text=self.text, completed=self.completed)
