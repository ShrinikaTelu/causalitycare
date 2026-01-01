from google import genai
from config import settings
import logging
import requests
import json

logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(api_key=settings.gemini_api_key)
MODEL = "gemini-2.0-flash"

# REST API endpoint for vision/multimodal requests
GEMINI_REST_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def call_gemini_rest_api(contents: list, temperature: float = 1.0, max_tokens: int = 2048) -> str:
    """
    Call Gemini API using REST endpoint instead of SDK (fixes image issues with v0.3.0).
    
    Args:
        contents: List of content parts (role, parts with text/image/audio)
        temperature: Sampling temperature
        max_tokens: Maximum output tokens
        
    Returns:
        str: Generated text response
        
    Raises:
        ValueError: If API call fails
    """
    try:
        payload = {
            'contents': contents,
            'generationConfig': {
                'temperature': temperature,
                'maxOutputTokens': max_tokens
            }
        }
        
        url = f"{GEMINI_REST_API_URL}?key={settings.gemini_api_key}"
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code != 200:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get('error', {}).get('message', response.text)
            raise ValueError(f"Gemini API error: {response.status_code} - {error_msg}")
        
        data = response.json()
        if 'candidates' in data and data['candidates']:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            raise ValueError("No response from Gemini API")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to call Gemini API: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Failed to parse Gemini response: {str(e)}")

# Import prompt from prompts module
from prompts import DEFAULT_PROMPT


def analyze_checkin(user_input: str, audio_transcript: str = None, image_description: str = None) -> str:
    """
    Send user input to Gemini 2.0 Flash and return structured causal analysis.
    
    Args:
        user_input: Text journal entry
        audio_transcript: Optional transcribed voice note + analysis
        image_description: Optional JSON description of uploaded photo analysis
    
    Returns:
        str: Raw JSON response from Gemini
    
    Raises:
        ValueError: If Gemini API call fails
    """
    
    # Build the full input with multimodal context
    full_input = user_input
    
    if audio_transcript:
        full_input += f"\n\n[AUDIO ANALYSIS]\nUser also provided a voice note. Consider tone, emotional state, and sentiment from: {audio_transcript}"
    
    if image_description:
        try:
            import json as json_mod
            # Try to parse image description if it's JSON
            if isinstance(image_description, str) and image_description.startswith('{'):
                image_data = json_mod.loads(image_description)
                # Extract key insights from image analysis
                mood_summary = image_data.get('mood_analysis', {}).get('summary', '')
                wellness = image_data.get('mood_analysis', {}).get('wellness_indicators', {})
                stress_indicators = wellness.get('stress_indicators', [])
                if mood_summary or stress_indicators:
                    full_input += f"\n\n[IMAGE ANALYSIS]\nUser uploaded a photo showing: {mood_summary}"
                    if stress_indicators:
                        full_input += f"\nVisual stress indicators: {', '.join(stress_indicators)}"
            else:
                full_input += f"\n\n[IMAGE CONTEXT]\n{image_description}"
        except Exception as e:
            logger.warning(f"Could not parse image description: {e}")
            full_input += f"\n\n[IMAGE CONTEXT]\n{image_description}"
    
    logger.info(f"→ Sending check-in to Gemini ({len(full_input)} chars)")
    
    try:
        # Call Gemini API
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"{DEFAULT_PROMPT}\n\n---USER INPUT---\n{full_input}\n\n---RESPOND WITH JSON ONLY---"
                        }
                    ]
                }
            ]
        )
        
        raw_response = response.text
        logger.info(f"✓ Gemini response received ({len(raw_response)} chars)")
        
        return raw_response
        
    except Exception as e:
        logger.error(f"✗ Error calling Gemini API: {e}", exc_info=True)
        raise ValueError(f"Gemini API error: {str(e)}")
