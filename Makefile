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
	docker compose down --remove-orphans
	sudo find . -name '*.pyc' -exec rm -f {} +
	sudo find . -name '*.pyo' -exec rm -f {} +
	sudo find . -name '*~' -exec rm -f {} +
	sudo find . -name '__pycache__' -exec rm -fr {} +

logs:
	docker compose logs -f

board-sync:
	docker compose run --rm api sh -c "./wait-for-it.sh postgres:5432; ./wait-for-it.sh redis:6379; python manage.py board syncwithredis"

session-stats:
	docker compose run --rm api sh -c "./wait-for-it.sh postgres:5432; python manage.py session stats"

session-cleanup:
	docker compose run --rm api sh -c "./wait-for-it.sh postgres:5432; python manage.py session cleanup"
