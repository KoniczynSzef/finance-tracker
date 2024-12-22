import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.development';
import { Login } from '../types/auth/login.type';
import { Register } from '../types/auth/register.type';
import { Token } from '../types/auth/token.type';
import { UserRead } from '../types/schemas/user-schemas.type';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  API_URL = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  getCurrentUser() {
    const token = window.localStorage.getItem('jwt-token');

    return this.httpClient.get<UserRead>(
      `${this.API_URL}/auth/me?token=${token}`
    );
  }

  login(payload: Login) {
    const formData = new FormData();

    formData.append('username', payload.username);
    formData.append('password', payload.password);

    return this.httpClient.post<Token>(`${this.API_URL}/auth/token`, formData, {
      headers: new HttpHeaders({ Accept: 'application/json' }),
    });
  }

  register(payload: Register) {
    return this.httpClient.post<UserRead>(
      `${this.API_URL}/auth/register`,
      payload,
      {
        headers: new HttpHeaders({ Accept: 'application/json' }),
      }
    );
  }

  saveToken(token: Token) {
    window.localStorage.setItem('jwt-token', token.access_token);
  }

  getAuthenticationToken() {
    const token = window.localStorage.getItem('jwt-token');

    if (!token) {
      throw new Error('Not authenticated');
    }

    return token;
  }

  logout() {
    window.localStorage.removeItem('jwt-token');
  }
}
