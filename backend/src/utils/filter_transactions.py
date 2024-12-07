from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.schemas.transaction_schemas import TransactionRead


def filter_transactions(transactions: list[TransactionRead], name: Optional[str] = None, category: Optional[str] = None, min_date: Optional[datetime] = None, max_date: Optional[datetime] = None, min_amount: Optional[Decimal] = None, max_amount: Optional[Decimal] = None):
    filtered_transactions: list[TransactionRead] = transactions

    if name:
        filtered_transactions = [
            transaction for transaction in transactions if transaction.name == name]

    if category:
        filtered_transactions = [
            transaction for transaction in filtered_transactions if transaction.category == category]

    if min_date and max_date and min_date <= max_date:
        filtered_transactions = [
            transaction for transaction in filtered_transactions if transaction.date >= min_date and transaction.date <= max_date]
    elif min_date and max_date and min_date > max_date:
        raise ValueError("Invalid date range")

    if min_amount and max_amount and min_amount <= max_amount:
        filtered_transactions = [
            transaction for transaction in filtered_transactions if transaction.amount >= min_amount and transaction.amount <= max_amount]
    elif min_amount and max_amount and min_amount > max_amount:
        raise ValueError("Invalid amount range")

    return filtered_transactions
