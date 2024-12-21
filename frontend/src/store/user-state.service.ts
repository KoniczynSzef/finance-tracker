import { Injectable, signal } from '@angular/core';
import { catchError, of } from 'rxjs';
import { AuthService } from '../auth/auth.service';
import { User } from '../types/models/user.type';

export interface UserState {
  user: User | null;
  isLoaded: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class UserStateService {
  private state = signal<UserState>({ user: null, isLoaded: false });

  get state$() {
    return this.state;
  }

  constructor(private authService: AuthService) {
    this.authService
      .getCurrentUser()
      .pipe(
        catchError(() => {
          this.unsetUser();
          return of(null);
        })
      )
      .subscribe((user) => {
        this.state.set({ user, isLoaded: true });
      });
  }

  setUser(user: User) {
    this.state.set({ user, isLoaded: true });
  }

  unsetUser() {
    this.state.set({ user: null, isLoaded: false });
  }
}
