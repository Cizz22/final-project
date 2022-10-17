### DATABASE
# ¯¯¯¯¯¯¯¯


database.connect: ## Connect to database
	docker-compose exec db psql -Upostgres

database.migrate: ## Create alembic migration file
	docker-compose run --rm server python -m flask db migrate

database.upgrade: ## Upgrade to latest migration
	docker-compose run --rm server python -m flask db upgrade

database.downgrade: ## Downgrade latest migration
	docker-compose run --rm server python src/manage.py db downgrade
