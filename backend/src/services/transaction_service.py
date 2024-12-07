from datetime import datetime
from decimal import Decimal

from fastapi import Depends

# from schemas.transaction_schemas import TransactionRead
from sqlmodel import Session, select

from src.database.config import get_session
from src.models.transaction import Transaction, TransactionRating
from src.models.user import User
from src.schemas.errors import InvalidCredentials, NotFound, ValidationError
from src.schemas.transaction_schemas import (  # type: ignore # noqa: F401
    TransactionBase,
    TransactionCreate,
    TransactionRead,
)


class TransactionService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_transactions_by_user_id(self, user_id: int):
        transactions = self.session.exec(
            select(Transaction).where(Transaction.user_id == user_id)).all()

        return [TransactionRead(**transaction.model_dump()) for transaction in transactions]

    def get_transaction_by_id(self, transaction_id: int, user_id: int):
        transaction = self.session.exec(select(Transaction).where(
            Transaction.id == transaction_id)).first()

        if not transaction:
            raise NotFound(
                "Invalid transaction: Transaction does not exist.")

        if transaction.user_id != user_id:
            raise InvalidCredentials(
                "Invalid transaction: User does not own the transaction.")

        return transaction

    def add_transaction(self, user: User, transaction: TransactionCreate):
        if not user.id:
            raise InvalidCredentials(
                "Invalid user: User must have an ID to add a transaction.")

        try:
            new_transaction = Transaction(**transaction.model_dump())
            new_transaction.user_id = user.id
            new_transaction.user = user
        except ValidationError as e:
            raise ValidationError(e.args[0])

        self.session.add(new_transaction)
        user.transactions.append(new_transaction)

        self.session.add(user)
        self.session.commit()

        self.session.refresh(new_transaction)
        self.session.refresh(user)

        return TransactionRead(**new_transaction.model_dump())

    def update_user_balance(self, user: User, is_income: bool, amount: Decimal):
        if not user.id:
            raise InvalidCredentials(
                "Invalid user: User must have an ID to update the balance.")

        if amount <= 0:
            raise ValidationError(
                "Invalid transaction: Transaction amount must be greater than 0.")

        new_balance: Decimal = user.current_balance

        if not is_income:
            new_balance -= amount
        else:
            new_balance += amount

        user.current_balance = new_balance

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def update_transaction_by_id(self, transaction_id: int, user_id: int, transaction: TransactionBase):
        existing_transaction = self.session.exec(select(Transaction).where(
            Transaction.id == transaction_id)).first()

        if not existing_transaction:
            raise NotFound(
                "Invalid transaction: Transaction does not exist.")

        if existing_transaction.user_id != user_id:
            raise InvalidCredentials(
                "Invalid transaction: User does not own the transaction.")

        existing_transaction.name = transaction.name
        existing_transaction.description = transaction.description
        existing_transaction.category = transaction.category
        existing_transaction.tags = transaction.tags
        existing_transaction.date = transaction.date
        existing_transaction.amount = transaction.amount
        existing_transaction.currency = transaction.currency
        existing_transaction.is_income = transaction.is_income
        existing_transaction.rating = TransactionRating[transaction.rating]
        existing_transaction.is_recurring = transaction.is_recurring
        existing_transaction.recurrence_period_in_days = transaction.recurrence_period_in_days
        existing_transaction.updated_at = datetime.now()

        self.session.add(existing_transaction)
        self.session.commit()
        self.session.refresh(existing_transaction)

        return TransactionRead(**existing_transaction.model_dump())

    def delete_transaction_by_id(self, transaction_id: int, user_id: int):
        transaction = self.session.exec(select(Transaction).where(
            Transaction.id == transaction_id)).first()

        if not transaction:
            raise NotFound(
                "Invalid transaction: Transaction does not exist.")

        if transaction.user_id != user_id:
            raise InvalidCredentials(
                "Invalid transaction: User does not own the transaction.")

        self.session.delete(transaction)
        self.session.commit()

        return TransactionRead(**transaction.model_dump())

    def delete_all_transactions_by_user_id(self, user_id: int):
        transactions = self.session.exec(
            select(Transaction).where(Transaction.user_id == user_id)).all()

        if len(transactions) == 0:
            return "No transactions to delete."

        for transaction in transactions:
            self.session.delete(transaction)

        self.session.commit()

        return "Transactions deleted successfully."
