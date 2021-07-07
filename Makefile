.PHONY: setup_test
setup_test:
	docker-compose -f docker-compose-test.yml up -d

.PHONY: test
test: setup_test
	pytest -x
	docker-compose -f docker-compose-test.yml down

.PHONY: install
install:
	pip install -Ur requirements/dev.txt

.PHONY: run_dev
dev:
	docker-compose -f docker-compose-dev.yml up --build --force-recreate
