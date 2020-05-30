import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorbannerComponent } from './errorbanner.component';

describe('ErrorbannerComponent', () => {
  let component: ErrorbannerComponent;
  let fixture: ComponentFixture<ErrorbannerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ErrorbannerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ErrorbannerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
