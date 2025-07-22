from models.todo import ToDoBuilder

a = ToDoBuilder().set_id(1).set_text('test').build()
print(f'{a!r}')
