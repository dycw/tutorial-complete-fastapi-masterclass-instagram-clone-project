from dycw_utilities.fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.articles import create_article
from app.crud.articles import get_article
from app.db.engines import yield_sess
from app.db.schemas.users import DbArticle
from app.models.main import ArticleBase
from app.models.main import ArticleDisplay


router = APIRouter(prefix="/article", tags=["article"])


# create


@router.post("/", response_model=ArticleDisplay)
def _(
    *, sess: Session = Depends(yield_sess), request: ArticleBase
) -> DbArticle:
    return create_article(sess=sess, request=request)


# read


@router.get("/{id}", response_model=ArticleDisplay)
def _(*, sess: Session = Depends(yield_sess), id: int) -> DbArticle | None:
    return get_article(sess=sess, id=id)
