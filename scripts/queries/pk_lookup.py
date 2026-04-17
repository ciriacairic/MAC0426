QUERIES = [
    {
        "name": "posts_score_range",
        "sql": {
            "postgresql": {
                "default":  'SELECT "Id", "Title", "Score" FROM public."Posts" WHERE "Score" BETWEEN 10 AND 100 ORDER BY "Score" DESC',
                "fulltext": 'SELECT "Id", "Title" FROM public."Posts" WHERE to_tsvector(\'english\', "Body") @@ to_tsquery(\'english\', \'python & programming\')',
            },
            "mysql": {
                "default":  "SELECT Id, Title, Score FROM Posts WHERE Score BETWEEN 10 AND 100 ORDER BY Score DESC",
                "fulltext": "SELECT Id, Title FROM Posts WHERE MATCH(Body) AGAINST('python programming' IN BOOLEAN MODE)",
            },
        },
    },
]
