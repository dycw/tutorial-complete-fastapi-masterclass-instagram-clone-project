from beartype import beartype
from fastapi import APIRouter


router = blog_post_router = APIRouter(prefix="/blog", tags=["blog"])


@router.post("/new")
@beartype
def _() -> None:
    pass
