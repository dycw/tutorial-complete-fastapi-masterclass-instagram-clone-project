from beartype import beartype
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import builds
from hypothesis_faker.strategies import passwords

from app.models.main import UserBase


@beartype
def users_base() -> SearchStrategy[UserBase]:
    return builds(UserBase, password=passwords())
