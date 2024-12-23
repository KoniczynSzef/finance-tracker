import { Component, signal } from '@angular/core';
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
import { catchError, of } from 'rxjs';
import { AuthService } from '../../../../auth/auth.service';
import { UserStateService } from '../../../../store/user-state.service';
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
    private router: Router,
    private userStateService: UserStateService
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

    this.authService
      .login(payload)
      .pipe(
        catchError((err) => {
          console.log(err);

          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Invalid username or password.',
          });

          this.isSubmitting.set(false);

          return of(null);
        })
      )
      .subscribe((token) => {
        if (!token) return;
        this.authService.saveToken(token);

        this.authService.getCurrentUser().subscribe((user) => {
          this.userStateService.setUser(user);
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'You have been successfully logged in.',
          });

          setTimeout(() => {
            this.userStateService.navigateToDashboard();
          }, 500);
        });
      });
  }
}
