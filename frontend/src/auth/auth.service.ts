import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.development';
import { ResponseError } from '../types/auth/response-error.type';
import { Token } from '../types/auth/token.type';
import { User } from '../types/models/user.type';
import { UserRead } from '../types/schemas/user-schemas.type';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  API_URL = environment.apiUrl;
  user: User | null = null;

  constructor(private httpClient: HttpClient) {}

  getCurrentUser() {
    const token = window.localStorage.getItem('jwt-token');

    return this.httpClient.get<UserRead | ResponseError>(
      `${this.API_URL}/auth/me?token=${token}`
    );
  }

  login(username: string, password: string) {
    const formData = new FormData();

    formData.append('username', username);
    formData.append('password', password);

    return this.httpClient.post<Token>(`${this.API_URL}/auth/token`, formData, {
      headers: new HttpHeaders({ Accept: 'application/json' }),
    });
  }

  saveTokenInLocalStorage(token: Token) {
    window.localStorage.setItem('jwt-token', token.access_token);
  }

  logout() {
    window.localStorage.removeItem('jwt-token');
  }
}
