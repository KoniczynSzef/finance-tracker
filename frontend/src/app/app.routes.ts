import { Routes } from '@angular/router';
import {
  redirectToDashboardIfAuthenticated,
  redirectToLoginIfNotAuthenticated,
} from '../auth/auth.guard';
import { LoginFormComponent } from './components/auth/login-form/login-form.component';
import { RegisterFormComponent } from './components/auth/register-form/register-form.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginFormComponent,
    canActivate: [redirectToDashboardIfAuthenticated()],
  },
  {
    path: 'register',
    component: RegisterFormComponent,
    canActivate: [redirectToDashboardIfAuthenticated()],
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [redirectToLoginIfNotAuthenticated()],
  },
];
