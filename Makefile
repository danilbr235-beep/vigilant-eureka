.PHONY: help check check-api check-web

help:
	@echo "Targets:"
	@echo "  make check      - run api+web checks in docker"
	@echo "  make check-api  - run only api checks in docker"
	@echo "  make check-web  - run only web build in docker"

check:
	./scripts/check-in-docker.sh all

check-api:
	./scripts/check-in-docker.sh api

check-web:
	./scripts/check-in-docker.sh web
