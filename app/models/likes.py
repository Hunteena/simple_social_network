from typing import Optional

from pydantic import Field, PositiveInt

from app.models import BaseModel


class LikeFields:
    id = Field(description="Relation post/user id", examples=[1])
    post_id = Field(description="Post id", examples=[2])
    user_id = Field(description="User id", examples=[3])
    like = Field(
        description="Does user like the post or not",
        examples=[True, False, None],
        default=None
    )


class BaseReaction(BaseModel):
    """Base class for like"""


class Reaction(BaseReaction):
    id: PositiveInt = LikeFields.id
    post_id: PositiveInt = LikeFields.post_id
    user_id: PositiveInt = LikeFields.user_id
    like: Optional[bool] = LikeFields.like


class ReactToPostCommand(BaseReaction):
    post_id: PositiveInt = LikeFields.post_id
    user_id: PositiveInt = LikeFields.user_id
    like: bool = LikeFields.like


class GetReactionQuery(BaseReaction):
    post_id: PositiveInt = LikeFields.post_id
    user_id: PositiveInt = LikeFields.user_id
