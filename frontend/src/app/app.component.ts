import { Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ButtonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'frontend';
  constructor(private authService: AuthService) {}

  handleClick() {
    const username = window.prompt('Enter your username');
    const password = window.prompt('Enter your password');

    if (!username || !password) {
      return;
    }

    this.authService.login(username, password).subscribe((res) => {
      console.log(res);
    });
  }
}
