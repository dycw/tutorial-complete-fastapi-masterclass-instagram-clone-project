from typing import Any
from typing import Optional
from typing import cast

from dycw_utilities.fastapi import APIRouter
from fastapi import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.auth.oauth2 import create_access_token
from app.auth.oauth2 import token_key
from app.db.engines import yield_sess
from app.db.schemas.users import DbUser
from app.utilities.hash import Hash


router = APIRouter(tags=["authentication"])


@router.post(f"/{token_key}")
def _(
    *,
    request: OAuth2PasswordRequestForm = Depends(),
    sess: Session = Depends(yield_sess),
) -> dict[str, Any]:
    username = request.username
    if (
        user := cast(
            Optional[DbUser],
            sess.query(DbUser).filter(DbUser.username == username).first(),
        )
    ) is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify(cast(str, user.password), request.password):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = create_access_token({"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
