import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { Toast } from 'primeng/toast';
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
  ],
  providers: [MessageService],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.scss',
})
export class RegisterFormComponent {
  isSubmitting = false;
  registerFormGroup: FormGroup;
  value: string = '';

  constructor(
    private formBuilder: FormBuilder,
    private messageService: MessageService
  ) {
    this.registerFormGroup = this.formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      //   email: ['', [Validators.required, Validators.email]],
      //   password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit() {
    this.isSubmitting = true;
    const username = this.registerFormGroup.value.username;
    const email = this.registerFormGroup.value.email;
    const password = this.registerFormGroup.value.password;

    if (this.registerFormGroup.invalid) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill in all fields!',
        life: 3000,
      });

      return;
    }
  }
}
