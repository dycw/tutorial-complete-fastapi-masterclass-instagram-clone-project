from typing import cast

from dycw_utilities.modules import yield_modules
from sqlalchemy.sql.schema import MetaData

from app.db import schemas
from app.db.engines import SQLITE_ENGINE
from app.db.schemas.base import Base


for _ in yield_modules(schemas, recursive=True):
    pass


cast(MetaData, Base.metadata).create_all(SQLITE_ENGINE)
