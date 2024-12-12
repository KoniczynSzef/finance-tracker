import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

const API_URL = process.env['API_URL'];
console.log(API_URL);

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private httpClient: HttpClient) {}
}
