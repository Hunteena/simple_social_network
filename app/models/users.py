from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt
from pydantic.fields import Field
from pydantic.types import SecretStr


class UserFields:
    id = Field(description="User id", examples=["1"])
    username = Field(description="User name", examples=["John Doe"])
    email = Field(description="User email", examples=["some@example.com"])
    password = Field(description="User password", examples=["qwerty"])


class BaseUser(BaseModel):
    """Base model for user"""


# TODO SecretStr
class CreateUserCommand(BaseUser):
    username: str = UserFields.username
    email: EmailStr = UserFields.email
    password: str = UserFields.password


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email


class UserInDB(User):
    hashed_password: str = UserFields.password


class LoginCommand(BaseUser):
    username: str = UserFields.username
    password: str = UserFields.password


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = UserFields.username
