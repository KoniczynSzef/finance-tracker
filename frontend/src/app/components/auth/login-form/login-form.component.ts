import { Component, inject, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { Toast } from 'primeng/toast';
import { AuthService } from '../../../../auth/auth.service';
import { UserStore } from '../../../../store/user.store';
import { Login, LoginForm } from '../../../../types/auth/login.type';
import { FormCardComponent } from '../../forms/form-card/form-card.component';
import { FormRedirectActionComponent } from '../../forms/form-redirect-action/form-redirect-action.component';
import { FormWrapperComponent } from '../../forms/form-wrapper/form-wrapper.component';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    InputTextModule,
    PasswordModule,
    ButtonModule,
    Toast,
    RouterModule,
    FormCardComponent,
    FormRedirectActionComponent,
    FormWrapperComponent,
  ],
  providers: [MessageService],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss',
})
export class LoginFormComponent {
  userStore = inject(UserStore);
  isSubmitting = signal(false);

  loginFormGroup = new FormGroup<LoginForm>({
    username: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
  });

  constructor(
    private messageService: MessageService,
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    this.isSubmitting.set(true);

    const username = this.loginFormGroup.value.username;
    const password = this.loginFormGroup.value.password;

    if (this.loginFormGroup.invalid || !username || !password) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill in all fields!',
        life: 3000,
      });

      return;
    }

    const payload: Login = {
      username,
      password,
    };

    this.authService.login(payload).subscribe((token) => {
      this.authService.saveToken(token);

      this.authService.getCurrentUser().subscribe((user) => {
        if (user) {
          this.userStore.setUser(user);
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'You have been successfully logged in.',
          });

          setTimeout(() => {
            this.router.navigate(['/dashboard']);
          }, 500);
        }
      });
    });
  }
}
