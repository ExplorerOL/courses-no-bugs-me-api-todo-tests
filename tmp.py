from dataclasses import dataclass

from support.generators.generators_entity import GeneratorsEntity


@dataclass
class RandomData:
    # name: str
    age: int
    email: str
    is_active: bool
    balance: float
    # i: UUID


# print(str(fields(RandomData)) + '\n')
# for field in fields(RandomData):
#     print(str(field) + '\n')

# print('---------------------')
# for field in fields(RandomData):
#     print(str(field.name) + '\n')

entity = GeneratorsEntity.generate_entity_with_random_data(entity_type=RandomData)
print(f'{entity!r}')

# todo = GeneratorsEntity.generate_entity_with_random_data(type=ToDo)
# print(f'{todo!r}')
