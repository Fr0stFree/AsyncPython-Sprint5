run:
	poetry run python src/main.py

test:
	poetry run pytest

makemigrations:
	poetry run alembic revision --autogenerate -m "$(m)"

migrate:
	poetry run alembic upgrade head

rollback:
	poetry run alembic downgrade -1
