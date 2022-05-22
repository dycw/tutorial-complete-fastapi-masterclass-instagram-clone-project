from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.db.schemas.users import DbArticle
from app.models.main import ArticleBase


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


def get_article(*, sess: Session, id: int) -> DbArticle:
    if (
        article := sess.query(DbArticle).filter(DbArticle.id == id).first()
    ) is not None:
        return article
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Article with id {id} not found",
        )
