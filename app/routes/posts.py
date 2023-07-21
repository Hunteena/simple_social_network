from typing import Annotated

from fastapi import APIRouter, status, Depends

from app import models, services

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/",
    response_model=models.Post,
    status_code=status.HTTP_201_CREATED,
    summary="Create post",
)
async def create_post(
        current_user: Annotated[
            models.User,
            Depends(services.get_current_user)
        ],
        cmd: models.CreatePostCommand
):
    return await services.create_post(cmd=cmd, user_id=current_user.id)


@router.get(
    "/",
    response_model=list[models.Post],
    summary="View all posts"
)
async def get_all_posts():
    return await services.get_all_posts()


@router.delete(
    "/{post_id:int}",
    response_model=models.Post,
    summary="Delete post"
)
async def delete_post(
        current_user: Annotated[
            models.User,
            Depends(services.get_current_user)
        ],
        post_id: int,
):
    return await services.delete_post(
        cmd=models.DeletePostCommand(post_id=post_id),
        user_id=current_user.id
    )
