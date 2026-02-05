SHELL := /bin/bash

.PHONY: up down logs ps clean smoke demo precheck package

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

clean:
	rm -rf data/raw/* data/staging/* data/curated/* data/quarantine/*

smoke:
	docker compose exec -T airflow /opt/scripts/smoke_check.sh

demo:
	chmod +x scripts/demo_run.sh
	./scripts/demo_run.sh

precheck:
	chmod +x scripts/pre_submission_check.sh
	./scripts/pre_submission_check.sh

package:
	chmod +x scripts/package_submission.sh
	./scripts/package_submission.sh
