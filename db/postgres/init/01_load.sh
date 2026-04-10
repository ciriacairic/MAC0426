#!/bin/bash
set -e

echo "Patching and loading PostgreSQL script..."

sed 's/CREATE SCHEMA public;/CREATE SCHEMA IF NOT EXISTS public;/g' \
    /docker-scripts/postgresql_script_criacao_bd.sql | \
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --no-password

echo "PostgreSQL load complete."
