import psycopg2
import mysql.connector
from . import config


def connect_postgresql():
    conn = psycopg2.connect(
        host=config.PG_HOST,
        port=config.PG_PORT,
        user=config.PG_USER,
        password=config.PG_PASSWORD,
        dbname=config.PG_DB,
    )
    conn.autocommit = True
    return conn


def connect_mysql():
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB,
        autocommit=True,
    )
    return conn


CONNECTORS = {
    "postgresql": connect_postgresql,
    "mysql": connect_mysql,
}
