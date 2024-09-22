format:
	poetry run ruff format .

lint-fix:
	poetry run ruff check . --fix

test:
	poetry run pytest .

pretty:
	make format
	make lint-fix

install:
	poetry install --no-root

up:
	poetry run python main.py