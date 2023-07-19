from fastapi import APIRouter, status

from app import models, services

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=models.UserCreated,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
)
async def create_user(cmd: models.CreateUserCommand):
    user = await services.create(cmd=cmd)
    return user


@router.get(
    "/",
    summary="Get all users"
)
async def get_all_users():
    return {"message": "All users are to be shown here"}
