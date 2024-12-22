import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../types/models/user.type';

export interface UserState {
  user: User | null;
  isLoaded: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class UserStateService {
  router = inject(Router);
  private state = signal<UserState>({ user: null, isLoaded: false });

  get state$() {
    return this.state;
  }

  setUser(user: User) {
    this.state.set({ user, isLoaded: true });
  }

  unsetUser() {
    this.state.set({ user: null, isLoaded: false });
  }

  navigateToDashboard() {
    if (this.state$().user && this.state$().isLoaded) {
      this.router.navigateByUrl('/dashboard');
    }
  }

  navigateToLogin() {
    this.router.navigateByUrl('/login');
  }
}
