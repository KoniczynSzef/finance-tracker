import { inject } from '@angular/core';
import { patchState, signalStore, withMethods, withState } from '@ngrx/signals';
import { AuthService } from '../auth/auth.service';
import { Login } from '../types/auth/login.type';
import { User } from '../types/models/user.type';

type UserState = { user: User | null };

const userState: UserState = { user: null };

export const UserStore = signalStore(
  {
    providedIn: 'root',
  },
  withState(userState),
  withMethods((store, authService = inject(AuthService)) => ({
    login: (payload: Login) => {
      const res = authService.login(payload);

      res.subscribe((token) => {
        authService.getCurrentUser().subscribe((user) => {
          window.localStorage.setItem('jwt-token', token.access_token);
          patchState(store, { user: user });
        });
      });
    },

    isAuthenticated: () => {
      return !!window.localStorage.getItem('jwt-token');
    },

    logout: () => {
      window.localStorage.removeItem('jwt-token');
      patchState(store, { user: null });
    },
  }))
);
