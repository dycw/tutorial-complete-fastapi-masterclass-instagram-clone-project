from beartype import beartype
from fastapi import FastAPI

from app.routers.article import article_router
from app.routers.blog_get import blog_get_router
from app.routers.blog_post import blog_post_router
from app.routers.user import user_router


@beartype
def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(article_router)
    app.include_router(blog_get_router)
    app.include_router(blog_post_router)
    return app
