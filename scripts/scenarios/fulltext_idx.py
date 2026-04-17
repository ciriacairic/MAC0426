# PostgreSQL usa índice GIN sobre o tsvector pré-computado.
# MySQL usa índice FULLTEXT nativo.
# ATENÇÃO: CREATE FULLTEXT INDEX em tabelas grandes pode levar vários minutos.

SETUP = {
    "postgresql": [
        "CREATE INDEX IF NOT EXISTS gin_posts_body      ON public.\"Posts\" USING gin (to_tsvector('english', \"Body\"))",
        "CREATE INDEX IF NOT EXISTS gin_users_aboutme   ON public.\"Users\" USING gin (to_tsvector('english', \"AboutMe\"))",
    ],
    "mysql": [
        "CREATE FULLTEXT INDEX ft_posts_body    ON Posts (Body)",
        "CREATE FULLTEXT INDEX ft_users_aboutme ON Users (AboutMe)",
    ],
}

TEARDOWN = {
    "postgresql": [
        "DROP INDEX IF EXISTS gin_posts_body",
        "DROP INDEX IF EXISTS gin_users_aboutme",
    ],
    "mysql": [
        "DROP INDEX ft_posts_body    ON Posts",
        "DROP INDEX ft_users_aboutme ON Users",
    ],
}
