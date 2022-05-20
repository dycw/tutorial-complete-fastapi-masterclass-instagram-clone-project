from typing import Any
from typing import cast

from sqlalchemy.orm import declarative_base


Base = cast(Any, declarative_base())
