import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { AuthService } from '../../../../../auth/auth.service';
import { ResponseError } from '../../../../../types/auth/response-error.type';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [ReactiveFormsModule, InputTextModule, PasswordModule, ButtonModule],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss',
})
export class LoginFormComponent {
  constructor(private authService: AuthService) {}

  loginFormGroup = new FormGroup({
    username: new FormControl<string>(''),
    password: new FormControl<string>(''),
  });

  onSubmit() {
    const username = this.loginFormGroup.value.username;
    const password = this.loginFormGroup.value.password;

    if (!username || !password) {
      alert('Please fill in all fields');
      return;
    }

    this.authService.login(username, password).subscribe({
      next: (res) => {
        this.authService.saveTokenInLocalStorage(res);
        console.log('Logged in!');
      },
      error: (err: ResponseError) => {
        console.error(err.error.detail);
      },
    });
  }
}
