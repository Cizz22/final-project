### DATABASE
# ¯¯¯¯¯¯¯¯


database.connect: ## Connect to database
	docker-compose exec db psql -U user -d db

database.migrate: ## Create alembic migration file
	docker-compose run --rm server python -m flask db migrate

database.upgrade: ## Upgrade to latest migration
	docker-compose run --rm server python -m flask db upgrade

database.downgrade: ## Downgrade latest migration
	docker-compose run --rm server python -m flask db downgrade

database.seeder: ## Run database seeder
	docker-compose run --rm server python -m flask seeder 

database.drop: ## Drop database
	docker-compose run --rm server python -m flask drop
