.DEFAULT_GOAL := help

HOST ?= localhost
PORT ?= 8004

run:
	poetry run uvicorn main:app --host $(HOST) --port $(PORT) --reload --env-file .local.env

install:
	@echo "Подтягиваем зависимость $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall:
	@echo "Удаляем зависимость $(LIBRARY)"
	poetry remove $(LIBRARY)