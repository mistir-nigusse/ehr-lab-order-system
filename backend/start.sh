#!/usr/bin/env sh
set -e

echo "[backend] running migrations"
alembic upgrade head

echo "[backend] starting flask"
exec flask --app app:create_app run --host=0.0.0.0 --port=5000
