import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { catchError, of } from 'rxjs';
import { AuthService } from '../../../../../auth/auth.service';
import { ResponseError } from '../../../../../types/auth/response-error.type';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [ReactiveFormsModule, InputTextModule, PasswordModule, ButtonModule],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss',
})
export class LoginFormComponent implements OnInit {
  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.authService
      .getCurrentUser()
      .pipe(catchError(() => of()))
      .subscribe(() => {
        console.log('Logged in!');
        this.router.navigate(['/']);
      });
  }

  loginFormGroup = new FormGroup({
    username: new FormControl<string>(''),
    password: new FormControl<string>(''),
  });

  // TODO: Add validation

  onSubmit() {
    const username = this.loginFormGroup.value.username;
    const password = this.loginFormGroup.value.password;

    if (!username || !password) {
      return;
    }

    this.authService.login(username, password).subscribe({
      next: (res) => {
        this.authService.saveTokenInLocalStorage(res);
        this.router.navigate(['/']);
      },
      error: (err: ResponseError) => {
        alert(err.error.detail);
      },
    });
  }
}
