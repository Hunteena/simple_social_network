from pydantic import PositiveInt

from app import models
from app.services.db_connect import postgres_connection


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
            title,
            "text",
            created_at;
    """
    params = cmd.model_dump()
    params.update(user_id=user_id)
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            row = await cur.fetchone()
            post = models.Post.from_iterable(row)
            return post


async def get_all_posts() -> list[models.Post]:
    q = """
        SELECT
            id, 
            user_id,
            title,
            "text",
            created_at,
            updated_at
        FROM posts;
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q)
            rows = await cur.fetchall()
            posts = [models.Post.from_iterable(row) for row in rows]
            return posts
