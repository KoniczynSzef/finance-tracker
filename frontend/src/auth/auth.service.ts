import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.development';
import { Login } from '../types/auth/login.type';
import { Register } from '../types/auth/register.type';
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
    const formData = new FormData();

    formData.append('username', payload.username);
    formData.append('email', payload.email);
    formData.append('password', payload.password);

    return this.httpClient.post<Token>(
      `${this.API_URL}/auth/register`,
      formData,
      {
        headers: new HttpHeaders({ Accept: 'application/json' }),
      }
    );
  }
}
