import { TransactionRating } from '../models/transaction.type';

export interface TransactionRead {
  id?: number;
  name: string;
  description: string;
  category: string;
  is_income: boolean;
  amount: number;
  date: string;
  currency: string;
  tags: string;
  rating: TransactionRating;
  is_recurring: boolean;
  recurrence_period_in_days: number;
  created_at: string;
  updated_at: string;
  user_id: number;
}

export interface TransactionCreate {
  name: string;
  description: string;
  category: string;
  is_income: boolean;
  amount: number;
  date: string;
  currency: string;
  tags: string;
  rating: TransactionRating;
  is_recurring: boolean;
  recurrence_period_in_days: number;
}

export interface TransactionsSummary {
  total_income: number;
  total_expense: number;
  total_transactions: number;

  average_transaction_amount: number;
  highest_transaction_amount: number;
  lowest_transaction_amount: number;
  most_common_category: string;
}
