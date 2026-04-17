.DEFAULT_GOAL := help
.PHONY: help check check-api check-web

help:
	@echo "Targets:"
	@echo "  make check      - run docker checks (MODE=all by default)"
	@echo "  make check MODE=api"
	@echo "  make check MODE=web"
	@echo "  make check-api  - run only api checks in docker"
	@echo "  make check-web  - run only web build in docker"

MODE ?= all

check:
	./scripts/check-in-docker.sh $(MODE)

check-api:
	./scripts/check-in-docker.sh api

check-web:
	./scripts/check-in-docker.sh web
