import {
  Component,
  Input,
  AfterViewInit,
  ElementRef,
  ViewChild,
  OnChanges,
  SimpleChanges,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CausalityResponse, MoodBoard, VoiceSentiment } from '../../services/causality.service';

// Dynamic import to avoid module resolution issues
let Network: any;

interface VisNode {
  id: string;
  label: string;
  group: 'symptom' | 'trigger' | 'environment';
  title?: string;
  color?: string;
}

interface VisEdge {
  from: string;
  to: string;
  label: string;
  title?: string;
}

@Component({
  selector: 'app-causal-graph',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="graph-container">
      <h3>Causal Map (Click nodes for details)</h3>
      <div #networkContainer class="network-canvas"></div>
      <div class="legend">
        <div class="legend-item">
          <div class="legend-color" style="background: #ff6b6b"></div>
          <span>Symptoms</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: #ffa502"></div>
          <span>Triggers</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: #4f9ff0"></div>
          <span>Environment</span>
        </div>
      </div>
    </div>

    <!-- Image Analysis Section -->
    <div *ngIf="moodBoard" class="mood-board-section">
      <h3>📸 Image Analysis</h3>
      
      <div class="mood-board-content">
        <!-- Visual Mood -->
        <div *ngIf="moodBoard.visual_mood" class="analysis-card visual-mood">
          <h4>Visual Mood</h4>
          <p><strong>Colors:</strong> {{ moodBoard.visual_mood.colors }}</p>
          <p><strong>Composition:</strong> {{ moodBoard.visual_mood.composition }}</p>
          <p *ngIf="moodBoard.visual_mood.primary_subjects.length > 0">
            <strong>Elements:</strong> {{ moodBoard.visual_mood.primary_subjects.join(', ') }}
          </p>
        </div>

        <!-- Emotional Signals -->
        <div *ngIf="moodBoard.emotional_signals" class="analysis-card emotional-signals">
          <h4>Emotional Signals</h4>
          <p *ngIf="moodBoard.emotional_signals.primary_emotions.length > 0">
            <strong>Emotions:</strong> {{ moodBoard.emotional_signals.primary_emotions.join(', ') }}
          </p>
          <p><strong>Energy:</strong> {{ moodBoard.emotional_signals.energy_level }}</p>
          <p><strong>Intensity:</strong> {{ (moodBoard.emotional_signals.emotional_intensity * 100).toFixed(0) }}%</p>
        </div>

        <!-- Environmental Context -->
        <div *ngIf="moodBoard.environmental_context" class="analysis-card environmental">
          <h4>Environment</h4>
          <p><strong>Location:</strong> {{ moodBoard.environmental_context.location_type }}</p>
          <p *ngIf="moodBoard.environmental_context.activity_indicators.length > 0">
            <strong>Activities:</strong> {{ moodBoard.environmental_context.activity_indicators.join(', ') }}
          </p>
        </div>

        <!-- Wellness Indicators -->
        <div *ngIf="moodBoard.wellness_indicators" class="analysis-card wellness">
          <h4>Wellness Indicators</h4>
          <p *ngIf="moodBoard.wellness_indicators.stress_indicators.length > 0">
            <strong>Stress Signs:</strong> {{ moodBoard.wellness_indicators.stress_indicators.join(', ') }}
          </p>
          <p>{{ moodBoard.wellness_indicators.overall_assessment }}</p>
        </div>

        <!-- Summary & Confidence -->
        <div class="analysis-card summary">
          <p><em>{{ moodBoard.summary }}</em></p>
          <p class="confidence">Confidence: {{ (moodBoard.interpretation_confidence * 100).toFixed(0) }}%</p>
        </div>
      </div>
    </div>

    <!-- Audio Analysis Section -->
    <div *ngIf="voiceSentiment" class="voice-sentiment-section">
      <h3>🎵 Audio Analysis</h3>
      
      <div class="voice-sentiment-content">
        <div class="analysis-card voice-card">
          <p><strong>Tone:</strong> {{ voiceSentiment.tone }}</p>
          <p><strong>Pace:</strong> {{ voiceSentiment.pace }}</p>
          <p><strong>Volume:</strong> {{ voiceSentiment.volume }}</p>
          <p><strong>Clarity:</strong> {{ voiceSentiment.clarity }}</p>
          <p><strong>Energy Level:</strong> {{ voiceSentiment.energy_level }}</p>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      .graph-container {
        margin: 24px 0;
      }

      .graph-container h3 {
        margin: 0 0 12px 0;
        color: #222;
      }

      .network-canvas {
        width: 100%;
        height: 400px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background: white;
      }

      .legend {
        display: flex;
        gap: 20px;
        margin-top: 12px;
        font-size: 0.9rem;
        color: #666;
      }

      .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 50%;
      }

      /* Image Analysis Styles */
      .mood-board-section,
      .voice-sentiment-section {
        margin-top: 24px;
        padding: 16px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #fafafa;
      }

      .mood-board-section h3,
      .voice-sentiment-section h3 {
        color: #333;
        margin: 0 0 16px 0;
        font-size: 18px;
      }

      .mood-board-content,
      .voice-sentiment-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 12px;
      }

      .analysis-card {
        padding: 12px;
        background-color: white;
        border-left: 4px solid #4CAF50;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      }

      .analysis-card h4 {
        margin: 0 0 10px 0;
        color: #2c3e50;
        font-size: 14px;
        font-weight: 700;
      }

      .analysis-card p {
        margin: 5px 0;
        font-size: 13px;
        color: #555;
        line-height: 1.4;
      }

      .visual-mood {
        border-left-color: #FF6B6B;
      }

      .emotional-signals {
        border-left-color: #FFA500;
      }

      .environmental {
        border-left-color: #4ECDC4;
      }

      .wellness {
        border-left-color: #95E1D3;
      }

      .voice-card {
        border-left-color: #9B59B6;
      }

      .summary {
        grid-column: 1 / -1;
        border-left-color: #3498DB;
        background-color: #f5f5f5;
      }

      .summary p {
        margin: 8px 0;
      }

      .confidence {
        font-size: 12px;
        color: #666;
        margin-top: 10px !important;
        font-style: italic;
      }

      strong {
        color: #1a1a1a;
        font-weight: 600;
      }
    `,
  ],
})
export class CausalGraphComponent implements AfterViewInit, OnChanges {
  @Input() data?: CausalityResponse;
  @Input() moodBoard?: MoodBoard;
  @Input() voiceSentiment?: VoiceSentiment;
  @ViewChild('networkContainer') container?: ElementRef<HTMLDivElement>;
  
  private network?: any;

  ngAfterViewInit(): void {
    // Render immediately if data is already available
    if (this.data && this.container) {
      this.renderGraph();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Re-render when data changes after initial load
    if (changes['data'] && !changes['data'].firstChange) {
      // Wait for DOM to be ready before rendering
      setTimeout(() => {
        if (this.container && this.data) {
          this.renderGraph();
        }
      }, 50);
    }
  }

  private renderGraph(): void {
    // Double-check container exists before proceeding
    if (!this.data || !this.container?.nativeElement) {
      console.warn('Cannot render graph: missing data or container');
      return;
    }

    const nodeMap = new Map<string, VisNode>();
    const edges: VisEdge[] = [];

    // Create nodes from causal chains
    this.data.causal_chains.forEach((chain) => {
      // Determine group for "from" node
      let fromGroup: 'symptom' | 'trigger' | 'environment' = 'trigger';
      if (this.data!.symptoms.includes(chain.from)) {
        fromGroup = 'symptom';
      } else if (this.data!.environment_factors.includes(chain.from)) {
        fromGroup = 'environment';
      }

      // Determine group for "to" node
      let toGroup: 'symptom' | 'trigger' | 'environment' = 'trigger';
      if (this.data!.symptoms.includes(chain.to)) {
        toGroup = 'symptom';
      } else if (this.data!.environment_factors.includes(chain.to)) {
        toGroup = 'environment';
      }

      // Create or update nodes
      if (!nodeMap.has(chain.from)) {
        nodeMap.set(chain.from, {
          id: chain.from,
          label: chain.from,
          group: fromGroup,
          title: `${chain.from} (${fromGroup})`,
          color: this.getColorForGroup(fromGroup),
        });
      }

      if (!nodeMap.has(chain.to)) {
        nodeMap.set(chain.to, {
          id: chain.to,
          label: chain.to,
          group: toGroup,
          title: `${chain.to} (${toGroup})`,
          color: this.getColorForGroup(toGroup),
        });
      }

      // Create edge
      edges.push({
        from: chain.from,
        to: chain.to,
        label: `${Math.round(chain.confidence * 100)}%`,
        title: chain.why,
      });
    });

    // Convert to vis-network format
    const nodes = Array.from(nodeMap.values());
    const visNodes = nodes.map((n) => ({
      id: n.id,
      label: n.label,
      color: n.color,
      title: n.title,
      font: { size: 14 },
      physics: true,
    }));

    const visEdges = edges.map((e) => ({
      from: e.from,
      to: e.to,
      label: e.label,
      title: e.title,
      arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      font: { size: 11, align: 'middle' },
      smooth: { type: 'curvedCW' },
    }));

    // Destroy existing network if present
    if (this.network) {
      this.network.destroy();
      this.network = undefined;
    }

    // Dynamically import Network class
    import('vis-network').then((visModule) => {
      // Create network instance
      this.network = new visModule.Network(
        this.container!.nativeElement,
        { nodes: visNodes, edges: visEdges } as any,
        {
          interaction: {
            hover: true,
            navigationButtons: true,
            keyboard: true,
          },
          physics: {
            enabled: true,
            stabilization: {
              iterations: 200,
            },
            barnesHut: {
              gravitationalConstant: -26000,
              centralGravity: 0.3,
              springLength: 200,
            },
          },
          nodes: {
            shape: 'box',
            widthConstraint: {
              maximum: 200,
            },
            font: {
              multi: true,
              align: 'center',
            },
          },
        } as any
      );

      // Stabilize network only after it's created
      if (this.network && typeof this.network.once === 'function') {
        this.network.once('stabilizationIterationsDone', () => {
          this.network?.setOptions({ physics: false });
        });
      }
    }).catch((error) => {
      console.error('Failed to load vis-network:', error);
    });
  }

  private getColorForGroup(group: 'symptom' | 'trigger' | 'environment'): string {
    switch (group) {
      case 'symptom':
        return '#ff6b6b';
      case 'trigger':
        return '#ffa502';
      case 'environment':
        return '#4f9ff0';
    }
  }
}
