from fastapi import FastAPI

from app.routers import article
from app.routers import blog_get
from app.routers import blog_post
from app.routers import user


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user.router)
    app.include_router(article.router)
    app.include_router(blog_get.router)
    app.include_router(blog_post.router)
    return app


app = create_app()
