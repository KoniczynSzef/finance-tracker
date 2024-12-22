import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { environment } from '../../environments/environment.development';
import {
  TransactionCreate,
  TransactionRead,
  TransactionsSummary,
} from '../../types/schemas/transaction-schemas.type';

@Injectable({
  providedIn: 'root',
})
export class TransactionService {
  API_URL = environment.apiUrl;
  authService = inject(AuthService);
  httpClient = inject(HttpClient);

  getAllTransactions(
    name?: string,
    category?: string,
    min_date?: string,
    max_date?: string,
    min_amount?: number,
    max_amount?: number
  ) {
    const token = this.authService.getAuthenticationToken();
    const params = new HttpParams({
      fromString:
        'name=' +
        name +
        '&category=' +
        category +
        '&min_date=' +
        min_date +
        '&max_date=' +
        max_date +
        '&min_amount=' +
        min_amount +
        '&max_amount=' +
        max_amount,
    });

    return this.httpClient.get<TransactionRead[]>(
      `${this.API_URL}/transactions`,
      {
        headers: { Authorization: `Bearer ${token}` },
        params,
      }
    );
  }

  getTransactionById(transactionId: number) {
    const token = this.authService.getAuthenticationToken();

    return this.httpClient.get<TransactionRead>(
      `${this.API_URL}/transactions/${transactionId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
  }

  getTransactionsSummary() {
    const token = this.authService.getAuthenticationToken();

    return this.httpClient.get<TransactionsSummary>(
      `${this.API_URL}/transactions/transactions-summary`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
  }

  createTransaction(transaction: TransactionCreate) {
    const token = this.authService.getAuthenticationToken();

    return this.httpClient.post<TransactionRead>(
      `${this.API_URL}/transactions`,
      transaction,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
  }

  updateTransaction(transactionId: number, transaction: TransactionCreate) {
    const token = this.authService.getAuthenticationToken();

    return this.httpClient.put<TransactionRead>(
      `${this.API_URL}/transactions/${transactionId}`,
      transaction,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
  }

  deleteTransaction(transactionId: number) {
    const token = this.authService.getAuthenticationToken();

    return this.httpClient.delete<TransactionRead>(
      `${this.API_URL}/transactions/${transactionId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
  }

  deleteAllTransactions() {
    const token = this.authService.getAuthenticationToken();

    this.authService.getCurrentUser().subscribe((user) => {
      return this.httpClient.delete<string>(
        `${this.API_URL}/transactions/all/${user.id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
    });
  }
}
