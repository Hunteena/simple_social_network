from fastapi import FastAPI

from app.routes import users, posts, likes

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

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(likes.router)
