from app import models
from app.services.db_connect import postgres_connection


async def create(
        cmd: models.CreateUserCommand,
):
    # TODO hash password
    q = """
        INSERT INTO users(
            username,
            email,
            password
        )
            VALUES (
                %(username)s,
                %(email)s,
                %(password)s
            )
        RETURNING 
            id, 
            username,
            email;
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, cmd.model_dump())
            row = await cur.fetchone()
            user = dict(zip(["id", "username", "email"], row))
            return user
