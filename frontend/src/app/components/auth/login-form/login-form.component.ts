import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
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
import { ResponseError } from '../../../../types/auth/response-error.type';
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
export class LoginFormComponent implements OnInit {
  isSubmitting = false;
  loginFormGroup: FormGroup;

  constructor(
    private authService: AuthService,
    private router: Router,
    private messageService: MessageService,
    private formBuilder: FormBuilder
  ) {
    this.loginFormGroup = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  ngOnInit() {
    this.authService
      .getCurrentUser()
      .pipe(catchError(() => of()))
      .subscribe(() => {
        console.log('Logged in!');
        this.router.navigate(['/']);
      });
  }

  // TODO: Add validation

  onSubmit() {
    this.isSubmitting = true;
    const username = this.loginFormGroup.value.username;
    const password = this.loginFormGroup.value.password;

    if (this.loginFormGroup.invalid) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill in all fields!',
        life: 3000,
      });

      return;
    }

    this.authService.login(username, password).subscribe({
      next: (res) => {
        this.authService.saveTokenInLocalStorage(res);
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'You are now logged in!',
          life: 3000,
        });

        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 300);
      },
      error: (err: ResponseError) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: err.error.detail,
          life: 3000,
        });
      },
    });

    setTimeout(() => {
      this.isSubmitting = false;
    }, 300);
  }
}
