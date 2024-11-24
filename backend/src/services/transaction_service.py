from decimal import Decimal

from fastapi import Depends
from sqlmodel import Session, select

from src.database.config import get_session
from src.models.transaction import Transaction
from src.models.user import User


class TransactionService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_transactions(self):
        transactions = self.session.exec(select(Transaction)).all()
        return transactions

    def add_transaction(self, transaction: Transaction, user: User):
        if not user.id:
            raise ValueError(
                "Invalid user: User must have an ID to add a transaction.")

        transaction.user_id = user.id

        self.session.add(transaction)
        self.update_user_balance(
            user, transaction.is_income, transaction.amount)

        return transaction

    def update_user_balance(self, user: User, is_income: bool, amount: Decimal):
        if not user.id:
            raise ValueError(
                "Invalid user: User must have an ID to update the balance.")

        user.current_balance += amount if is_income else -amount

        self.session.commit()
        self.session.refresh(user)

        return user
