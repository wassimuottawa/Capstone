import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackletComponent } from './tracklet.component';

describe('TrackletComponent', () => {
  let component: TrackletComponent;
  let fixture: ComponentFixture<TrackletComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TrackletComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TrackletComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
