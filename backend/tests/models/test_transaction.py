from decimal import Decimal

from src.models.transaction import Transaction
from src.models.user import (
    User,  # type: ignore # noqa: F401 (imported because if not, transaction does not find User class)
)


def test_transaction():
    transaction = Transaction(name="test", amount=Decimal(100), user_id=1)

    assert transaction is not None
