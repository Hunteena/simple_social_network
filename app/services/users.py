from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app import models
from app.services.db_connect import postgres_connection
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def create(cmd: models.CreateUserCommand) -> models.User:
    user = await get_user(cmd.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
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
    params = cmd.model_dump()
    params.update(password=get_password_hash(params["password"]))
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            row = await cur.fetchone()
            user = models.User(**dict(zip(["id", "username", "email"], row)))
            return user


async def get_all() -> list[models.User]:
    q = """
    SELECT 
        id, 
        username,
        email
    FROM users;    
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q)
            rows = await cur.fetchall()
            users = [
                models.User(**dict(zip(["id", "username", "email"], row)))
                for row in rows
            ]
            return users


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str) -> models.UserInDB:
    q = """
    SELECT 
        id,
        username,
        email,
        password
    FROM users
    WHERE username = %(username)s;
    """
    async with postgres_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, {'username': username})
            row = await cur.fetchone()
            if row:
                user = models.UserInDB(
                    **dict(zip(["id", "username", "email", "hashed_password"],
                               row))
                )
                return user


async def authenticate_user(
        cmd: models.LoginCommand
) -> bool | models.UserInDB:
    user = await get_user(cmd.username)
    if not user:
        return False
    if not verify_password(cmd.password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value())
    return encoded_jwt


async def login_for_access_token(cmd: models.LoginCommand) -> models.Token:
    user = await authenticate_user(cmd)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")
