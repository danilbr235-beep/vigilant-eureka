#!/usr/bin/env sh
set -eu

MODE="${1:-all}"

run_api() {
  echo "==> Running API tests in docker"
  docker run --rm \
    -v "$PWD/apps/api:/app" \
    -w /app \
    python:3.11-slim \
    sh -lc "pip install -e . && pytest -q"
}

run_web() {
  echo "==> Running Web build in docker"
  docker run --rm \
    -v "$PWD/apps/web:/app" \
    -w /app \
    node:20-alpine \
    sh -lc "npm install && npm run build"
}

case "$MODE" in
  api)
    run_api
    ;;
  web)
    run_web
    ;;
  all)
    run_api
    run_web
    ;;
  *)
    echo "Usage: $0 [api|web|all]"
    exit 1
    ;;
esac
