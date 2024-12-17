import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormRedirectActionComponent } from './form-redirect-action.component';

describe('FormRedirectActionComponent', () => {
  let component: FormRedirectActionComponent;
  let fixture: ComponentFixture<FormRedirectActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormRedirectActionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormRedirectActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
