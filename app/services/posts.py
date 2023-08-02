from pydantic import PositiveInt

from app import models
from app.services.db_connect import get_db_conn


async def create_post(
        cmd: models.CreatePostCommand,
        user_id: PositiveInt
) -> models.Post:
    q = """
        INSERT INTO posts(
            user_id,
            title,
            "text"
        )
            VALUES (
                %(user_id)s,
                %(title)s,
                %(text)s
            )
        RETURNING 
            id, 
            user_id,
            (SELECT username FROM users WHERE id = %(user_id)s) AS author,
            title,
            "text",
            created_at,
            updated_at;
    """
    params = cmd.model_dump()
    params.update(user_id=user_id)
    async with get_db_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            row = await cur.fetchone()
            post = models.Post.from_iterable(row)
            return post


async def get_all_posts() -> list[models.PostWithReactions]:
    q = """
        WITH reactions AS (
            SELECT 
                post_id,
                "like",
                count(*) 
            FROM likes
            WHERE "like" IS NOT NULL 
            GROUP BY post_id, "like"
        )
        SELECT
            p.id, 
            p.user_id,
            u.username AS author,
            p.title,
            p."text",
            p.created_at,
            p.updated_at,
            COALESCE((SELECT count FROM reactions AS r WHERE r.post_id = p.id AND r."like" IS true), 0) AS likes,
            COALESCE((SELECT count FROM reactions AS r WHERE r.post_id = p.id AND r."like" IS false), 0) AS dislikes
        FROM posts AS p
            JOIN users AS u ON p.user_id = u.id;	
"""
    async with get_db_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q)
            rows = await cur.fetchall()
            if rows:
                posts = [models.PostWithReactions.from_iterable(row) for row in rows]
                return posts
            else:
                raise models.PostNotFound


async def delete_post(
        cmd: models.DeletePostCommand,
) -> models.Post:
    q = """
        DELETE FROM posts 
        WHERE id = %(post_id)s
            AND user_id = %(user_id)s
        RETURNING
            id, 
            user_id,
            (SELECT username FROM users WHERE id = %(user_id)s) AS author,
            title,
            "text",
            created_at,
            updated_at;
    """
    async with get_db_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, cmd.model_dump())
            row = await cur.fetchone()
            if row:
                post = models.Post.from_iterable(row)
                return post
            else:
                raise models.PostNotFound


async def update_post(
        cmd: models.UpdatePostCommand
) -> models.Post:
    q = """
        UPDATE posts
            SET title = COALESCE(%(title)s, title),
                text = COALESCE(%(text)s, text),
                updated_at = now()
            WHERE id = %(post_id)s
                AND user_id = %(user_id)s
        RETURNING
            id, 
            user_id,
            (SELECT username FROM users WHERE id = %(user_id)s) AS author,
            title,
            "text",
            created_at,
            updated_at;        
    """
    async with get_db_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, cmd.model_dump())
            row = await cur.fetchone()
            if row:
                post = models.Post.from_iterable(row)
                return post
            else:
                raise models.PostNotFound


async def get_post_by_id(query: models.GetPostQuery):
    q = """
        WITH reactions AS (
            SELECT 
                "like" ,
                count(*) 
            FROM likes
            WHERE "like" IS NOT NULL 
                AND post_id = %(post_id)s
            GROUP BY "like"
        )
        SELECT
            p.id, 
            p.user_id,
            u.username AS author,
            p.title,
            p."text",
            p.created_at,
            p.updated_at,
            COALESCE((SELECT count FROM reactions AS r WHERE r."like" IS true), 0) AS likes,
            COALESCE((SELECT count FROM reactions AS r WHERE r."like" IS false), 0) AS dislikes
        FROM posts AS p
            JOIN users AS u ON p.user_id = u.id
        WHERE p.id = %(post_id)s;	
    """
    async with get_db_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, query.model_dump())
            row = await cur.fetchone()
            if row:
                post = models.PostWithReactions.from_iterable(row)
                return post
            else:
                raise models.PostNotFound


async def get_posts_by_user_id(query: models.GetPostsByUserQuery):
    q = """
        WITH reactions AS (
            SELECT 
                post_id,
                "like",
                count(*) 
            FROM likes
            WHERE "like" IS NOT NULL 
            GROUP BY post_id, "like"
        )
        SELECT
            p.id, 
            p.user_id,
            u.username AS author,
            p.title,
            p."text",
            p.created_at,
            p.updated_at,
            COALESCE((SELECT count FROM reactions AS r WHERE r.post_id = p.id AND r."like" IS true), 0) AS likes,
            COALESCE((SELECT count FROM reactions AS r WHERE r.post_id = p.id AND r."like" IS false), 0) AS dislikes
        FROM posts AS p
            JOIN users AS u ON p.user_id = u.id
        WHERE p.user_id = %(user_id)s;	
    """
    async with get_db_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, query.model_dump())
            rows = await cur.fetchall()
            if rows:
                posts = [models.PostWithReactions.from_iterable(row) for row in rows]
                return posts
            else:
                raise models.PostNotFound
