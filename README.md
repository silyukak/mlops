# Учебный проект MLOps

uv управляет зависимостями и окружением, Ruff проверяет и форматирует код,
ty проверяет типы. Настройки находятся в `pyproject.toml`.
Все команды выполняются из корня репозитория в терминале WSL.

## Подготовка окружения

Для существующего проекта после клонирования:

```bash
uv sync --locked
```

Создаёт `.venv`, если его нет, и устанавливает зависимости, включая группу
`dev`. Флаг `--locked` запрещает изменение `uv.lock`: если он не соответствует
`pyproject.toml`, команда сообщит об ошибке.

После ручного изменения зависимостей в `pyproject.toml`:

```bash
uv sync
```

Это обновит lock-файл и окружение. Изменение только настроек Ruff или ty
не требует синхронизации зависимостей.

Для создания нового проекта, справочно:

```bash
uv init
uv venv
```

`uv venv` создаёт только окружение. Отдельно запускать его необязательно:
`uv sync` и `uv run` также умеют создавать окружение проекта.

## Запуск программы

```bash
uv run python src/mlops/main.py
```

Скрипт обращается к NASA EONET и сохраняет данные в `data/wildfires.csv`.
Для запроса нужен доступ к интернету.

Команда `uv run mlops` пока вызывает функцию из `src/mlops/__init__.py`
и печатает приветствие. Её назначение задано в `[project.scripts]`.

## Проверки и исправления

Проверить проект без изменения исходников:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
```

Исправить доступные нарушения линтера, затем отформатировать код:

```bash
uv run ruff check . --fix
uv run ruff format .
```

`check --fix` исправляет поддерживаемые нарушения правил, включая порядок
импортов. `format` приводит отступы, кавычки и переносы к единому стилю.
Оставшиеся сообщения нужно разобрать вручную, затем повторить проверки.

Дополнительные команды:

```bash
uv run ruff rule I001     # Объяснение конкретного правила Ruff
uv run ty check --watch   # Перепроверять типы при изменении файлов; выход — Ctrl+C
uv run pytest            # Запустить тесты, когда они появятся
```

Сейчас тестов нет; pytest в таком случае завершится с кодом 5.

## Управление зависимостями

Примеры команд, которые изменяют зависимости:

```bash
uv add requests pandas       # Добавить библиотеки для работы программы
uv add --dev ruff ty pytest   # Добавить инструменты разработки
uv remove requests           # Удалить обычную зависимость
uv remove --dev pytest        # Удалить зависимость из группы dev
```

Удаление показано для справки: текущему скрипту нужен `requests`.
Сейчас Ruff и ty находятся в обычных зависимостях. Для переноса в `dev`
с сохранением текущих ограничений версий:

```bash
uv remove ruff ty
uv add --dev 'ruff>=0.17.0' 'ty>=0.0.86'
```

Обновить Ruff в пределах ограничений `pyproject.toml`:

```bash
uv lock --upgrade-package ruff
uv sync
```

Команда `uv lock` пересчитывает lock-файл без установки пакетов.
`pyproject.toml` описывает требования, `uv.lock` фиксирует выбранные версии,
`.venv` содержит установленное окружение. Lock-файл обновляет uv.

## Какие программы используются

```bash
uv --version
uv run python --version
uv run ruff --version
uv run ty --version

# Команды, доступные в текущем терминале
command -v ruff
command -v ty

# Пути к Python, Ruff и ty внутри окружения проекта
uv run python -c 'import sys, shutil; print(sys.executable); print(shutil.which("ruff")); print(shutil.which("ty"))'
```

Для `uv run` активировать окружение не требуется. Если нужно запускать
`python`, `ruff` и `ty` напрямую из `.venv`:

```bash
source .venv/bin/activate
deactivate  # Выйти из активированного окружения
```

Отдельные установки через `uv tool` управляются независимо от проекта:

```bash
uv tool list
uv tool upgrade ty
uv tool upgrade ruff
```

`uv tool upgrade` обновляет отдельную установку инструмента и не меняет
зависимости проекта. В VS Code путь к запущенной программе можно посмотреть
в панели «Вывод» (Output), выбрав канал Ruff или ty.

## Git

Перед коммитом выполнить проверки и просмотреть изменения:

```bash
git status
git diff
git add README.md pyproject.toml uv.lock .python-version .gitignore src/
git diff --cached
git commit -m "Настроить учебный проект"
```

В Git сохраняются исходники, настройки и `uv.lock`. Окружение `.venv`
и данные `data/` исключены через `.gitignore`.

## Справка

```bash
uv --help
uv add --help
uv run ruff check --help
uv run ty check --help
```

- [Работа с проектами uv](https://docs.astral.sh/uv/guides/projects/)
- [Отдельные инструменты uv tool](https://docs.astral.sh/uv/concepts/tools/)
- [Настройка Ruff](https://docs.astral.sh/ruff/configuration/)
- [Настройка ty](https://docs.astral.sh/ty/reference/configuration/)

Презентация лекции сделана с помощью Quarto и reveal.js.
