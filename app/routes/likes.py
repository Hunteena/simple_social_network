from typing import Annotated

from fastapi import APIRouter, Depends

from app import models, services

router = APIRouter(prefix="/posts", tags=["Reactions"])


@router.post(
    "/{post_id:int}/like",
    response_model=models.Reaction,
    summary="Like a post. "
            "If the post was already liked then change to no reaction",
)
async def like_post(
        post_id: int,
        current_user: Annotated[
            models.User,
            Depends(services.get_current_user)
        ],
):
    return await services.react_to_post(
        cmd=models.ReactToPostCommand(
            post_id=post_id,
            user_id=current_user.id,
            like=True
        )
    )


@router.post(
    "/{post_id:int}/dislike",
    response_model=models.Reaction,
    summary="Dislike a post. "
            "If the post was already disliked then change to no reaction",
)
async def dislike_post(
        post_id: int,
        current_user: Annotated[
            models.User,
            Depends(services.get_current_user)
        ],
):
    return await services.react_to_post(
        cmd=models.ReactToPostCommand(
            post_id=post_id,
            user_id=current_user.id,
            like=False
        )
    )
