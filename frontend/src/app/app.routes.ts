import { Routes } from '@angular/router';
import { LoginFormComponent } from './components/auth/login-form/login-form/login-form.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginFormComponent,
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
  },
];
