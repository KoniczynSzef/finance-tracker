import { Routes } from '@angular/router';
import { LoginFormComponent } from './components/auth/login-form/login-form.component';
import { RegisterFormComponent } from './components/auth/register-form/register-form.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginFormComponent,
  },
  {
    path: 'register',
    component: RegisterFormComponent,
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
  },
];
