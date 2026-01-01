import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-safety-banner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="safety-banner">
      <h3>🛡️ A Word About Our Care</h3>
      <p>
        <strong>CausalityCare is a reflection tool, not medical advice or therapy.</strong>
      </p>
      <p>
        We help you understand patterns in your wellbeing through structured reflection. If you're
        experiencing a mental health crisis or thinking about self-harm:
      </p>
      <ul>
        <li>
          <strong>In the US:</strong> Call or text
          <a href="tel:988" target="_blank">988</a> (Suicide & Crisis Lifeline)
        </li>
        <li>
          <strong>Text Crisis:</strong> Text HOME to
          <a href="sms:741741" target="_blank">741741</a> (Crisis Text Line)
        </li>
        <li>
          <strong>Internationally:</strong>
          <a
            href="https://www.iasp.info/resources/Crisis_Centres/"
            target="_blank"
            rel="noopener noreferrer"
          >
            IASP Crisis Centers
          </a>
        </li>
      </ul>
      <p class="closing">
        Your wellbeing matters. Please reach out to someone you trust or a trained professional.
      </p>
    </div>
  `,
  styles: [
    `
      .safety-banner {
        background: #fef3f3;
        border: 1px solid #e8d5d5;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 0;
        border-left: 4px solid #e74c3c;
      }

      .safety-banner h3 {
        margin: 0 0 12px 0;
        color: #c0392b;
        font-size: 1rem;
        font-weight: 700;
      }

      .safety-banner p {
        margin: 0 0 12px 0;
        color: #666;
        line-height: 1.6;
        font-size: 0.95rem;
      }

      .safety-banner strong {
        color: #c0392b;
        font-weight: 600;
      }

      .safety-banner ul {
        list-style: none;
        margin: 12px 0;
        padding: 0;
        color: #666;
      }

      .safety-banner li {
        padding: 6px 0 6px 24px;
        position: relative;
        font-size: 0.95rem;
      }

      .safety-banner li:before {
        content: '•';
        position: absolute;
        left: 0;
        color: #e74c3c;
        font-weight: bold;
      }

      .safety-banner a {
        color: #e74c3c;
        text-decoration: none;
        font-weight: 600;
      }

      .safety-banner a:hover {
        text-decoration: underline;
      }

      .closing {
        margin: 12px 0 0 0;
        font-size: 0.9rem;
        font-style: italic;
        color: #666;
      }
    `,
  ],
})
export class SafetyBannerComponent {}
