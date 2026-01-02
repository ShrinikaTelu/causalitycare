# 🚀 Gemini 3 Pro API Integration

## Overview
CausalityCare is fully integrated with **Google Gemini 3 Pro API** (Early Access) for advanced multimodal analysis of emotional wellbeing and causal reasoning.

## Model Used
- **Model**: `gemini-3-pro-preview`
- **Status**: Early Access (Hackathon Program)
- **Availability**: Through official Gemini API with early access credentials

## Integration Points

### 1. Text Analysis (`gemini_service.py`)
```python
MODEL = "gemini-3-pro-preview"
GEMINI_REST_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"
```
- Analyzes journal entries and user input
- Returns structured JSON with causal chains
- Processing time: 11-20 seconds

### 2. Image Analysis (`image_processor.py`)
```python
MODEL = "gemini-3-pro-preview"
```
- Analyzes mood boards and uploaded images
- Extracts emotional signals and wellness indicators
- Processing time: 15-30 seconds

### 3. Audio Analysis (`audio_processor.py`)
```python
MODEL = "gemini-3-pro-preview"
```
- Transcribes and analyzes voice sentiment
- Detects emotional tone, stress indicators, and energy levels
- Processing time: 20-40 seconds

## Features Leveraged

### Multimodal Capabilities
- ✅ **Text Analysis**: Journal entries, personal notes
- ✅ **Image Understanding**: Mood boards, photos, visual context
- ✅ **Audio Processing**: Voice transcription, sentiment analysis, emotional tone

### Advanced Reasoning
- **Causal Analysis**: Identifies root causes of stress and anxiety
- **Confidence Scoring**: Provides 0.0-1.0 confidence on each causal link
- **Structured Output**: Returns JSON with validated schema
- **Safety Detection**: Flags urgent mental health concerns

## API Integration Details

### Request Format
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent
Authorization: key={GEMINI_API_KEY}
Content-Type: application/json

{
  "contents": [{
    "role": "user",
    "parts": [{
      "text": "User input with analysis prompts"
    }]
  }],
  "generationConfig": {
    "temperature": 1.0,
    "maxOutputTokens": 2048
  }
}
```

### Response Format
```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "text": "{\"summary\": \"...\", \"causal_chains\": [...]}"
      }]
    }
  }]
}
```

## Performance Metrics

| Analysis Type | Time | Tokens |
|---|---|---|
| Text Only | 11-20s | ~2000 |
| Text + Image | 40-50s | ~4000 |
| Text + Audio | 35-45s | ~3500 |
| Text + Image + Audio | 60-70s | ~5000 |

## Frontend Timeout Configuration
- **Timeout**: 120 seconds (2 minutes)
- **Operator**: RxJS timeout in `causality.service.ts`
- **Reason**: Multimodal analysis can take 50-70 seconds

## Configuration

### Environment Variable
```bash
GEMINI_API_KEY=<your-early-access-api-key>
```

### Backend Settings
- Model: `gemini-3-pro-preview`
- API Version: v1beta
- Temperature: 1.0 (balanced creativity and consistency)
- Max Tokens: 2048

## Usage in Application

### 1. User Submits Check-in
```
Text: "I feel overwhelmed..."
Image: (optional mood board)
Audio: (optional voice note)
```

### 2. Backend Processing
```
gemini_service.py → analyze_checkin()
├── Text Analysis (11-20s)
├── Image Analysis (if provided, +15-30s)
├── Audio Analysis (if provided, +20-40s)
└── Response Validation & Storage
```

### 3. Response to Frontend
```json
{
  "id": 52,
  "data": {
    "summary": "Causal analysis...",
    "symptoms": ["feeling overwhelmed"],
    "triggers": ["work deadlines"],
    "causal_chains": [{
      "from": "Work deadlines",
      "to": "Feeling overwhelmed",
      "why": "...",
      "confidence": 0.9
    }],
    "micro_actions": ["..."],
    "safety_flags": {"self_harm": false, "urgent": false}
  },
  "mood_board": {...},
  "voice_sentiment": {...},
  "processing_time_seconds": 25.3
}
```

## Safety & Compliance

✅ **Crisis Detection**: Flags self-harm and urgent concerns  
✅ **Structured Reasoning**: Causal chains with confidence scores  
✅ **Transparent Uncertainty**: Questions mark ambiguities  
✅ **Professional-Ready**: Designed for human mental health follow-up  

## Limitations & Future Work

### Current Limitations
- Audio processing requires transcription before analysis
- Image analysis is contextual, not diagnostic
- No real-time streaming (request-response only)

### Future Enhancements
- Streaming responses for faster UX
- Multi-turn conversations for deeper analysis
- Pattern recognition across historical data
- Integration with mental health resources

## Testing

### Quick Test
```bash
curl -X POST http://localhost:8000/analyze \
  -F "text=I am feeling stressed about work" \
  -F "image=@mood_board.jpg" \
  -F "audio=@voice_note.m4a"
```

### Expected Response Time
- Text only: ~15 seconds
- With multimodal: ~60 seconds

## References

- **Gemini API Docs**: https://ai.google.dev/docs
- **Model Card**: Gemini 3 Pro (Early Access)
- **API Endpoint**: v1beta

---

**Built with Gemini 3 Pro for the Hackathon 🎊**
