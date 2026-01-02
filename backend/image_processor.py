"""
Image Processing Module
Analyzes uploaded images for mood board interpretation and emotional context.
Uses Google Vision API for image understanding.
"""

import base64
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

# Vision API prompts
MOOD_BOARD_PROMPT = """
Analyze this image as a mood board. Extract the emotional and contextual signals:

1. **Visual Mood**: What emotions does the color palette, composition, and subjects convey?
   - Colors: (e.g., warm/cool, vibrant/muted, contrasting/harmonious)
   - Composition: (e.g., chaotic/organized, crowded/spacious, bright/dark)
   - Subject matter: (e.g., nature, work, social, intimate, public)

2. **Emotional Signals**: Infer emotional context from visual elements
   - Primary emotions: (list top 3)
   - Energy level: (low/medium/high)
   - Time of day/season indicators

3. **Environmental Context**:
   - Location type: (home/office/outdoor/social/other)
   - Activity indicators: (working, relaxing, socializing, exercising, etc.)
   - Social context: (alone/with others)

4. **Health & Wellness Indicators**:
   - Visual wellness markers: (organization level, cleanliness, self-care evidence)
   - Potential stress indicators: (clutter, chaos, dark environment, isolation signals)
   - Energy indicators: (activity level suggestions, movement, engagement)

5. **Confidence Assessment**:
   - How confident are these interpretations? (0.0-1.0)
   - What visual cues support them?

RESPOND WITH STRICT JSON:
{
  "mood_analysis": {
    "visual_mood": {
      "colors": "string",
      "composition": "string",
      "primary_subjects": ["string"]
    },
    "emotional_signals": {
      "primary_emotions": ["string"],
      "energy_level": "low|medium|high",
      "emotional_intensity": 0.5
    },
    "environmental_context": {
      "location_type": "string",
      "activity_indicators": ["string"],
      "social_context": "alone|with_others|unclear"
    },
    "wellness_indicators": {
      "wellness_markers": ["string"],
      "stress_indicators": ["string"],
      "energy_indicators": ["string"]
    },
    "interpretation_confidence": 0.75,
    "summary": "2-3 sentence interpretation of mood/state"
  }
}

RETURN ONLY JSON. NO OTHER TEXT.
"""


def encode_image_to_base64(image_path: str) -> str:
    """
    Encode image file to base64 for Gemini Vision API.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Base64 encoded image string
    """
    with open(image_path, "rb") as image_file:
        return base64.standard_b64encode(image_file.read()).decode("utf-8")


def get_image_media_type(file_path: str) -> str:
    """
    Determine MIME type from file extension.
    
    Args:
        file_path: Path to image file
        
    Returns:
        MIME type (e.g., 'image/jpeg')
    """
    ext = Path(file_path).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    return mime_types.get(ext, "image/jpeg")


async def analyze_mood_board(image_path: str) -> Dict[str, Any]:
    """
    Analyze uploaded image as mood board for emotional/contextual signals.
    
    Args:
        image_path: Path to uploaded image file
        
    Returns:
        Dict with mood_analysis, emotional_signals, environment_context, etc.
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        json.JSONDecodeError: If Gemini response isn't valid JSON
        ValueError: If image format is not supported
    """
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Validate file extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    if Path(image_path).suffix.lower() not in valid_extensions:
        raise ValueError(f"Unsupported image format. Supported: {valid_extensions}")
    
    try:
        import asyncio
        
        # Run the synchronous Gemini API call in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def _analyze():
            from gemini_service import call_gemini_rest_api
            media_type = get_image_media_type(image_path)
            
            logger.info(f"Analyzing mood board for: {Path(image_path).name}")
            
            # Read and encode image
            with open(image_path, "rb") as f:
                image_bytes = f.read()
                image_base64 = base64.standard_b64encode(image_bytes).decode("utf-8")
            
            logger.info(f"Image size: {len(image_bytes)} bytes, base64: {len(image_base64)} chars")
            
            # Call Gemini REST API with proper structure
            response = call_gemini_rest_api(
                contents=[{
                    "role": "user",
                    "parts": [
                        {"text": MOOD_BOARD_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": media_type,
                                "data": image_base64,
                            }
                        }
                    ]
                }],
                temperature=1.0,
                max_tokens=2000
            )
            
            return response
        
        # Execute in thread pool
        response_text = await loop.run_in_executor(None, _analyze)
        
        # Parse JSON response
        response_text = response_text.strip()
        
        # Try to extract JSON if wrapped in text
        if response_text.startswith("{"):
            mood_analysis = json.loads(response_text)
        else:
            # Look for JSON block
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                mood_analysis = json.loads(json_match.group())
            else:
                logger.warning(f"Could not extract JSON from response: {response_text[:200]}")
                raise json.JSONDecodeError("No JSON found in response", response_text, 0)
        
        logger.info(f"✓ Analyzed mood board: {Path(image_path).name}")
        return mood_analysis
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error analyzing image: {e}")
        raise ValueError(f"Failed to parse Gemini response: {str(e)}")
    except Exception as e:
        logger.error(f"Error analyzing mood board: {str(e)}", exc_info=True)
        raise


async def extract_visual_context(image_path: str) -> Dict[str, Any]:
    """
    Extract basic visual context from image (simplified analysis).
    Useful for quick context before full mood board analysis.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dict with basic visual information
    """
    simple_prompt = """
    Briefly describe this image in terms of:
    1. Setting/location
    2. Primary activities or subjects
    3. Lighting/brightness level
    4. Overall mood (happy/sad/calm/energetic/stressful)
    
    Keep responses concise. Return as JSON:
    {
      "setting": "string",
      "activities": ["string"],
      "lighting": "bright|moderate|dim",
      "mood": "string"
    }
    
    RETURN ONLY JSON.
    """
    
    try:
        image_data = encode_image_to_base64(image_path)
        media_type = get_image_media_type(image_path)
        
        response = client.models.generate_content(
            model=MODEL,
            contents=[{
                "role": "user",
                "parts": [
                    {"text": simple_prompt},
                    {
                        "inline_data": {
                            "mime_type": media_type,
                            "data": image_data
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
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        
        return {"error": "Could not parse response"}
    
    except Exception as e:
        logger.error(f"Error extracting visual context: {str(e)}")
        return {"error": str(e)}


# Example usage documentation
"""
USAGE IN main.py:

from image_processor import analyze_mood_board, extract_visual_context

@app.post("/analyze")
async def analyze(
    text: str = Form(...),
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # ... existing validation ...
    
    # Save image if provided
    image_description = None
    if image:
        image_filename = f"img_{datetime.utcnow().timestamp()}_{image.filename}"
        image_path = UPLOADS_DIR / image_filename
        with open(image_path, "wb") as f:
            f.write(await image.read())
        
        # Analyze mood board
        try:
            mood_analysis = await analyze_mood_board(str(image_path))
            image_description = json.dumps(mood_analysis)
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            # Continue with text-only analysis
    
    # Pass image_description to Gemini in analyze_checkin()
    # ... rest of endpoint ...
"""
