import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserStore } from '../store/user.store';

export function redirectToLoginIfNotAuthenticated(): CanActivateFn {
  return () => {
    const user = inject(UserStore).user();
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
    const user = inject(UserStore).user();
    const router = inject(Router);

    if (user) {
      // * Redirect to dashboard page
      return router.parseUrl('/dashboard');
    }

    return true;
  };
}
