from decimal import Decimal

from models.transaction import Transaction


def test_transaction():
    transaction = Transaction(name="test", amount=Decimal(100), user_id=1)

    assert transaction is not None
