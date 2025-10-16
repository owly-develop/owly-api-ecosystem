# Makefile for OWLY CRM API

.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test clean backup

help:
	@echo "OWLY CRM API - Available Commands"
	@echo "=================================="
	@echo "make build         - Build Docker images"
	@echo "make up            - Start all services"
	@echo "make down          - Stop all services"
	@echo "make restart       - Restart all services"
	@echo "make logs          - View logs (all services)"
	@echo "make logs-web      - View web logs"
	@echo "make logs-celery   - View celery logs"
	@echo "make shell         - Open Django shell"
	@echo "make bash          - Open bash in web container"
	@echo "make migrate       - Run database migrations"
	@echo "make makemigrations - Create new migrations"
	@echo "make createsuperuser - Create superuser"
	@echo "make test          - Run tests"
	@echo "make test-coverage - Run tests with coverage"
	@echo "make seed          - Seed database with test data"
	@echo "make seed-clean    - Clear and seed database"
	@echo "make clean         - Remove all containers and volumes"
	@echo "make backup        - Backup database"
	@echo "make setup         - Initial setup (first time)"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "🌐 API: http://localhost:8000/api/"
	@echo "👤 Admin: http://localhost:8000/admin/"
	@echo "📚 Docs: http://localhost:8000/api/docs/"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-celery:
	docker-compose logs -f celery

shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web /bin/bash

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web python manage.py test

clean:
	docker-compose down -v
	@echo "✅ All containers and volumes removed"

backup:
	@./scripts/backup.sh

seed:
	docker-compose exec web python manage.py seed_data
	@echo "✅ Database seeded with test data"

seed-clean:
	docker-compose exec web python manage.py seed_data --clear
	@echo "✅ Database cleared and seeded"

setup:
	@echo "🚀 Setting up OWLY CRM API..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Using default values..."; \
	fi
	docker-compose up -d
	@echo "⏳ Waiting for services to start..."
	@sleep 10
	docker-compose exec web python manage.py migrate
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Create superuser: make createsuperuser"
	@echo "2. Visit: http://localhost:8000/admin/"
	@echo "3. API Docs: http://localhost:8000/api/docs/"

