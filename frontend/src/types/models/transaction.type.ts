export interface Transaction {
  id?: number;
  name: string;
  description: string;
  category: string;
  is_income: boolean;
  amount: number;
  date: Date;
  currency: string;
  tags: string;
  rating: TransactionRating;
  is_recurring: boolean;
  recurrence_period_in_days: number;
  created_at: Date;
  updated_at: Date;
  user_id: number;
}

export enum TransactionRating {
  SATISFIED = 'SATISFIED',
  NEUTRAL = 'NEUTRAL',
  REGRETFUL = 'REGRETFUL',
  DISLIKE = 'DISLIKE',
  IMPORTANT = 'IMPORTANT',
}
