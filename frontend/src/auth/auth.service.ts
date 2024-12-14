import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.development';
import { ResponseError } from '../types/auth/response-error.type';
import { Token } from '../types/auth/token.type';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  API_URL = environment.apiUrl;
  constructor(private httpClient: HttpClient) {}

  healthCheck() {
    return this.httpClient.get<{ status: 'ok' }>(`${this.API_URL}/`);
  }

  getUser() {
    const token = window.localStorage.getItem('jwt-token');

    return this.httpClient.get<any>(`${this.API_URL}/auth/me?token=${token}`);
  }

  login(username: string, password: string) {
    const formData = new FormData();

    formData.append('username', username);
    formData.append('password', password);

    return this.httpClient.post<Token | ResponseError>(
      `${this.API_URL}/auth/token`,
      formData,
      {
        headers: new HttpHeaders({ Accept: 'application/json' }),
      }
    );
  }

  saveTokenInLocalStorage(token: Token) {
    window.localStorage.setItem('jwt-token', token.access_token);
  }
}
