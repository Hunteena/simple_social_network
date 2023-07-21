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
            post = models.Post(**dict(
                zip(["id", "user_id", "title", "text", "created_at"], row)))
            return post
