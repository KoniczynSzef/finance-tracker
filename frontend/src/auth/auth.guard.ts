import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserStateService } from '../store/user-state.service';

export function redirectToLoginIfNotAuthenticated(): CanActivateFn {
  return () => {
    const user = inject(UserStateService).state$().user;
    const router = inject(Router);

    if (!user) {
      // * Redirect to login page
      return router.parseUrl('/login');
    }

    return true;
  };
}

export function redirectToDashboardIfAuthenticated(): CanActivateFn {
  return () => {
    const user = inject(UserStateService).state$().user;
    const router = inject(Router);

    if (user) {
      // * Redirect to dashboard page
      return router.parseUrl('/dashboard');
    }

    return true;
  };
}
