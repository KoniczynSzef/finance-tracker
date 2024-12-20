import { Component, inject, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { Toast } from 'primeng/toast';
import { catchError, of } from 'rxjs';
import { AuthService } from '../../../../auth/auth.service';
import { UserStore } from '../../../../store/user.store';
import { Register, RegisterForm } from '../../../../types/auth/register.type';
import { passwordPattern } from '../../../../utils/password-pattern';
import { FormCardComponent } from '../../forms/form-card/form-card.component';
import { FormRedirectActionComponent } from '../../forms/form-redirect-action/form-redirect-action.component';
import { FormWrapperComponent } from '../../forms/form-wrapper/form-wrapper.component';

@Component({
  selector: 'app-register-form',
  standalone: true,
  imports: [
    FormCardComponent,
    PasswordModule,
    InputTextModule,
    ButtonModule,
    FormWrapperComponent,
    Toast,
    FormRedirectActionComponent,
    ReactiveFormsModule,
  ],
  providers: [MessageService],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.scss',
})
export class RegisterFormComponent {
  isSubmitting = signal(false);
  userStore = inject(UserStore);

  registerFormGroup = new FormGroup<RegisterForm>({
    username: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [
        Validators.required,
        Validators.minLength(8),
        Validators.pattern(passwordPattern),
      ],
    }),
  });

  constructor(
    private messageService: MessageService,
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    this.isSubmitting.set(true);

    const payload = this.registerFormGroup.value;

    if (!payload.username || !payload.email || !payload.password) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill in all fields!',
        life: 3000,
      });

      return;
    }

    const userData: Register = {
      username: payload.username,
      password: payload.password,
      email: payload.email,

      // * These fields are not essential for the registration, they will have default values
      full_name: '',
      current_balance: 0,
      balance_threshold: 0,
    };

    this.authService
      .register(userData)
      .pipe(
        catchError((err) => {
          console.log(err);

          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'There was an error registering the user.',
            life: 3000,
          });

          this.isSubmitting.set(false);
          console.log(this.registerFormGroup.value);

          return of(null);
        })
      )
      .subscribe((user) => {
        if (!user) return;

        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'User registered successfully!',
          life: 3000,
        });

        if (!payload.password) return;

        this.authService
          .login({ username: user.username, password: payload.password })
          .subscribe((token) => {
            this.authService.saveToken(token);
          });

        this.userStore.setUser(user);
        this.isSubmitting.set(false);

        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 500);
      });
  }
}
