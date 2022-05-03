from contextlib import AbstractContextManager

from beartype import beartype
from sqlalchemy.orm import Session

from app.db.hash import Hash
from app.db.models import DbUser
from app.schemas import UserBase


@beartype
def create_user(
    *, db: AbstractContextManager[Session], request: UserBase
) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    with db as sess:
        sess.add(new_user)
        sess.commit()
        sess.refresh(new_user)
    return new_user


@beartype
def get_all_users(*, db: AbstractContextManager[Session]) -> list[DbUser]:
    with db as sess:
        return sess.query(DbUser).all()


@beartype
def get_user(*, db: AbstractContextManager[Session], id: int) -> DbUser | None:
    with db as sess:
        return sess.query(DbUser).filter(DbUser.id == id).first()


@beartype
def update_user(
    *, db: AbstractContextManager[Session], id: int, request: UserBase
) -> bool:
    with db as sess:
        user = sess.query(DbUser).filter(DbUser.id == id)
        user.update(
            {
                DbUser.username: request.username,
                DbUser.email: request.email,
                DbUser.password: Hash.bcrypt(request.password),
            }
        )
        sess.commit()
    return True


@beartype
def delete_user(*, db: AbstractContextManager[Session], id: int) -> bool:
    with db as sess:
        user = sess.query(DbUser).filter(DbUser.id == id).first()
        if user is not None:
            sess.delete(user)
            sess.commit()
    return True
