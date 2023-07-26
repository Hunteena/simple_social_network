from app import models
from app.services.db_connect import postgres_connection


async def get_post_author(post_id: int) -> models.User:
    q = """
    SELECT 
        u.id,
        u.username,
        u.email 
    FROM users AS u 
        JOIN posts AS p ON p.user_id = u.id
    WHERE p.id = %(post_id)s; 
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, {"post_id": post_id})
            row = await cur.fetchone()
            return models.User.from_iterable(row)


async def get_current_reaction(
        query: models.GetReactionQuery
) -> models.Reaction:
    q = """
        SELECT 
            id, 
            post_id,
            user_id,
            "like"
        FROM likes 
        WHERE post_id = %(post_id)s 
            AND user_id = %(user_id)s;    
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, query.model_dump())
            row = await cur.fetchone()
            return models.Reaction.from_iterable(row)


async def react_to_post(
        cmd: models.ReactToPostCommand
) -> models.Post:
    post_author = await get_post_author(post_id=cmd.post_id)
    if post_author is None:
        raise models.PostNotFound
    elif post_author.id == cmd.user_id:
        raise models.CannotReact
    current_reaction = await get_current_reaction(
        models.GetReactionQuery(post_id=cmd.post_id, user_id=cmd.user_id)
    )
    if current_reaction is None:
        q = """
            INSERT INTO likes(
                post_id,
                user_id,
                "like"
            )
                VALUES (
                    %(post_id)s,
                    %(user_id)s,
                    %(like)s
                )
            RETURNING 
                id, 
                post_id,
                user_id,
                "like";
        """
    else:
        q = """
            UPDATE likes
                SET 
                    "like" = %(like)s
                WHERE post_id = %(post_id)s 
                    AND user_id = %(user_id)s
                RETURNING 
                    id, 
                    post_id,
                    user_id,
                    "like";
        """
    params = cmd.model_dump()
    if current_reaction and current_reaction.like == cmd.like:
        params["like"] = None
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            row = await cur.fetchone()
            return models.Reaction.from_iterable(row)
