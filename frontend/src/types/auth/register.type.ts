export interface Register {
  username: string;
  email: string;
  password: string;

  // * These fields are not essential for the registration, they will have default values
  full_name: string;
  current_balance: number;
  balance_threshold: number;
}
