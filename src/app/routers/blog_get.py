from enum import auto

from beartype import beartype
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_404_NOT_FOUND
from strenum import StrEnum


router = blog_get_router = APIRouter(prefix="/blog", tags=["blog"])


@router.get(
    "/all/",
    summary="Retrieve all blogs",
    description="This API call simulates fetching all blogs",
    response_description="The list of available blogs",
)
@beartype
def _(*, page: int = 1, page_size: int | None = None) -> JSONResponse:
    return JSONResponse({"message": f"All {page_size} blogs on page {page}"})


@router.get("/{id}/comments/{comment_id}", tags=["comment"])
@beartype
def _(
    *, id: int, comment_id: int, valid: bool = True, username: str | None = None
) -> JSONResponse:
    """Simulates rteieving a comment of a blog

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """

    return JSONResponse(
        {"message": f"blog_id {id}, {comment_id=}, {valid=}, {username=}"}
    )


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@router.get("/type/{type}/")
@beartype
def _(*, type: BlogType) -> JSONResponse:
    return JSONResponse({"message": f"Blog type {type}"})


@router.get("/{id}/", status_code=HTTP_200_OK)
@beartype
def _(*, response: Response, id: int) -> JSONResponse:
    if id > 5:
        response.status_code = HTTP_404_NOT_FOUND
        return JSONResponse({"error": f"Blog {id} not found"})
    else:
        response.status_code = HTTP_200_OK
        return JSONResponse({"message": f"Blog with id {id}"})
