from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import builds
from hypothesis_faker.strategies import passwords

from app.models.main import UserBase


def users_base() -> SearchStrategy[UserBase]:
    return builds(UserBase, password=passwords())
