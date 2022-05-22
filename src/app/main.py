from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_418_IM_A_TEAPOT

from app.exceptions import StoryException
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

    @app.exception_handler(StoryException)  # type: ignore
    def _(_: Request, exc: StoryException) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_418_IM_A_TEAPOT, content={"detail": exc.name}
        )

    return app


app = create_app()
