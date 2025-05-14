.DEFAULT_GOAL := help

HOST ?= localhost
PORT ?= 8005

run:
	poetry run uvicorn main:app --host $(HOST) --port $(PORT) --reload

install:
	@echo "Подтягиваем зависимость $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall:
	@echo "Удаляем зависимость $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MESSAGE)

migrate-apply:
	alembic upgrade head
