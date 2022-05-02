from enum import auto

from beartype import beartype
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_404_NOT_FOUND
from strenum import StrEnum


app = FastAPI()


@app.get("/hello/")
@beartype
def _() -> JSONResponse:
    return JSONResponse({"Hello": "World"})


@app.get("/blog/all/")
@beartype
def _(*, page: int = 1, page_size: int | None = None) -> JSONResponse:
    return JSONResponse({"message": f"All {page_size} blogs on page {page}"})


@app.get("/blog/{id}/comments/{comment_id}")
@beartype
def _(
    *, id: int, comment_id: int, valid: bool = True, username: str | None = None
) -> JSONResponse:
    return JSONResponse(
        {"message": f"blog_id {id}, {comment_id=}, {valid=}, {username=}"}
    )


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@app.get("/blog/type/{type}/")
@beartype
def _(*, type: BlogType) -> JSONResponse:
    return JSONResponse({"message": f"Blog type {type}"})


@app.get("/blog/{id}/", status_code=HTTP_200_OK)
@beartype
def _(*, response: Response, id: int) -> JSONResponse:
    if id > 5:
        response.status_code = HTTP_404_NOT_FOUND
        return JSONResponse({"error": f"Blog {id} not found"})
    else:
        response.status_code = HTTP_200_OK
        return JSONResponse({"message": f"Blog with id {id}"})
