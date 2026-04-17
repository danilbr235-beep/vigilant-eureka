FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

RUN pip install --no-cache-dir -e .

EXPOSE 8000
