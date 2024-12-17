import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-form-wrapper',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './form-wrapper.component.html',
  styleUrl: './form-wrapper.component.scss',
})
export class FormWrapperComponent {
  @Input() formGroup: FormGroup = new FormGroup({});
  @Output() submitOutput = new EventEmitter<void>();

  emitSubmit() {
    this.submitOutput.emit();
  }
}
