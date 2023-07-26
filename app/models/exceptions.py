from fastapi import status


class BaseAPIException(Exception):
    status_code: int
    message: str
    headers: dict | None = None


class PostNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Post not found"


class CannotReact(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Cannot react to your own post"


class InvalidCredentials(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Incorrect username or password"
    headers = {"WWW-Authenticate": "Bearer"}


class CredentialsException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class UsernameTaken(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Username already taken"

