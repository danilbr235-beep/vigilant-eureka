#!/usr/bin/env sh
set -eu

MODE="${1:-all}"

if command -v git >/dev/null 2>&1; then
  ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  if [ -n "${ROOT}" ]; then
    cd "${ROOT}"
  fi
fi

if [ ! -f "./docker-compose.yml" ]; then
  echo "Repository root not detected (docker-compose.yml not found)."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required but not found in PATH."
  exit 1
fi

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
