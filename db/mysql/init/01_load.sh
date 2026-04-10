#!/bin/bash
set -e

echo "Loading MySQL script..."

mysql -u root -p"$MYSQL_ROOT_PASSWORD" StackOverflow < /docker-scripts/mysql_script_criacao_bd.sql

echo "MySQL load complete."
