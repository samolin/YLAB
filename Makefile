.PHONY: up
up:
	@docker compose --profile app up --build


.PHONY: tests
tests:
	@docker compose --profile tests up --build -d

.PHONY: down
down:
	@docker compose --profile app down


.PHONY: tests-down
tests-down:
	@docker compose --profile tests down


# .PHONY: up
# up:
# 	@docker compose --profile app start
