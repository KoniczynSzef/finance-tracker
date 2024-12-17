import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-form-card',
  standalone: true,
  imports: [],
  templateUrl: './form-card.component.html',
  styleUrl: './form-card.component.scss'
})
export class FormCardComponent {
    @Input() title = ""
    @Input() description = ""
}
