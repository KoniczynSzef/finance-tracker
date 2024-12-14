import { Component, OnInit } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { AuthService } from '../auth/auth.service';

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
    this.authService.getUser().subscribe((res) => {
      console.log(res);
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
        console.log(res);
        this.authService.saveTokenInLocalStorage(res);

        this.authService.getUser().subscribe((res) => {
          console.log(res);
        });
      }
    });
  }
}
