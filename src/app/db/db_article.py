from beartype import beartype
from sqlalchemy.orm import Session

from app.db.schemas.users import DbArticle
from app.schemas import ArticleBase


@beartype
def create_article(*, sess: Session, request: ArticleBase) -> DbArticle:
    new_article = DbArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id,
    )
    sess.add(new_article)
    sess.commit()
    sess.refresh(new_article)
    return new_article


@beartype
def get_article(*, sess: Session, id: int) -> DbArticle | None:
    return sess.query(DbArticle).filter(DbArticle.id == id).first()
