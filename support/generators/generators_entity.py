import random
from dataclasses import fields
from typing import Any, TypeVar

from models.todo import ToDo
from support.entities_factory import EntitiesFactory
from support.generators.generators_string import GeneratorsString

T = TypeVar('T')


class GeneratorsEntity:
    @staticmethod
    def generate_entity_with_random_data(type: Any) -> Any:
        data = {}
        for field in fields(type):
            if field.type is bool:
                data[field.name] = random.choice([True, False])
            elif field.type is int:
                data[field.name] = random.randint(-1000000, 1000000)
            elif field.type is float:
                data[field.name] = round(random.uniform(-1000000.0, 1000000000.0), 3)
            elif field.type is str:
                data[field.name] = GeneratorsString.generate_random_string()
            else:
                raise ValueError(f'Unsupported type: {field.type}')
        return type(**data)

        id = random.randint(0, 1000000000)
        text = GeneratorsString.generate_random_string()
        completed = random.choice([True, False])
        return EntitiesFactory.create_entity(type=type, id=id, text=text, completed=completed)

    @staticmethod
    def generate_entities_with_random_data(todo_count: int) -> list[ToDo]:
        return [GeneratorsEntity.generate_entity_with_random_data(type=ToDo) for _ in range(todo_count)]
