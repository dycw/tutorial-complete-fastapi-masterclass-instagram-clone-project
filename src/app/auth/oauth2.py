import datetime as dt
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose.jwt import encode


oauth2_scheme = OAuth2PasswordBearer("token")


SECRET_KEY = "77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107"  # noqa: S105
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict, expires_delta: Optional[dt.timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = dt.datetime.utcnow() + expires_delta
    else:
        expire = dt.datetime.utcnow() + dt.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    assert 0, type(encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
