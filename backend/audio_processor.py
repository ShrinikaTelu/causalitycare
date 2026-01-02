"""
Audio Processing Module
Analyzes voice tone, sentiment, and emotional intensity from audio uploads.
Includes transcription and sentiment detection.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from google import genai
from config import settings

logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(api_key=settings.gemini_api_key)
MODEL = "gemini-3-pro-preview"

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".aac": "audio/aac"
}

VOICE_SENTIMENT_PROMPT = """
Analyze this audio recording for voice sentiment and emotional indicators:

TRANSCRIPTION & VOICE ANALYSIS:
1. **Transcription**: Accurate transcription of spoken content
   
2. **Voice Characteristics**:
   - Tone: (confident/hesitant/calm/agitated/sad/happy/neutral)
   - Pace: (slow/moderate/fast, steady/irregular)
   - Volume: (quiet/moderate/loud, consistent/varying)
   - Clarity: (clear/mumbled/emotional breaks/pauses)
   - Energy: (low/medium/high)

3. **Emotional Sentiment**:
   - Primary emotions detected: ["emotion": confidence_score]
   - Overall emotional state: (positive/neutral/negative)
   - Emotional intensity: (0.0-1.0)
   - Emotional trajectory: (improving/degrading/stable)

4. **Stress & Wellbeing Indicators**:
   - Stress signals: (voice tremor, rapid speech, sighing, pauses, silence)
   - Anxiety markers: (hesitation, filler words, self-correction)
   - Wellbeing indicators: (clear speech, enthusiasm, coherence, calmness)
   - Sleep/fatigue indicators: (raspy voice, slow speech, confusion)

5. **Content vs. Delivery Mismatch**:
   - Does emotional tone match content?
   - Any incongruences between words and delivery?

6. **Confidence & Recommendations**:
   - How confident is this analysis? (0.0-1.0)
   - Any concerns about mental health, stress, or wellbeing?
   - Suggested follow-up questions?

RESPOND WITH STRICT JSON:
{
  "transcription": "exact words spoken",
  "voice_analysis": {
    "tone": "string",
    "pace": "slow|moderate|fast",
    "volume": "quiet|moderate|loud",
    "clarity": "string",
    "energy_level": "low|medium|high"
  },
  "emotional_sentiment": {
    "emotions": {
      "emotion_name": 0.85,
      "emotion_name": 0.60
    },
    "overall_sentiment": "positive|neutral|negative",
    "emotional_intensity": 0.65,
    "emotional_trajectory": "improving|stable|degrading"
  },
  "stress_indicators": {
    "stress_signals": ["string"],
    "anxiety_markers": ["string"],
    "wellbeing_indicators": ["string"]
  },
  "content_emotion_match": true,
  "incongruences": ["string"],
  "analysis_confidence": 0.8,
  "summary": "2-3 sentence summary of emotional state and concerns"
}

RETURN ONLY JSON. NO OTHER TEXT.
"""


def get_audio_media_type(file_path: str) -> str:
    """
    Determine MIME type from file extension.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        MIME type (e.g., 'audio/mpeg')
        
    Raises:
        ValueError: If file format not supported
    """
    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_AUDIO_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {ext}. "
            f"Supported: {', '.join(SUPPORTED_AUDIO_FORMATS.keys())}"
        )
    return SUPPORTED_AUDIO_FORMATS[ext]


def read_audio_file(audio_path: str) -> bytes:
    """
    Read audio file as binary data.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Binary audio data
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    with open(audio_path, "rb") as f:
        return f.read()


async def analyze_voice_sentiment(audio_path: str) -> Dict[str, Any]:
    """
    Analyze voice tone, sentiment, and emotional indicators from audio.
    
    Args:
        audio_path: Path to uploaded audio file
        
    Returns:
        Dict with transcription, voice analysis, emotional sentiment, stress indicators
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If format not supported
        json.JSONDecodeError: If response isn't valid JSON
    """
    try:
        import asyncio
        
        # Validate file
        file_path = Path(audio_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Audio not found: {audio_path}")
        
        # Check file size (Gemini has limits, ~100MB typically)
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > 50:
            logger.warning(f"Large audio file: {file_size_mb:.1f}MB. May be truncated.")
        
        # Get media type
        media_type = get_audio_media_type(audio_path)
        
        # Read audio file
        audio_data = read_audio_file(audio_path)
        
        # Run the synchronous Gemini API call in a thread pool
        loop = asyncio.get_event_loop()
        
        def _analyze():
            # Encode audio
            import base64
            audio_base64 = base64.standard_b64encode(audio_data).decode("utf-8")
            
            logger.info(f"Analyzing voice sentiment for: {file_path.name}")
            
            # Use REST API instead of SDK (fixed for multimodal)
            from gemini_service import call_gemini_rest_api
            
            response_text = call_gemini_rest_api(
                contents=[{
                    "role": "user",
                    "parts": [
                        {"text": VOICE_SENTIMENT_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": media_type,
                                "data": audio_base64,
                            }
                        }
                    ]
                }],
                temperature=1.0,
                max_tokens=2000
            )
            
            return response_text
        
        # Execute in thread pool
        response_text = await loop.run_in_executor(None, _analyze)
        
        # Parse JSON response
        response_text = response_text.strip()
        
        if response_text.startswith("{"):
            voice_analysis = json.loads(response_text)
        else:
            # Look for JSON block
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                voice_analysis = json.loads(json_match.group())
            else:
                logger.warning(f"Could not extract JSON from response: {response_text[:200]}")
                raise json.JSONDecodeError("No JSON found in response", response_text, 0)
        
        logger.info(f"✓ Analyzed voice sentiment: {file_path.name}")
        return voice_analysis
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error analyzing audio: {e}")
        raise ValueError(f"Failed to parse Gemini response: {str(e)}")
    except Exception as e:
        logger.error(f"Error analyzing voice sentiment: {str(e)}", exc_info=True)
        raise


async def transcribe_audio(audio_path: str) -> str:
    """
    Quick transcription of audio without full sentiment analysis.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Transcribed text
    """
    try:
        import asyncio
        
        file_path = Path(audio_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Audio not found: {audio_path}")
        
        media_type = get_audio_media_type(audio_path)
        audio_data = read_audio_file(audio_path)
        
        loop = asyncio.get_event_loop()
        
        def _transcribe():
            import base64
            audio_base64 = base64.standard_b64encode(audio_data).decode("utf-8")
            
            logger.info(f"Transcribing audio: {file_path.name}")
            
            response = client.models.generate_content(
                model=MODEL,
                contents=[{
                    "role": "user",
                    "parts": [
                        {
                            "text": "Transcribe this audio accurately. Return ONLY the exact text spoken, no other commentary."
                        },
                        {
                            "inline_data": {
                                "mime_type": media_type,
                                "data": audio_base64
                            }
                        }
                    ]
                }]
            )
            
            return response.text.strip()
        
        return await loop.run_in_executor(None, _transcribe)
    
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}", exc_info=True)
        return f"[Transcription failed: {str(e)}]"


async def extract_voice_mood(audio_path: str) -> Dict[str, Any]:
    """
    Quick voice mood extraction (faster, simpler than full sentiment).
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Dict with quick mood assessment
    """
    simple_prompt = """
    Analyze the speaker's emotional state:
    1. Overall mood: happy/sad/calm/stressed/neutral
    2. Energy level: low/medium/high
    3. Confidence: hesitant/confident
    4. Any major emotion detected
    
    Return JSON:
    {
      "mood": "string",
      "energy": "low|medium|high",
      "confidence": "hesitant|neutral|confident",
      "dominant_emotion": "string"
    }
    
    RETURN ONLY JSON.
    """
    
    try:
        import asyncio
        
        file_path = Path(audio_path)
        media_type = get_audio_media_type(audio_path)
        audio_data = read_audio_file(audio_path)
        
        loop = asyncio.get_event_loop()
        
        def _extract():
            import base64
            audio_base64 = base64.standard_b64encode(audio_data).decode("utf-8")
            
            logger.info(f"Extracting voice mood: {file_path.name}")
            
            response = client.models.generate_content(
                model=MODEL,
                contents=[{
                    "role": "user",
                    "parts": [
                        {"text": simple_prompt},
                        {
                            "inline_data": {
                                "mime_type": media_type,
                                "data": audio_base64
                            }
                        }
                    ]
                }]
            )
            
            response_text = response.text.strip()
            if response_text.startswith("{"):
                return json.loads(response_text)
            else:
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            
            raise ValueError("Could not parse mood JSON from response")
        
        return await loop.run_in_executor(None, _extract)
        
        return {"error": "Could not parse response"}
    
    except Exception as e:
        logger.error(f"Error extracting voice mood: {str(e)}")
        return {"error": str(e)}


# Example usage documentation
"""
USAGE IN main.py:

from audio_processor import analyze_voice_sentiment, transcribe_audio

@app.post("/analyze")
async def analyze(
    text: str = Form(...),
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # ... existing validation and image handling ...
    
    # Handle audio
    audio_description = None
    audio_transcript = None
    if audio:
        audio_filename = f"audio_{datetime.utcnow().timestamp()}_{audio.filename}"
        audio_path = UPLOADS_DIR / audio_filename
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        
        # Transcribe
        try:
            audio_transcript = await transcribe_audio(str(audio_path))
            
            # Analyze sentiment
            voice_analysis = await analyze_voice_sentiment(str(audio_path))
            audio_description = json.dumps(voice_analysis)
        except Exception as e:
            logger.error(f"Audio analysis failed: {str(e)}")
            # Continue with text-only analysis
    
    # Combine inputs for Gemini analysis
    full_context = text
    if audio_transcript:
        full_context += f"\\n\\n[Voice Note]: {audio_transcript}"
    if audio_description:
        full_context += f"\\n\\n[Voice Analysis]: {audio_description}"
    if image_description:
        full_context += f"\\n\\n[Mood Board]: {image_description}"
    
    # Pass full_context to Gemini...
"""
