### TEST
# ¯¯¯¯¯¯¯¯


.PHONY: test
test: ## Launch tests in their own docker container
	docker-compose run --rm testserver

.PHONY: coverage
test.coverage: ## Generate test coverage
	docker-compose run --rm testserver bash -c "python -m pytest --cov-report term --cov-report html:coverage --cov-config setup.cfg --cov=src/ test/"

