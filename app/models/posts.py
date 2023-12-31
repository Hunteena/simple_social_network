from typing import Optional

from pydantic import Field, PositiveInt, NonNegativeInt

from app.models import BaseModel


class PostFields:
    id = Field(description="Post id", examples=[1])
    user_id = Field(description="Author's id", examples=[1])
    author = Field(description="Author username", examples=["John Doe"])
    title = Field(
        description="Post title",
        examples=["My best post"],
        default=None
    )
    text = Field(
        description="Post text",
        examples=["Very interesting things"],
        default=None
    )
    created_at = Field(
        description="Created at",
        examples=["2023-07-20 00:00:00"]
    )
    updated_at = Field(
        description="Updated at",
        examples=["2023-07-24 00:00:00"],
        default=None
    )
    likes = Field(description="Post's likes", examples=[2])
    dislikes = Field(description="Post's dislikes", examples=[1])


class BasePost(BaseModel):
    """Base model for post"""


class CreatePostCommand(BasePost):
    title: str = PostFields.title
    text: str = PostFields.text


class Author(BaseModel):
    user_id: PositiveInt = PostFields.user_id
    username: str = PostFields.author


class Post(BasePost):
    id: PositiveInt = PostFields.id
    author: Author
    title: str = PostFields.title
    text: str = PostFields.text
    created_at: str = PostFields.created_at
    updated_at: Optional[str] = PostFields.updated_at


class PostWithReactions(Post):
    likes: NonNegativeInt = PostFields.likes
    dislikes: NonNegativeInt = PostFields.dislikes


class DeletePostCommand(BasePost):
    post_id: PositiveInt = PostFields.id
    user_id: PositiveInt = PostFields.user_id


class UpdatePostQuery(BasePost):
    title: Optional[str] = PostFields.title
    text: Optional[str] = PostFields.text


class UpdatePostCommand(UpdatePostQuery):
    post_id: PositiveInt = PostFields.id
    user_id: PositiveInt = PostFields.user_id


class GetPostQuery(BasePost):
    post_id: PositiveInt = PostFields.id


class GetPostsByUserQuery(BasePost):
    user_id: PositiveInt = PostFields.user_id
