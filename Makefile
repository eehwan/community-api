shell:
	docker compose exec api bash

shell-redis:
	docker compose exec redis redis-cli

shell-postgres:
	docker compose exec postgres psql -U developer -d developer

build: clean
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

clean:
	docker compose down -v --remove-orphans
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

logs:
	docker compose logs -f