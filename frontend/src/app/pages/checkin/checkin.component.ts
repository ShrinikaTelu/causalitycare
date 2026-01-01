import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CausalityService, CausalityResponse, MoodBoard, VoiceSentiment } from '../../services/causality.service';
import { CausalGraphComponent } from '../../components/causal-graph/causal-graph.component';
import { SafetyBannerComponent } from '../../components/safety-banner/safety-banner.component';

@Component({
  selector: 'app-checkin',
  standalone: true,
  imports: [CommonModule, FormsModule, CausalGraphComponent, SafetyBannerComponent],
  template: `
    <div class="page">
      <!-- Hero Header -->
      <header class="hero">
        <div class="hero__text">
          <div class="hero__brand">
            <svg class="hero__heart" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#a855f7;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
                </linearGradient>
              </defs>
              <path d="M50 85 C25 70, 10 60, 10 45 C10 35, 18 28, 28 28 C35 28, 42 32, 50 40 C58 32, 65 28, 72 28 C82 28, 90 35, 90 45 C90 60, 75 70, 50 85 Z" 
                    fill="none" stroke="url(#heartGradient)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span class="hero__brandName">CausalityCare</span>
          </div>
          <h1>Daily Check-in</h1>
          <p class="subtitle">
            Share a few lines (and optionally a photo/voice note). We'll map <b>possible causes</b> → <b>effects</b> and suggest small, humane next steps.
          </p>

          <div class="meta">
            <div class="pill">2–10 lines is perfect</div>
            <div class="pill">Not medical advice</div>
            <div class="pill">Private by default</div>
          </div>
        </div>

      </header>

      <!-- Main Content -->
      <main class="content">
        <!-- Left: Form -->
        <section class="card card--primary">
          <div class="card__header">
            <h2>What's on your mind?</h2>
            <p class="hint">Be specific: sleep, caffeine, deadlines, conflicts, environment, body signals.</p>
          </div>

          <label class="label" for="text">Your note</label>
          <textarea
            id="text"
            [(ngModel)]="text"
            name="text"
            rows="7"
            class="textarea"
            placeholder="Example: Feeling anxious today. Slept at 2am, had 3 coffees, lots of deadlines. Couldn't focus this morning..."
            (input)="updateCharCount()"
          ></textarea>

          <div class="charCount">{{ charCount }} / 800 characters</div>

          <!-- Preset chips -->
          <div class="presetChips">
            <button type="button" class="chip" (click)="insertPreset('Sleep')">Sleep</button>
            <button type="button" class="chip" (click)="insertPreset('Work')">Work</button>
            <button type="button" class="chip" (click)="insertPreset('Health')">Health</button>
            <button type="button" class="chip" (click)="insertPreset('Relationships')">Relationships</button>
          </div>

          <!-- Upload tiles -->
          <div class="uploadGrid">
            <!-- Photo tile -->
            <div class="uploadTile" 
              (dragover)="onDragOver($event)" 
              (drop)="onDrop($event, 'image')"
              (dragleave)="onDragLeave($event)">
              <div class="uploadTile__icon">🖼️</div>
              <div class="uploadTile__body">
                <div class="uploadTile__title">Workspace photo</div>
                <div class="uploadTile__sub">Optional • JPG/PNG</div>
              </div>

              <label class="uploadTile__cta">
                <input type="file" accept="image/*" (change)="onFileChange($event, 'image')" />
                Choose file
              </label>

              <div class="uploadTile__file" *ngIf="imageFile">
                <span class="dot"></span> {{ imageFile.name }}
                <button type="button" class="linkBtn" (click)="imageFile = undefined">Remove</button>
              </div>
            </div>

            <!-- Audio tile -->
            <div class="uploadTile"
              (dragover)="onDragOver($event)"
              (drop)="onDrop($event, 'audio')"
              (dragleave)="onDragLeave($event)">
              <div class="uploadTile__icon">🎙️</div>
              <div class="uploadTile__body">
                <div class="uploadTile__title">Voice note</div>
                <div class="uploadTile__sub">Optional • 30–90 sec</div>
              </div>

              <label class="uploadTile__cta">
                <input type="file" accept="audio/*" (change)="onFileChange($event, 'audio')" />
                Choose file
              </label>

              <div class="uploadTile__file" *ngIf="audioFile">
                <span class="dot"></span> {{ audioFile.name }}
                <button type="button" class="linkBtn" (click)="audioFile = undefined">Remove</button>
              </div>
            </div>
          </div>

          <div class="actions">
            <button
              class="btn btn--primary"
              (click)="submit()"
              [disabled]="loading || !text.trim()"
            >
              <span *ngIf="!loading">Analyze my day</span>
              <span *ngIf="loading" class="spinner" aria-hidden="true"></span>
              <span *ngIf="loading">Analyzing…</span>
            </button>

            <div class="tinyNote">
              We'll show a causal map with confidence and 1–3 questions if needed.
            </div>
          </div>
        </section>

        <!-- Right: Care + Safety -->
        <aside class="card card--info">
          <div class="card__header row">
            <div>
              <h2>Care & Safety</h2>
              <p class="hint">CausalityCare is reflection support — not therapy or medical advice.</p>
            </div>
            <button type="button" class="chipBtn" (click)="showSafety = !showSafety">
              {{ showSafety ? 'Hide' : 'Show' }} resources
            </button>
          </div>

                    <div class="safety" *ngIf="showSafety">
            <p class="safety__lead">If you're in a mental health crisis or thinking about self-harm, please seek immediate help:</p>
            <ul class="safety__list">
              <li><b>US:</b> Call or text <b>988</b> (Suicide & Crisis Lifeline)</li>
              <li><b>Text Crisis:</b> Text <b>HOME</b> to <b>741741</b> (Crisis Text Line)</li>
              <li><b>International:</b> <a href="https://www.iasp.info/resources/Crisis_Centres/" target="_blank" rel="noopener">IASP Crisis Centers</a></li>
            </ul>
            <p class="safety__foot">💚 Your wellbeing matters. Reaching out takes courage, and we're here to support you.</p>
          </div>

          <div class="mini">
            <div class="mini__title">What you'll get</div>
            <ul class="mini__list">
              <li>Symptoms vs triggers vs environment</li>
              <li>Causal chain map with confidence</li>
              <li>2–5 micro-actions (low effort)</li>
              <li>Questions if we're uncertain</li>
            </ul>
          </div>
        </aside>
      </main>

      <!-- Results Section -->
      <div *ngIf="result && !loading" class="results">
        <h2>Your Causal Map</h2>

        <!-- Safety alert -->
        <div *ngIf="result.safety_flags.urgent" class="alert alert-urgent">
          <strong>We care about your wellbeing.</strong> If you're experiencing thoughts of self-harm or
          suicide, please reach out to:
          <ul>
            <li>National Suicide Prevention Lifeline: 988 (US)</li>
            <li>Crisis Text Line: Text HOME to 741741</li>
            <li>International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/</li>
          </ul>
        </div>

        <!-- Summary -->
        <div class="summary-card">
          <h3>Summary</h3>
          <p>{{ result.summary }}</p>
        </div>

        <!-- Causal graph -->
        <app-causal-graph [data]="result" [moodBoard]="moodBoard" [voiceSentiment]="voiceSentiment"></app-causal-graph>

        <!-- Symptoms, triggers, environment -->
        <div class="factors-grid">
          <div class="factor-card symptoms">
            <h4>Symptoms (How you feel)</h4>
            <ul>
              <li *ngFor="let s of result.symptoms">{{ s }}</li>
            </ul>
          </div>

          <div class="factor-card triggers">
            <h4>Triggers (What happened)</h4>
            <ul>
              <li *ngFor="let t of result.triggers">{{ t }}</li>
            </ul>
          </div>

          <div class="factor-card environment">
            <h4>Environment (Your context)</h4>
            <ul>
              <li *ngFor="let e of result.environment_factors">{{ e }}</li>
            </ul>
          </div>
        </div>

        <!-- Micro actions -->
        <div class="micro-actions-card">
          <h3>What You Can Try Today</h3>
          <p class="hint">(Start with just one—no pressure!)</p>
          <ul class="micro-actions">
            <li *ngFor="let action of result.micro_actions" class="action-item">
              ✓ {{ action }}
            </li>
          </ul>
        </div>

        <!-- Questions -->
        <div *ngIf="result.questions.length > 0" class="questions-card">
          <h3>To Better Understand You</h3>
          <ul>
            <li *ngFor="let q of result.questions">{{ q }}</li>
          </ul>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        color: #0f172a;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      }

      .page {
        min-height: 100vh;
        padding: 28px 18px 48px;
        background:
          radial-gradient(1200px 600px at 15% 10%, rgba(99,102,241,.16), transparent 60%),
          radial-gradient(900px 500px at 90% 20%, rgba(34,197,94,.14), transparent 60%),
          linear-gradient(180deg, #f8fafc 0%, #ffffff 40%, #ffffff 100%);
      }

      .hero {
        max-width: 1100px;
        margin: 0 auto 18px;
        padding: 22px 22px;
        border-radius: 20px;
        display: grid;
        grid-template-columns: 1fr;
        gap: 18px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 14px 40px rgba(2, 6, 23, 0.08);
        background-image: url('/assets/hero-bg.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        backdrop-filter: blur(8px);
        position: relative;
      }
      
      .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background: rgba(255,255,255,.15);
        border-radius: 20px;
        pointer-events: none;
      }
      
      .hero__text {
        position: relative;
        z-index: 1;
      }

      .hero__text h1 {
        margin: 8px 0 8px;
        font-size: 42px;
        letter-spacing: -0.03em;
        color: rgba(15,23,42,.95);
        text-shadow: 0 2px 8px rgba(255,255,255,.4);
      }

      .subtitle {
        margin: 0 0 14px;
        color: rgba(15,23,42,.80);
        line-height: 1.45;
        text-shadow: 0 1px 3px rgba(255,255,255,.3);
      }

      .badge {
        display: inline-flex;
        align-items: center;
        padding: 7px 10px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 12px;
        background: rgba(99,102,241,.10);
        border: 1px solid rgba(99,102,241,.25);
        color: #3730a3;
      }

      .hero__brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 20px;
        animation: slideInDown 0.6s ease-out;
      }

      .hero__heart {
        width: 56px;
        height: 56px;
        flex-shrink: 0;
        animation: heartbeat 1.5s ease-in-out infinite, slideInDown 0.6s ease-out;
      }

      .hero__brandName {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.9) 0%, rgba(59, 130, 246, 0.85) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
      }

      .meta {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }

      .pill {
        padding: 8px 10px;
        border-radius: 999px;
        font-size: 12px;
        border: 1px solid rgba(15,23,42,.10);
        background: rgba(255,255,255,.8);
        color: rgba(15,23,42,.70);
      }
      
      .pill:nth-child(1) {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.35);
        color: rgba(15, 100, 60, 0.85);
      }
      
      .pill:nth-child(2) {
        background: rgba(249, 115, 22, 0.15);
        border: 1px solid rgba(249, 115, 22, 0.35);
        color: rgba(120, 53, 15, 0.85);
      }
      
      .pill:nth-child(3) {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.35);
        color: rgba(29, 78, 216, 0.85);
      }

      .hero__art {
        position: relative;
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(15,23,42,.08);
        background-image: url('/assets/hero-bg.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 250px;
      }

      .hero__art::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image: url('/assets/hero-accent.png');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: top right;
        pointer-events: none;
        opacity: 0.95;
      }

      .orb { position: absolute; border-radius: 50%; filter: blur(1px); opacity: 0; display: none; }
      .orb--1 { width: 180px; height: 180px; left: -40px; top: -40px; background: rgba(99,102,241,.35); }
      .orb--2 { width: 140px; height: 140px; right: -30px; top: 30px; background: rgba(34,197,94,.25); }
      .orb--3 { width: 220px; height: 220px; right: 30px; bottom: -90px; background: rgba(14,165,233,.18); }

      .grid {
        position: absolute;
        inset: 0;
        background-image: linear-gradient(rgba(15,23,42,.06) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(15,23,42,.06) 1px, transparent 1px);
        background-size: 28px 28px;
        mask-image: radial-gradient(circle at 50% 50%, rgba(0,0,0,.9), transparent 70%);
        opacity: 0;
        display: none;
      }

      .content {
        max-width: 1100px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1.4fr .9fr;
        gap: 18px;
        align-items: flex-start;
      }

      .card {
        border-radius: 20px;
        border: 1px solid rgba(15,23,42,.10);
        background: rgba(255,255,255,.88);
        box-shadow: 0 14px 40px rgba(2, 6, 23, 0.07);
        padding: 18px;
        animation: fadeIn 0.5s ease-out, slideUp 0.6s ease-out;
      }
      
      .card--info {
        background: linear-gradient(135deg, rgba(219, 234, 254, 0.6) 0%, rgba(240, 253, 250, 0.6) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 14px 40px rgba(59, 130, 246, 0.08);
      }

      .card__header h2 {
        margin: 0 0 4px;
        font-size: 18px;
        letter-spacing: -0.01em;
      }

      .hint {
        margin: 0;
        color: rgba(15,23,42,.62);
        font-size: 13px;
      }

      .row {
        display: flex;
        justify-content: space-between;
        gap: 14px;
        align-items: flex-start;
      }

      .label {
        display: block;
        margin: 16px 0 8px;
        font-weight: 600;
        font-size: 13px;
        color: rgba(15,23,42,.78);
      }

      .textarea {
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(15,23,42,.12);
        padding: 14px 14px;
        font-size: 14px;
        line-height: 1.5;
        outline: none;
        background: rgba(255,255,255,.9);
        transition: box-shadow .15s ease, border-color .15s ease;
        font-family: inherit;
      }

      .textarea:focus {
        border-color: rgba(99,102,241,.55);
        box-shadow: 0 0 0 4px rgba(99,102,241,.14);
      }

      .charCount {
        font-size: 12px;
        color: rgba(15,23,42,.60);
        margin: 8px 0 16px 0;
      }

      .presetChips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 14px;
      }

      .chip {
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid rgba(99,102,241,.30);
        background: rgba(99,102,241,.08);
        color: #3730a3;
        font-weight: 600;
        font-size: 12px;
        cursor: pointer;
        transition: all .2s ease;
      }

      .chip:hover {
        background: rgba(99,102,241,.15);
        border-color: rgba(99,102,241,.50);
      }

      .uploadGrid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 14px;
      }

      .uploadTile {
        border-radius: 16px;
        border: 1px dashed rgba(15,23,42,.18);
        background: rgba(248,250,252,.9);
        padding: 14px;
        animation: fadeIn 0.5s ease-out;
        transition: all 0.3s ease;
        display: grid;
        grid-template-columns: 34px 1fr;
        column-gap: 10px;
        row-gap: 10px;
        align-items: center;
        transition: all .2s ease;
        cursor: grab;
      }

      .uploadTile:hover {
        border-color: rgba(99,102,241,.35);
        background: rgba(99,102,241,.05);
      }

      .uploadTile__icon {
        font-size: 22px;
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border-radius: 12px;
        background: rgba(99,102,241,.10);
        border: 1px solid rgba(99,102,241,.22);
      }

      .uploadTile__title { font-weight: 700; font-size: 13px; }
      .uploadTile__sub { color: rgba(15,23,42,.60); font-size: 12px; margin-top: 2px; }

      .uploadTile__cta {
        grid-column: 1 / -1;
        justify-self: start;
        padding: 9px 11px;
        border-radius: 12px;
        background: rgba(15,23,42,.06);
        border: 1px solid rgba(15,23,42,.10);
        cursor: pointer;
        font-size: 12px;
        font-weight: 600;
        transition: all .2s ease;
      }

      .uploadTile__cta:hover {
        background: rgba(99,102,241,.10);
        border-color: rgba(99,102,241,.25);
      }

      .uploadTile__cta input { display: none; }

      .uploadTile__file {
        grid-column: 1 / -1;
        font-size: 12px;
        color: rgba(15,23,42,.75);
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .dot {
        width: 8px; height: 8px; border-radius: 999px;
        background: rgba(34,197,94,.9);
      }

      .linkBtn {
        border: none;
        background: transparent;
        color: rgba(99,102,241,.95);
        font-weight: 700;
        cursor: pointer;
        padding: 0;
      }

      .actions {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 16px;
      }

      .btn {
        border: none;
        border-radius: 14px;
        padding: 12px 14px;
        font-weight: 800;
        cursor: pointer;
      }

      .btn--primary {
        min-width: 180px;
        color: white;
        background: linear-gradient(135deg, #4f46e5, #22c55e);
        box-shadow: 0 14px 30px rgba(79,70,229,.18);
        transition: all .2s ease;
      }

      .btn--primary:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 18px 40px rgba(79,70,229,.25);
      }

      .btn--primary:disabled {
        opacity: .55;
        cursor: not-allowed;
        filter: grayscale(25%);
      }

      .tinyNote {
        font-size: 12px;
        color: rgba(15,23,42,.62);
        line-height: 1.35;
      }

      .spinner {
        width: 14px;
        height: 14px;
        border-radius: 999px;
        border: 2px solid rgba(255,255,255,.55);
        border-top-color: rgba(255,255,255,1);
        display: inline-block;
        margin-right: 8px;
        animation: spin 0.8s linear infinite;
      }

      @keyframes spin { to { transform: rotate(360deg); } }

      .chipBtn {
        border: 1px solid rgba(59, 130, 246, 0.25);
        background: rgba(59, 130, 246, 0.08);
        border-radius: 999px;
        padding: 8px 12px;
        font-weight: 700;
        font-size: 12px;
        cursor: pointer;
        transition: all .2s ease;
        color: rgba(59, 130, 246, 0.85);
      }

      .chipBtn:hover {
        background: rgba(59, 130, 246, 0.12);
        border-color: rgba(59, 130, 246, 0.4);
        color: rgba(59, 130, 246, 1);
      }

      .safety { overflow: visible; min-width: 0; }
      .safety__lead { margin: 0 0 14px; color: rgba(15,23,42,.80); font-weight: 600; font-size: 14px; }
      .safety__list { margin: 0 0 16px; padding-left: 0; color: rgba(15,23,42,.80); font-size: 14px; list-style: none; display: flex; flex-direction: column; gap: 10px; }
      .safety__list li { display: flex; gap: 12px; align-items: center; overflow: visible; flex-wrap: nowrap; white-space: nowrap; }
      .safety__list li::before { flex-shrink: 0; font-weight: bold; font-size: 18px; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; }
      .safety__list li:nth-child(1)::before { content: '🏥'; }
      .safety__list li:nth-child(2)::before { content: '💬'; }
      .safety__list li:nth-child(3)::before { content: '🌍'; }
      .safety__list b { font-weight: 700; color: rgba(15,23,42,.95); }
      .safety__list a { color: rgba(59, 130, 246, 0.85); text-decoration: none; font-weight: 700; }
      .safety__list a:hover { text-decoration: underline; color: rgba(59, 130, 246, 1); }
      .safety__foot { margin-top: 16px; font-weight: 700; color: rgba(59, 130, 246, 0.85); font-size: 14px; line-height: 1.5; }

      .mini {
        margin-top: 14px;
        padding: 14px;
        border-radius: 16px;
        animation: fadeIn 0.6s ease-out;
        border: 1px solid rgba(59, 130, 246, 0.25);
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(34, 197, 94, 0.05) 100%);
      }

      .mini__title { font-weight: 800; margin-bottom: 8px; font-size: 14px; color: rgba(15,23,42,.85); }
      .mini__list { margin: 0; padding-left: 18px; color: rgba(15,23,42,.75); font-size: 13px; }
      .mini__list li { margin: 8px 0; display: flex; gap: 8px; }
      .mini__list li::before { content: '✓'; color: rgba(34, 197, 94, 0.75); font-weight: bold; flex-shrink: 0; }

      .results {
        max-width: 1100px;
        margin: 40px auto 0;
        animation: fadeIn 0.3s ease;
      }

      .results h2 {
        font-size: 28px;
        margin: 0 0 20px 0;
      }

      .alert {
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid;
      }

      .alert-urgent {
        background: #fef3f3;
        border-color: #e74c3c;
        color: #c0392b;
      }

      .alert-urgent strong {
        display: block;
        margin-bottom: 8px;
      }

      .alert-urgent ul {
        margin: 8px 0 0 20px;
        padding: 0;
      }

      .summary-card {
        background: #f0f7ff;
        border-left: 4px solid #4f9ff0;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 24px;
      }

      .summary-card h3 {
        margin: 0 0 12px 0;
        color: #222;
      }

      .summary-card p {
        margin: 0;
        color: #555;
        line-height: 1.6;
      }

      .factors-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin: 24px 0;
      }

      .factor-card {
        border-radius: 8px;
        padding: 16px;
      }

      .factor-card h4 {
        margin: 0 0 12px 0;
        font-size: 1rem;
        color: white;
      }

      .factor-card ul {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      .factor-card li {
        padding: 6px 0;
        color: white;
        font-size: 0.95rem;
      }

      .symptoms {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
      }

      .triggers {
        background: linear-gradient(135deg, #ffa502, #ff7e04);
      }

      .environment {
        background: linear-gradient(135deg, #4f9ff0, #2e7fd4);
      }

      .micro-actions-card {
        background: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 24px 0;
      }

      .micro-actions-card h3 {
        margin: 0 0 8px 0;
        color: #222;
      }

      .micro-actions {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      .action-item {
        background: white;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-radius: 6px;
        border-left: 3px solid #4f9ff0;
        color: #333;
      }

      .questions-card {
        background: #fafafa;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 24px 0;
      }

      .questions-card h3 {
        margin: 0 0 16px 0;
        color: #222;
      }

      .questions-card ul {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      .questions-card li {
        padding: 8px 0 8px 24px;
        position: relative;
        color: #666;
      }

      .questions-card li:before {
        content: '❓';
        position: absolute;
        left: 0;
      }

      @media (max-width: 940px) {
        .hero, .content { grid-template-columns: 1fr; }
        .hero__art { height: 170px; }
        .uploadGrid { grid-template-columns: 1fr; }
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      @keyframes slideInDown {
        from {
          opacity: 0;
          transform: translateY(-20px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      
      @keyframes slideUp {
        from {
          opacity: 0;
          transform: translateY(20px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        14% { transform: scale(1.15); }
        28% { transform: scale(1); }
      }
    `,
  ],
})
export class CheckinComponent implements OnInit {
  text = '';
  imageFile?: File;
  audioFile?: File;
  charCount = 0;
  showSafety = false;

  loading = false;
  result?: CausalityResponse;
  moodBoard?: MoodBoard;
  voiceSentiment?: VoiceSentiment;
  error?: string;

  constructor(private api: CausalityService) {}

  ngOnInit(): void {
    // Check API health
    this.api.health().subscribe({
      error: () => {
        this.error =
          'Backend API not available. Make sure FastAPI is running on http://localhost:8000';
      },
    });
  }

  updateCharCount(): void {
    this.charCount = this.text.length;
  }

  insertPreset(topic: string): void {
    const presets: { [key: string]: string } = {
      Sleep: 'Not enough sleep. Woke up at ',
      Work: 'Work is overwhelming. Too many deadlines, ',
      Health: 'Feeling physically unwell. ',
      Relationships: 'Had a conflict with someone. ',
    };

    if (this.text) {
      this.text += ' ' + presets[topic];
    } else {
      this.text = presets[topic];
    }
    this.updateCharCount();
  }

  onDragOver(e: DragEvent): void {
    e.preventDefault();
    e.stopPropagation();
  }

  onDragLeave(e: DragEvent): void {
    e.preventDefault();
  }

  onDrop(e: DragEvent, type: 'image' | 'audio'): void {
    e.preventDefault();
    e.stopPropagation();

    const files = e.dataTransfer?.files;
    if (!files?.length) return;

    const file = files[0];

    // Validate file type
    if (type === 'image' && !file.type.startsWith('image/')) {
      alert('Please drop an image file');
      return;
    }
    if (type === 'audio' && !file.type.startsWith('audio/')) {
      alert('Please drop an audio file');
      return;
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      alert('File too large. Max 10MB.');
      return;
    }

    if (type === 'image') {
      this.imageFile = file;
    } else {
      this.audioFile = file;
    }
  }

  onFileChange(e: Event, type: 'image' | 'audio'): void {
    const input = e.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      alert('File too large. Max 10MB.');
      return;
    }

    if (type === 'image') {
      this.imageFile = file;
    } else {
      this.audioFile = file;
    }
  }

  submit(): void {
    if (!this.text.trim()) {
      alert('Please write something first!');
      return;
    }

    const formData = new FormData();
    formData.append('text', this.text);

    if (this.imageFile) {
      formData.append('image', this.imageFile);
    }
    if (this.audioFile) {
      formData.append('audio', this.audioFile);
    }

    this.loading = true;
    this.error = undefined;

    this.api.analyze(formData).subscribe({
      next: (response) => {
        this.result = response.data;
        this.moodBoard = response.mood_board;
        this.voiceSentiment = response.voice_sentiment;
        this.loading = false;

        // Scroll to results
        setTimeout(() => {
          const resultsEl = document.querySelector('.results');
          resultsEl?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Failed to analyze. Please try again.';
        console.error(err);
      },
    });
  }
}
