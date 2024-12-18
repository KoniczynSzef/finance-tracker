import { patchState, signalStore, withMethods, withState } from '@ngrx/signals';
import { User } from '../types/models/user.type';

type UserState = { user: User | null };

const userState: UserState = { user: null };

export const UserStore = signalStore(
  {
    providedIn: 'root',
  },
  withState(userState),
  withMethods((store) => ({
    setUser: (user: User) => patchState(store, { user }),
  }))
);
