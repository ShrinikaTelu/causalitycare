import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import 'hammerjs';

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient()],
}).catch((err) => {
  console.error('Bootstrap error:', err);
  const root = document.querySelector('app-root');
  if (root) {
    root.innerHTML = `<div style="padding: 20px; color: red; font-family: monospace;">
      <h3>Application Error</h3>
      <p>${err?.message || 'Unknown error'}</p>
    </div>`;
  }
});
