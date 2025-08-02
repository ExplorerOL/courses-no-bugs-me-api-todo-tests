import random
from dataclasses import fields
from typing import Any, Generic, TypeVar

from support.generators.generators_string import GeneratorsString

T = TypeVar('T')


class GeneratorsEntity(Generic[T]):
    @staticmethod
    def generate_entity_with_random_data(entity_type: T) -> T:
        data = {}
        for field in fields(entity_type):
            if field.type is bool:
                data[field.name] = random.choice([True, False])
            elif field.type is int:
                if field.name == 'id':
                    data[field.name] = random.randint(1, 1000000)
                else:
                    data[field.name] = random.randint(-1000000, 1000000)
            elif field.type is float:
                data[field.name] = round(random.uniform(-1000000.0, 1000000000.0), 3)
            elif field.type is str:
                data[field.name] = GeneratorsString.generate_random_string()
            else:
                raise ValueError(f'Неподдерживаемый тип для генерации данных: {field.type!r}!')
        return entity_type(**data)

    @staticmethod
    def generate_entities_with_random_data(type: T, todo_count: int) -> list[Any]:
        return [GeneratorsEntity.generate_entity_with_random_data(entity_type=T) for _ in range(todo_count)]
