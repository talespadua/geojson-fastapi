BUILD_IMAGE_NAME=project
DOCKER_COMP_EXEC_CMD=docker-compose exec -T $(BUILD_IMAGE_NAME)

env/raise:
	$(info Raising Infrastructure)
	docker-compose up -d --build

env/shutdown:
	$(info Shutting down Infrastructure)
	docker-compose down

env/db/seed:
	$(info seeding database)
	$(DOCKER_COMP_EXEC_CMD) python scripts/seed_db.py

env/db/drop:
	$(info dropping db)
	$(DOCKER_COMP_EXEC_CMD) python scripts/drop_db.py

test:
	$(DOCKER_COMP_EXEC_CMD) python -m pytest --cov=project test/

mypy:
	$(DOCKER_COMP_EXEC_CMD) python -m mypy .

test-single:
	$(DOCKER_COMP_EXEC_CMD) python -m pytest $(test)

black:
	$(DOCKER_COMP_EXEC_CMD) black --check ./test ./project

flake8:
	$(DOCKER_COMP_EXEC_CMD) flake8 ./project --max-line-length=88

pipeline/qa:
	make mypy
	make black
	make flake8
	make test

shell:
	$(info Connecting container)
	$(DOCKER_COMP_EXEC_CMD) /bin/sh

make-migration:
	$(DOCKER_COMP_EXEC_CMD) alembic revision --autogenerate -m "$(description)"

.PHONY: test lint