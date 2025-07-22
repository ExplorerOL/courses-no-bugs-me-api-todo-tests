import random

from models.todo import ToDo
from support.generators_string import GeneratorsString


class GeneratorsToDo:
    @staticmethod
    def generate_todo_with_random_data() -> ToDo:
        id = random.randint(0, 1000000000)
        text = GeneratorsString.generate_random_string()
        completed = random.choice([True, False])
        return ToDo(id=id, text=text, completed=completed)

    @staticmethod
    def generate_todos_with_random_data(todo_count: int) -> list[ToDo]:
        return [GeneratorsToDo.generate_todo_with_random_data() for _ in range(todo_count)]
