makemigrations:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1
