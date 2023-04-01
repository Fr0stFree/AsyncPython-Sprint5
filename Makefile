init: migrate run

run:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8080

test:
	poetry run pytest

makemigrations:
	poetry run alembic revision --autogenerate -m "$(m)"

migrate:
	poetry run alembic upgrade head

rollback:
	poetry run alembic downgrade -1
