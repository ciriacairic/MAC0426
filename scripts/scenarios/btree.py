SETUP = {
    "postgresql": [
        'CREATE INDEX IF NOT EXISTS btree_posts_score   ON public."Posts"    USING btree ("Score")',
        'CREATE INDEX IF NOT EXISTS btree_posts_owner   ON public."Posts"    USING btree ("OwnerUserId")',
        'CREATE INDEX IF NOT EXISTS btree_posts_type    ON public."Posts"    USING btree ("PostTypeId")',
        'CREATE INDEX IF NOT EXISTS btree_posts_created ON public."Posts"    USING btree ("CreationDate")',
        'CREATE INDEX IF NOT EXISTS btree_users_rep     ON public."Users"    USING btree ("Reputation")',
        'CREATE INDEX IF NOT EXISTS btree_comments_post ON public."Comments" USING btree ("PostId")',
        'CREATE INDEX IF NOT EXISTS btree_votes_post    ON public."Votes"    USING btree ("PostId")',
    ],
    "mysql": [
        "CREATE INDEX btree_posts_score   ON Posts    (Score)",
        "CREATE INDEX btree_posts_owner   ON Posts    (OwnerUserId)",
        "CREATE INDEX btree_posts_type    ON Posts    (PostTypeId)",
        "CREATE INDEX btree_posts_created ON Posts    (CreationDate)",
        "CREATE INDEX btree_users_rep     ON Users    (Reputation)",
        "CREATE INDEX btree_comments_post ON Comments (PostId)",
        "CREATE INDEX btree_votes_post    ON Votes    (PostId)",
    ],
}

TEARDOWN = {
    "postgresql": [
        "DROP INDEX IF EXISTS btree_posts_score",
        "DROP INDEX IF EXISTS btree_posts_owner",
        "DROP INDEX IF EXISTS btree_posts_type",
        "DROP INDEX IF EXISTS btree_posts_created",
        "DROP INDEX IF EXISTS btree_users_rep",
        "DROP INDEX IF EXISTS btree_comments_post",
        "DROP INDEX IF EXISTS btree_votes_post",
    ],
    "mysql": [
        "DROP INDEX btree_posts_score   ON Posts",
        "DROP INDEX btree_posts_owner   ON Posts",
        "DROP INDEX btree_posts_type    ON Posts",
        "DROP INDEX btree_posts_created ON Posts",
        "DROP INDEX btree_users_rep     ON Users",
        "DROP INDEX btree_comments_post ON Comments",
        "DROP INDEX btree_votes_post    ON Votes",
    ],
}
