from enum import auto

from beartype import beartype
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from strenum import StrEnum


app = FastAPI()


@app.get("/hello/")
@beartype
def _() -> JSONResponse:
    return JSONResponse({"Hello": "World"})


@app.get("/blog/all/")
@beartype
def _() -> JSONResponse:
    return JSONResponse({"message": "All blogs provided"})


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@app.get("/blog/type/{type}/")
@beartype
def _(*, type: BlogType) -> JSONResponse:
    return JSONResponse({"message": f"Blog type {type}"})


@app.get("/blog/{id}/")
@beartype
def _(*, id: int) -> JSONResponse:
    return JSONResponse({"message": f"Blog with id {id}"})
