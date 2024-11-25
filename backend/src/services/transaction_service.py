from decimal import Decimal

from fastapi import Depends
from sqlmodel import Session, select

from src.database.config import get_session
from src.models.transaction import Transaction
from src.models.user import User


class TransactionService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_transactions_by_user_id(self, user_id: int):
        transactions = self.session.exec(
            select(Transaction).where(Transaction.user_id == user_id)).all()

        return transactions

    def add_transaction(self, transaction: Transaction, user: User):
        if not user.id:
            raise ValueError(
                "Invalid user: User must have an ID to add a transaction.")

        transaction.user_id = user.id

        self.session.add(transaction)
        self.update_user_balance(
            user, transaction.is_income, Decimal(transaction.amount))

        return transaction

    def update_user_balance(self, user: User, is_income: bool, amount: Decimal):
        if not user.id:
            raise ValueError(
                "Invalid user: User must have an ID to update the balance.")

        if amount <= 0:
            raise ValueError(
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

    def delete_transaction_by_id(self, transaction_id: int):
        transaction = self.session.get(Transaction, transaction_id)

        if not transaction:
            raise ValueError(
                "Invalid transaction: Transaction does not exist.")

        self.session.delete(transaction)
        self.session.commit()

        return transaction
