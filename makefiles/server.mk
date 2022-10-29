### SERVER
# ¯¯¯¯¯¯¯¯¯¯¯

server.install: ## Install server with its dependencies
	docker-compose run --rm server pip install -r requirements.txt --user --upgrade --no-warn-script-location && docker-compose run --rm worker pip install -r requirements.txt --user --upgrade --no-warn-script-location

server.start: ## Start server in its docker container
	docker-compose up server

server.bash: ## Connect to server to lauch commands
	docker-compose exec server bash

server.daemon: ## Start daemon server in its docker container
	docker-compose up -d server

server.stop: ## Start server in its docker container
	docker-compose stop

server.storage: ## make storage file
	docker-compose run server bash -c "mkdir -p static/images"

server.logs: ## Display server logs
	tail -f server.log


