from enum import auto
from typing import Any

from fastapi import Depends
from fastapi.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_404_NOT_FOUND
from strenum import StrEnum

from app.routers.blog_post import required_functionality
from app.utilities.routers import APIRouter


router = APIRouter(prefix="/blog", tags=["blog"])


@router.get(
    "/all",
    summary="Retrieve all blogs",
    description="This API call simulates fetching all blogs",
    response_description="The list of available blogs",
)
def _(
    *,
    page: int = 1,
    page_size: int | None = None,
    req_parameter: dict[str, str] = Depends(required_functionality),
) -> dict[str, Any]:
    return {
        "message": f"All {page_size} blogs on page {page}",
        "req_parameter": req_parameter,
    }


@router.get("/{id}/comments/{comment_id}", tags=["comment"])
def _(
    *, id: int, comment_id: int, valid: bool = True, username: str | None = None
) -> dict[str, Any]:
    """Simulates rteieving a comment of a blog

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """

    return {"message": f"blog_id {id}, {comment_id=}, {valid=}, {username=}"}


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@router.get("/type/{type}")
def _(*, type: BlogType) -> dict[str, Any]:
    return {"message": f"Blog type {type}"}


@router.get("/{id}", status_code=HTTP_200_OK)
def _(*, response: Response, id: int) -> dict[str, Any]:
    if id > 5:
        response.status_code = HTTP_404_NOT_FOUND
        return {"error": f"Blog {id} not found"}
    else:
        response.status_code = HTTP_200_OK
        return {"message": f"Blog with id {id}"}
