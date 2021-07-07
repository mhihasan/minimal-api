.PHONY: setup_test
setup_test:
	docker-compose up -d

.PHONY: test
test: setup_test
	pytest -x

.PHONY: install
install:
	pip install -Ur requirements/dev.txt
