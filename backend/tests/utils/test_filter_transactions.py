from datetime import datetime
from decimal import Decimal

import pytest
from src.schemas.transaction_schemas import TransactionRead
from src.utils.filter_transactions import filter_transactions


def get_mock_transactions():
    return [
        TransactionRead(
            id=1, name="Groceries", category="Food", date=datetime(2024, 1, 1), amount=Decimal("50.00"), user_id=1
        ),
        TransactionRead(
            id=2, name="Rent", category="Housing", date=datetime(2024, 1, 5), amount=Decimal("1200.00"), user_id=1
        ),
        TransactionRead(
            id=3, name="Utilities", category="Housing", date=datetime(2024, 1, 10), amount=Decimal("150.00"), user_id=1
        ),
        TransactionRead(
            id=4, name="Entertainment", category="Entertainment", date=datetime(2024, 2, 1), amount=Decimal("100.00"), user_id=1
        ),
    ]


def test_filter_without_filters():
    transactions = get_mock_transactions()
    filtered = filter_transactions(transactions)

    assert len(filtered) == 4
    assert all(t.name in [
               "Groceries", "Rent", "Utilities", "Entertainment"] for t in filtered)


def test_filter_by_name():
    transactions = get_mock_transactions()
    filtered = filter_transactions(transactions, name="Groceries")

    assert len(filtered) == 1
    assert filtered[0].name == "Groceries"


def test_filter_by_category():
    transactions = get_mock_transactions()
    filtered = filter_transactions(transactions, category="Housing")

    assert len(filtered) == 2
    assert all(t.category == "Housing" for t in filtered)


def test_filter_by_date_range():
    transactions = get_mock_transactions()
    filtered = filter_transactions(transactions, min_date=datetime(
        2024, 1, 1), max_date=datetime(2024, 1, 31))

    assert len(filtered) == 3
    assert all(t.date >= datetime(2024, 1, 1) and t.date <= datetime(
        2024, 1, 31) for t in filtered)


def test_filter_by_amount_range():
    transactions = get_mock_transactions()
    filtered = filter_transactions(transactions, min_amount=Decimal(
        "50.00"), max_amount=Decimal("150.00"))

    assert len(filtered) == 3
    assert all(Decimal("50.00") <= t.amount <= Decimal("150.00")
               for t in filtered)


def test_combined_filters():
    transactions = get_mock_transactions()
    filtered = filter_transactions(
        transactions,
        name="Groceries",
        category="Food",
        min_date=datetime(2024, 1, 1),
        max_date=datetime(2024, 1, 31),
        min_amount=Decimal("50.00"),
        max_amount=Decimal("100.00"),
    )

    assert len(filtered) == 1
    assert filtered[0].name == "Groceries"
    assert filtered[0].category == "Food"
    assert filtered[0].amount == Decimal("50.00")
    assert filtered[0].date == datetime(2024, 1, 1)


def test_invalid_date_range():
    transactions = get_mock_transactions()
    with pytest.raises(ValueError):
        filter_transactions(transactions, min_date=datetime(
            2024, 1, 1), max_date=datetime(2023, 12, 31))


def test_invalid_amount_range():
    transactions = get_mock_transactions()
    with pytest.raises(ValueError):
        filter_transactions(transactions, min_amount=Decimal(
            "150.00"), max_amount=Decimal("100.00"))
