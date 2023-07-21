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
        current_user: Annotated[models.User, Depends(services.get_current_user)],
        cmd: models.CreatePostCommand
):
    user = await services.create_post(cmd=cmd, user_id=current_user.id)
    return user
