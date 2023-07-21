from datetime import date
from typing import Optional

from pydantic import Field, BaseModel, PositiveInt


class PostFields:
    id = Field(description="Post id", examples=["1"])
    user_id = Field(description="Author's id", examples=["1"])
    title = Field(description="Post title", examples=["My best post"])
    text = Field(description="Post text", examples=["Very interesting things"])
    created_at = Field(description="Created at", examples=["2023-07-20"])
    updated_at = Field(description="Updated at", examples=["2023-07-24"], default=None)


class BasePost(BaseModel):
    """Base model for post"""


class CreatePostCommand(BasePost):
    title: str = PostFields.title
    text: str = PostFields.text


class Post(BasePost):
    id: PositiveInt = PostFields.id
    user_id: PositiveInt = PostFields.user_id
    title: str = PostFields.title
    text: str = PostFields.text
    created_at: date = PostFields.created_at
    updated_at: Optional[date] = PostFields.updated_at
