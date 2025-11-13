SHELL := /bin/bash

# Try to use host UID for file permissions in Airflow containers
export AIRFLOW_UID := $(shell id -u 2>/dev/null || echo 50000)

.PHONY: up down logs web trigger ps init

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

web:
	@echo "Open Airflow UI at: http://localhost:8080 (user: admin / pass: admin)"

trigger:
	docker compose exec airflow-webserver airflow dags trigger batch_lakehouse_daily

ps:
	docker compose ps

init:
	docker compose up airflow-init
