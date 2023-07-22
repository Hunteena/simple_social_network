from fastapi import HTTPException, status
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
            (SELECT username FROM users WHERE id = %(user_id)s) AS author,
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
            p.id, 
            u.username AS author,
            p.title,
            p."text",
            p.created_at,
            p.updated_at
        FROM posts AS p
            JOIN users AS u ON p.user_id = u.id ;	

    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q)
            rows = await cur.fetchall()
            posts = [models.Post.from_iterable(row) for row in rows]
            return posts


async def delete_post(
        cmd: models.DeletePostCommand,
) -> models.Post:
    q = """
        DELETE FROM posts 
        WHERE id = %(post_id)s
            AND user_id = %(user_id)s
        RETURNING
            id, 
            (SELECT username FROM users WHERE id = %(user_id)s) AS author,
            title,
            "text",
            created_at,
            updated_at;
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, cmd.model_dump())
            row = await cur.fetchone()
            if row:
                post = models.Post.from_iterable(row)
                return post
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )


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
            (SELECT username FROM users WHERE id = %(user_id)s) AS author,
            title,
            "text",
            created_at,
            updated_at;        
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, cmd.model_dump())
            row = await cur.fetchone()
            if row:
                post = models.Post.from_iterable(row)
                return post
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )
