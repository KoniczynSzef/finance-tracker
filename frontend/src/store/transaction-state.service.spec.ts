import { TestBed } from '@angular/core/testing';

import { TransactionStateService } from './transaction-state.service';

describe('TransactionStateService', () => {
  let service: TransactionStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TransactionStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
