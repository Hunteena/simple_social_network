from fastapi import APIRouter

from app import models, services

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{user_id:int}/",
    response_model=list[models.PostWithReactions],
    summary="View posts of specific user",
)
async def get_posts_by_user_id(user_id: int):
    return await services.get_posts_by_user_id(
        query=models.GetPostsByUserQuery(user_id=user_id)
    )
