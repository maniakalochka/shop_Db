#!/bin/sh
set -e

echo "Running Alembic migrations..."
alembic -c alembic.ini upgrade head

echo "Starting application..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload