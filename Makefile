.PHONY: up
up:
	@docker compose --profile app up --build -d


.PHONY: tests
tests:
	@docker compose --profile tests up --build -d

.PHONY: down
down:
	@docker-compose down 


.PHONY: start
start:
	@poetry run uvicorn app.main:app --reload