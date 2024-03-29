from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_418_IM_A_TEAPOT

from app.exceptions import StoryException
from app.routers import article
from app.routers import blog_get
from app.routers import blog_post
from app.routers import product
from app.routers import user


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(article.router)
    app.include_router(blog_get.router)
    app.include_router(blog_post.router)
    app.include_router(product.router)
    app.include_router(user.router)
    app.exception_handler(StoryException)(handle_story_exception)
    origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def handle_http_exception(_: Request, exc: HTTPException) -> PlainTextResponse:
    return PlainTextResponse(content=str(exc), status_code=HTTP_400_BAD_REQUEST)


def handle_story_exception(_: Request, exc: StoryException) -> JSONResponse:
    return JSONResponse(
        content={"detail": exc.name}, status_code=HTTP_418_IM_A_TEAPOT
    )


app = create_app()
