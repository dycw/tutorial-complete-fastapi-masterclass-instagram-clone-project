from hypothesis.core import given

from app.models.main import UserBase
from tests.strategies.user import users_base


class TestStrategies:
    @given(user=users_base())
    def test_users_base(self, user: UserBase) -> None:
        assert isinstance(user, UserBase)
