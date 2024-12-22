import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { UserStateService } from '../store/user-state.service';

export function redirectToLoginIfNotAuthenticated(): CanActivateFn {
  return () => {
    const userStateService = inject(UserStateService);
    const user = userStateService.state$().user;

    if (!user) {
      // * Redirect to login page
      userStateService.navigateToLogin();
    }

    return true;
  };
}

export function redirectToDashboardIfAuthenticated(): CanActivateFn {
  return () => {
    const userStateService = inject(UserStateService);
    const user = userStateService.state$().user;

    if (user) {
      // * Redirect to dashboard page
      userStateService.navigateToDashboard();
    }

    return true;
  };
}
