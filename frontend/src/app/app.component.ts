import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CheckinComponent } from './pages/checkin/checkin.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, CheckinComponent],
  template: `
    <app-checkin></app-checkin>
  `,
  styles: [
    `
      :host {
        display: block;
      }
    `,
  ],
})
export class AppComponent {}
