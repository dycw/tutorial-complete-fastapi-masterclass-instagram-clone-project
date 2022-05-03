from contextlib import AbstractContextManager

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import yield_db
from app.db.db_article import create_article
from app.db.db_article import get_article
from app.db.models import DbArticle
from app.schemas import ArticleBase
from app.schemas import ArticleDisplay


router = article_router = APIRouter(prefix="/article", tags=["article"])


# Create article


@router.post("/", response_model=ArticleDisplay)
def _(
    *,
    db: AbstractContextManager[Session] = Depends(yield_db),
    request: ArticleBase,
) -> DbArticle:
    return create_article(db=db, request=request)


# Get specific article


@router.get("/{id}", response_model=ArticleDisplay)
def _(
    *, db: AbstractContextManager[Session] = Depends(yield_db), id: int
) -> DbArticle | None:
    return get_article(db=db, id=id)
