import { Component, OnInit } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { AuthService } from '../auth/auth.service';
import { ResponseError } from '../types/auth/response-error.type';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ButtonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  title = 'frontend';
  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe({
      next: (user) => {
        if ('error' in user) {
          return;
        }

        console.log(user);
      },
      error: (errorResponse: ResponseError) => {
        console.log('Error Detail: ', errorResponse.error.detail);
      },
    });
  }

  handleClick() {
    const username = window.prompt('Enter your username');
    const password = window.prompt('Enter your password');

    if (!username || !password) {
      return;
    }

    this.authService.login(username, password).subscribe((res) => {
      if ('access_token' in res) {
        this.authService.saveTokenInLocalStorage(res);

        this.authService.getCurrentUser().subscribe((res) => {
          // TODO: logic to set authenticated user
        });
      }
    });
  }

  handleLogout() {
    this.authService.logout();
    window.location.reload();
  }
}
