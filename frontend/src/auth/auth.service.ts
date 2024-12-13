import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.development';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  API_URL = environment.apiUrl;
  constructor(private httpClient: HttpClient) {}

  getUser() {
    const token = window.localStorage.getItem('jwt-token');

    return this.httpClient.get<any>(`${this.API_URL}/auth/me?token=${token}`);
  }
}
