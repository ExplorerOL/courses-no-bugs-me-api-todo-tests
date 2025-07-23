import enum

from models.todo import ToDo


class EntityTypes(enum.Enum):
    todo = ToDo


class EntitiesFactory:
    @staticmethod
    def create_entity(type: EntityTypes, **kwargs) -> ToDo:
        match type:
            case EntityTypes.todo.value:
                return ToDo(**kwargs)
            case _:
                raise ValueError(f'Генерация сущности {type!r} не реализована!')
