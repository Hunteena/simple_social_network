from typing import Annotated

from fastapi import APIRouter, status, Depends

from app import models, services

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/",
    response_model=list[models.PostWithReactions],
    summary="View all posts"
)
async def get_all_posts():
    return await services.get_all_posts()


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
    "/{user_id:int}/",
    response_model=list[models.PostWithReactions],
    summary="View posts of specific user",
)
async def get_posts_by_user_id(user_id: int):
    return await services.get_posts_by_user_id(
        query=models.GetPostsByUserQuery(user_id=user_id)
    )


@router.get(
    "/{post_id:int}/",
    response_model=models.PostWithReactions,
    summary="View post by id",
)
async def get_post_by_id(post_id: int):
    return await services.get_post_by_id(query=models.GetPostQuery(post_id=post_id))


@router.patch(
    "/{post_id:int}",
    response_model=models.Post,
    summary="Update post"
)
async def update_post(
        current_user: Annotated[
            models.User,
            Depends(services.get_current_user)
        ],
        post_id: int,
        query: models.UpdatePostQuery
):
    return await services.update_post(
        cmd=models.UpdatePostCommand(
            **query.model_dump(),
            post_id=post_id,
            user_id=current_user.id
        ),

    )


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
        cmd=models.DeletePostCommand(post_id=post_id, user_id=current_user.id)
    )
