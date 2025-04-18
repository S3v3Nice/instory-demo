-include .env
export

setup:
	sh bin/setup

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

build:
	docker compose build

makemigrations:
	sh bin/makemigrations

migrate:
	sh bin/migrate
