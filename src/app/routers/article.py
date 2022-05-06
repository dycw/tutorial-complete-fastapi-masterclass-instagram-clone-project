from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.db_article import create_article
from app.db.db_article import get_article
from app.db.engines import yield_sess
from app.db.schemas.users import DbArticle
from app.schemas import ArticleBase
from app.schemas import ArticleDisplay


router = APIRouter(prefix="/article", tags=["article"])


# Create article


@router.post("/", response_model=ArticleDisplay)
@beartype
def _(
    *, sess: Session = Depends(yield_sess), request: ArticleBase
) -> DbArticle:
    return create_article(sess=sess, request=request)


# Get specific article


@router.get("/{id}", response_model=ArticleDisplay)
@beartype
def _(*, sess: Session = Depends(yield_sess), id: int) -> DbArticle | None:
    return get_article(sess=sess, id=id)
