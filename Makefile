.PHONY: check check-api check-web

check:
	./scripts/check-in-docker.sh all

check-api:
	./scripts/check-in-docker.sh api

check-web:
	./scripts/check-in-docker.sh web
