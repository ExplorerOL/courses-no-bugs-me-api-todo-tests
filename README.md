
# Запуск тестов на Windows с использованием uv
## Установка uv глобально
```
python -m pip install uv
```
Добавить в переменную окружения Path путь к uv. При глобальной установке uv будет находиться в C:\Users\sea4833\AppData\Local\Programs\Python\Python311\Scripts


## Склонировать репозиторий
```
git clone https://github.com/ExplorerOL/courses-no-bugs-me-todo-tests.git
```

## Запуск тестов
```
cd <путь к директории проекта>
python -m uv run pytest
```
При запуске тестов автоматически создастся виртуальное окружение и будут установлены зависимости

### Форматирование и линтинг кода тестов
```
uv run ruff format; uv run ruff check --fix;
```