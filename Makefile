-include .env
export

setup:
	sh bin/setup

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build
