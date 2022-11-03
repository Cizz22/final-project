worker.start: ## Start worker in its docker container
		docker-compose up worker

worker.daemon: ## Start daemon worker in its docker container
		docker-compose up -d worker

worker.logs: ## Display worker logs
		tail -f celery.log

worker.bash: ## Connect to worker to lauch commands
		docker-compose exec worker bash

worker.install: ## Install worker with its dependencies
		docker-compose run --rm worker pip install -r requirements.txt --user --upgrade --no-warn-script-location