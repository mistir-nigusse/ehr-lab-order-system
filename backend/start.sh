#!/usr/bin/env sh
set -e

PORT_TO_USE=${PORT:-5000}

echo "[backend] running migrations"
alembic upgrade head

echo "[backend] starting gunicorn on port ${PORT_TO_USE}"
exec gunicorn -b 0.0.0.0:${PORT_TO_USE} -w ${WEB_CONCURRENCY:-2} 'app:create_app()'
