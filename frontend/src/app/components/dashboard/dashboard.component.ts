import { Component, inject } from '@angular/core';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { Toast } from 'primeng/toast';
import { AuthService } from '../../../auth/auth.service';
import { UserStateService } from '../../../store/user-state.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [ButtonModule, Toast],
  providers: [MessageService],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  userStateService = inject(UserStateService);
  authService = inject(AuthService);
  messageService = inject(MessageService);

  user = this.userStateService.state$().user;

  logout() {
    this.authService.logout();
    this.userStateService.unsetUser();

    this.messageService.add({
      severity: 'success',
      summary: 'Success',
      detail: 'You have been successfully logged out.',
      life: 3000,
    });

    setTimeout(() => {
      this.userStateService.navigateToLogin();
    }, 500);
  }
}
