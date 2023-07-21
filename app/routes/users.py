from fastapi import APIRouter, status

from app import models, services

router = APIRouter(prefix="", tags=["Authorization"])


@router.post(
    "/signup",
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
)
async def create_user(cmd: models.CreateUserCommand):
    user = await services.create_user(cmd=cmd)
    return user


@router.post(
    "/login",
    response_model=models.Token,
    summary="Log in user"
)
async def login(
        cmd: models.LoginCommand
):
    return await services.login_for_access_token(cmd)


# TODO remove
@router.get(
    "/users",
    response_model=list[models.User],
    summary="Get all users"
)
async def get_all_users():
    return await services.get_all_users()
