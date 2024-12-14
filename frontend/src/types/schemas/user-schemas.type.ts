export interface UserCreate {
  username: string;
  email: string;
  full_name: string;
  password: string;
}

export interface UserRead {
  id?: number;
  username: string;
  email: string;
  full_name: string;
  hashed_password: string;

  is_active: boolean;
  is_verified: boolean;

  current_balance: number;
  balance_threshold: number;

  created_at: string;
  updated_at: string;

  // TODO: add transaction array
}

export interface UserUpdate {
  username?: string;
  email?: string;
  full_name?: string;
  password?: string;
}
