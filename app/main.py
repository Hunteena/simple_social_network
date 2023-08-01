from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.exceptions import BaseAPIException
from app.routes import auth, likes, posts, users

description = """
You are able to:
- **view** all posts,
- **signup**,
- **login** and get an access token.  

With the access token you are able to:
- **create** a post,
- **edit and delete** your own posts,
- **like or dislike** other users' posts.
"""

app = FastAPI(
    title="Simple social network",
    description=description,
    summary="RESTful API for a simple social networking application",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(likes.router)


@app.exception_handler(BaseAPIException)
def handle_api_exceptions(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
        headers=exc.headers
    )
