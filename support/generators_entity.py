import random

from models.todo import ToDo
from support.entities_factory import EntitiesFactory
from support.generators_string import GeneratorsString


class GeneratorEntities:
    @staticmethod
    def generate_entity_with_random_data(type: ToDo) -> ToDo:
        id = random.randint(0, 1000000000)
        text = GeneratorsString.generate_random_string()
        completed = random.choice([True, False])
        return EntitiesFactory.create_entity(type=type, id=id, text=text, completed=completed)

    @staticmethod
    def generate_entities_with_random_data(todo_count: int) -> list[ToDo]:
        return [GeneratorEntities.generate_entity_with_random_data(type=ToDo) for _ in range(todo_count)]
