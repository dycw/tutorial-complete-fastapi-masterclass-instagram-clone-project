from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.db.schemas.users import DbUser
from app.models.main import UserBase
from app.utilities.hash import Hash


# create


def create_user(*, sess: Session, request: UserBase) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    sess.add(new_user)
    sess.commit()
    sess.refresh(new_user)
    return new_user


# read


def get_all_users(*, sess: Session) -> list[DbUser]:
    return sess.query(DbUser).all()


def get_user(*, sess: Session, id: int) -> DbUser:
    if (user := sess.query(DbUser).filter(DbUser.id == id).first()) is not None:
        return user
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )


# update


def update_user(*, sess: Session, id: int, request: UserBase) -> bool:
    if (user := sess.query(DbUser).filter(DbUser.id == id)) is not None:
        _ = user.update(
            {
                DbUser.username: request.username,
                DbUser.email: request.email,
                DbUser.password: Hash.bcrypt(request.password),
            }
        )
        sess.commit()
        return True
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )


# delete


def delete_user(*, sess: Session, id: int) -> bool:
    if (user := sess.query(DbUser).filter(DbUser.id == id).first()) is not None:
        if user is not None:
            sess.delete(user)
            sess.commit()
        return True
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
