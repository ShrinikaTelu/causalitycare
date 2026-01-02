import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { timeout } from 'rxjs/operators';

/**
 * CausalEdge: Single cause → effect relationship
 */
export interface CausalEdge {
  from: string;
  to: string;
  why: string;
  confidence: number;
}

/**
 * SafetyFlags: Mental health risk detection
 */
export interface SafetyFlags {
  self_harm: boolean;
  urgent: boolean;
}

/**
 * MoodBoard: Image analysis results
 */
export interface MoodBoard {
  mood_analysis: {
    visual_mood: {
      colors: string;
      composition: string;
      primary_subjects: string[];
    };
    emotional_signals: {
      primary_emotions: string[];
      energy_level: string;
      emotional_intensity: number;
    };
    environmental_context: {
      location_type: string;
      activity_indicators: string[];
      social_context?: string;
    };
    wellness_indicators: {
      stress_indicators: string[];
      overall_assessment?: string;
      energy_indicators?: string[];
      wellness_markers?: string[];
    };
    summary: string;
    interpretation_confidence: number;
  };
}

/**
 * VoiceSentiment: Audio analysis results
 */
export interface VoiceSentiment {
  tone: string;
  pace: string;
  volume: string;
  clarity: string;
  energy_level: string;
}

/**
 * CausalityResponse: Structured analysis from Gemini
 */
export interface CausalityResponse {
  summary: string;
  symptoms: string[];
  triggers: string[];
  environment_factors: string[];
  causal_chains: CausalEdge[];
  uncertainties: string[];
  questions: string[];
  micro_actions: string[];
  safety_flags: SafetyFlags;
}

/**
 * CheckInResponse: API response from /analyze endpoint
 */
export interface CheckInResponse {
  id: number;
  data: CausalityResponse;
  mood_board?: MoodBoard;
  voice_sentiment?: VoiceSentiment;
  safety_alert: boolean;
  created_at: string;
  processing_time_seconds: number;
}

@Injectable({ providedIn: 'root' })
export class CausalityService {
  private baseUrl = 'http://localhost:8000';
  // Set timeout to 2 minutes for analysis (backend can take 14-60 seconds)
  private readonly ANALYZE_TIMEOUT_MS = 120000;

  constructor(private http: HttpClient) {}

  /**
   * Send check-in (text + optional files) for analysis
   */
  analyze(formData: FormData): Observable<CheckInResponse> {
    return this.http.post<CheckInResponse>(`${this.baseUrl}/analyze`, formData)
      .pipe(timeout(this.ANALYZE_TIMEOUT_MS));
  }

  /**
   * Get history of past check-ins
   */
  history(days: number = 7): Observable<any> {
    return this.http.get(`${this.baseUrl}/history?days=${days}`);
  }

  /**
   * Get trend patterns across multiple check-ins
   */
  trends(days: number = 14): Observable<any> {
    return this.http.get(`${this.baseUrl}/trends?days=${days}`);
  }

  /**
   * Get single check-in detail
   */
  getCheckIn(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/checkin/${id}`);
  }

  /**
   * Health check
   */
  health(): Observable<any> {
    return this.http.get(`${this.baseUrl}/health`);
  }
}
