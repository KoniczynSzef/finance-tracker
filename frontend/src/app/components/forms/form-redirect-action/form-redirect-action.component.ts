import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-form-redirect-action',
  standalone: true,
  imports: [ButtonModule, RouterModule],
  templateUrl: './form-redirect-action.component.html',
  styleUrl: './form-redirect-action.component.scss',
})
export class FormRedirectActionComponent {
  @Input() title = '';
  @Input() buttonLabel = '';
  @Input() href = '';
}
