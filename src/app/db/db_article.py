from contextlib import AbstractContextManager

from beartype import beartype
from sqlalchemy.orm import Session

from app.db.models import DbArticle
from app.schemas import ArticleBase


@beartype
def create_article(
    *, db: AbstractContextManager[Session], request: ArticleBase
) -> DbArticle:
    new_article = DbArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id,
    )
    with db as sess:
        sess.add(new_article)
        sess.commit()
        sess.refresh(new_article)
    return new_article


@beartype
def get_article(
    *, db: AbstractContextManager[Session], id: int
) -> DbArticle | None:
    with db as sess:
        return sess.query(DbArticle).filter(DbArticle.id == id).first()
