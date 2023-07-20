.PHONY: up
up:
	@docker-compose up --build -d


.PHONY: down
down:
	@docker-compose down 


.PHONY: start
start:
	@poetry run uvicorn app.main:app --reload