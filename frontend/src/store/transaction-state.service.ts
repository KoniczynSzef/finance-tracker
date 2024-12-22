import { Injectable, signal } from '@angular/core';
import {
  TransactionCreate,
  TransactionRead,
} from '../types/schemas/transaction-schemas.type';

@Injectable({
  providedIn: 'root',
})
export class TransactionStateService {
  private transactions = signal<TransactionRead[]>([]);

  get transactions$() {
    return this.transactions;
  }

  setTransactions(transactions: TransactionRead[]) {
    this.transactions.set(transactions);
  }

  addTransaction(transaction: TransactionCreate, userId: number) {
    const newTransaction: TransactionRead = {
      ...transaction,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      user_id: userId,
    };

    this.transactions.set([...this.transactions$(), newTransaction]);
  }

  updateTransaction(transactionId: number, transaction: TransactionCreate) {
    this.transactions.set(
      this.transactions$().map((t) => {
        if (t.id === transactionId) {
          return {
            ...transaction,
            updated_at: t.updated_at,
            created_at: t.created_at,
            user_id: t.user_id,
          };
        }

        return t;
      })
    );
  }

  deleteTransaction(transactionId: number) {
    this.transactions.set(
      this.transactions$().filter((t) => t.id !== transactionId)
    );
  }

  deleteAllTransactions() {
    this.transactions.set([]);
  }
}
