#!/usr/bin/env sh
set -e

if [ -z "${DATABASE_URL}" ] && [ "${USE_SQLITE}" != "1" ]; then
  echo "[backend] ensuring database ${POSTGRES_DB:-ehrdb} exists"
  python <<'PY'
import os
import sys

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

user = os.getenv("POSTGRES_USER", "ehr")
password = os.getenv("POSTGRES_PASSWORD", "ehrpw")
host = os.getenv("POSTGRES_HOST", "postgres")
port = os.getenv("POSTGRES_PORT", "5432")
database = os.getenv("POSTGRES_DB", "ehrdb")

try:
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
except psycopg2.OperationalError as exc:
    print(f"[backend] failed to connect to postgres to ensure database exists: {exc}")
    sys.exit(1)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
with conn.cursor() as cur:
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database,))
    if cur.fetchone():
        print(f"[backend] database {database} already present")
    else:
        cur.execute(sql.SQL("CREATE DATABASE {}" ).format(sql.Identifier(database)))
        print(f"[backend] created database {database}")
conn.close()
PY
fi

echo "[backend] running migrations"
alembic upgrade head

echo "[backend] starting flask"
exec flask --app app:create_app run --host=0.0.0.0 --port=5000
