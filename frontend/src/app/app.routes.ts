import { Routes } from '@angular/router';
import { LoginFormComponent } from './components/auth/login-form/login-form/login-form.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginFormComponent,
  },
];
