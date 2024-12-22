import { Component, inject, OnInit } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { catchError, of } from 'rxjs';
import { AuthService } from '../auth/auth.service';
import { UserStateService } from '../store/user-state.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ButtonModule, RouterModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  title = 'frontend';

  authService = inject(AuthService);
  userStateService = inject(UserStateService);

  ngOnInit() {
    this.authService
      .getCurrentUser()
      .pipe(
        catchError(() => {
          this.userStateService.unsetUser();
          return of(null);
        })
      )
      .subscribe((user) => {
        if (!user) return;

        this.userStateService.setUser(user);
        this.userStateService.navigateToDashboard();
      });
  }
}
