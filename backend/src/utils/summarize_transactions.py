from decimal import Decimal

from src.schemas.transaction_schemas import TransactionRead, TransactionsSummary


def summarize_transactions(transactions: list[TransactionRead]):
    total_income = Decimal(0)
    total_expense = Decimal(0)
    total_transactions = 0

    highest_transaction_amount = Decimal(0)
    lowest_transaction_amount = Decimal(0)
    average_transaction_amount = Decimal(0)

    for transaction in transactions:
        if transaction.is_income:
            total_income += transaction.amount
        else:
            total_expense += transaction.amount

        if transaction.amount > highest_transaction_amount:
            highest_transaction_amount = transaction.amount

        if transaction.amount < lowest_transaction_amount:
            lowest_transaction_amount = transaction.amount

        average_transaction_amount += transaction.amount

        total_transactions += 1

    average_transaction_amount = average_transaction_amount / total_transactions

    return TransactionsSummary(
        total_income=total_income,
        total_expense=total_expense,
        total_transactions=total_transactions,
        average_transaction_amount=average_transaction_amount,
        highest_transaction_amount=highest_transaction_amount,
    )
