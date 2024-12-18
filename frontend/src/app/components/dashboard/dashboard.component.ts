import { Component, inject } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { UserStore } from '../../../store/user.store';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [ButtonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  readonly userStore = inject(UserStore);
}
