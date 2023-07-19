from pydantic import BaseModel, EmailStr, PositiveInt
from pydantic.fields import Field
from pydantic.types import SecretStr


class UserFields:
    id = Field(description="User id", example="1")
    username = Field(description="User name", example="John Doe")
    email = Field(description="User email", example="some@example.com")
    password = Field(description="User password")


class BaseUser(BaseModel):
    """Base model for user"""


# TODO SecretStr
class CreateUserCommand(BaseUser):
    username: str = UserFields.username
    email: EmailStr = UserFields.email
    password: str = UserFields.password


class UserCreated(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email
