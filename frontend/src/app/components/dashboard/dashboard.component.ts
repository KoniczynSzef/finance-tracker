import { Component, inject } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { UserStateService } from '../../../store/user-state.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [ButtonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  userStateService = inject(UserStateService);

  user = this.userStateService.state$().user;
}
