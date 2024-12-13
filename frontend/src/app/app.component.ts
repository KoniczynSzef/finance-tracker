import { Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { catchError, of } from 'rxjs';
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
  isLoggedIn = false;
  constructor(private authService: AuthService) {}

  handleClick() {
    this.authService
      .getUser()
      .pipe(
        catchError((err) => {
          console.log(err);
          return of(null);
        })
      )
      .subscribe((data) => {
        if (data) {
          this.isLoggedIn = true;
        }
      });
  }
}
