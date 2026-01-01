from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import json
import re
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# Request/Response Models
# ============================================================================

class CheckInRequest(BaseModel):
    """User check-in input."""
    text: str
    audio_transcript: Optional[str] = None
    image_base64: Optional[str] = None


class CausalChain(BaseModel):
    """Single causal relationship with 'from' alias for JSON compatibility."""
    from_: str = Field(alias="from")
    to: str
    why: str
    confidence: float  # 0.0 to 1.0
    
    class Config:
        populate_by_name = True  # Allow both 'from' and 'from_'


class SafetyFlags(BaseModel):
    """Safety checks for mental health risks."""
    self_harm: bool = False
    urgent: bool = False


class CausalityResponse(BaseModel):
    """Structured output from Gemini - matches forced JSON schema."""
    summary: str
    symptoms: List[str] = []
    triggers: List[str] = []
    environment_factors: List[str] = []
    causal_chains: List[CausalChain] = []
    uncertainties: List[str] = []
    questions: List[str] = []
    micro_actions: List[str] = []
    safety_flags: SafetyFlags = Field(default_factory=SafetyFlags)
    
    class Config:
        populate_by_name = True


class CheckInResponse(BaseModel):
    """Complete check-in with analysis."""
    id: int
    created_at: datetime
    user_input: str
    analysis: CausalityResponse
    
    class Config:
        from_attributes = True


# ============================================================================
# MULTIMODAL ANALYSIS SCHEMAS
# ============================================================================

class MoodAnalysis(BaseModel):
    """Image mood board analysis results."""
    visual_mood: dict = Field(default_factory=dict)
    emotional_signals: dict = Field(default_factory=dict)
    environmental_context: dict = Field(default_factory=dict)
    wellness_indicators: dict = Field(default_factory=dict)
    interpretation_confidence: float = 0.0
    summary: str = ""


class VoiceAnalysis(BaseModel):
    """Audio voice sentiment and emotion analysis."""
    transcription: str = ""
    voice_analysis: dict = Field(default_factory=dict)
    emotional_sentiment: dict = Field(default_factory=dict)
    stress_indicators: dict = Field(default_factory=dict)
    content_emotion_match: bool = True
    incongruences: List[str] = []
    analysis_confidence: float = 0.0
    summary: str = ""


class MultimodalAnalysis(BaseModel):
    """Complete multimodal analysis combining text, image, and audio."""
    text_analysis: CausalityResponse
    mood_board: Optional[MoodAnalysis] = None
    voice_sentiment: Optional[VoiceAnalysis] = None
    integration_summary: str = ""
    
    class Config:
        from_attributes = True


class MultimodalCheckInResponse(BaseModel):
    """Complete check-in response with multimodal data."""
    id: int
    created_at: datetime
    user_input: str
    multimodal: MultimodalAnalysis
    safety_alert: bool = False
    
    class Config:
        from_attributes = True


# ============================================================================
# JSON Extraction & Validation (Failsafe)
# ============================================================================

def extract_json(text: str) -> dict:
    """
    Safely extract the first JSON object from a string.
    
    Handles cases where Gemini accidentally wraps JSON in text.
    
    Args:
        text: Raw response from Gemini
    
    Returns:
        Parsed JSON dictionary
    
    Raises:
        ValueError: If no valid JSON found or parsing fails
    """
    # Try direct JSON parse first (common case)
    text = text.strip()
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    
    # Find first {...} JSON block (handles wrapped text)
    match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL)
    if not match:
        logger.error(f"No JSON object found in response: {text[:200]}")
        raise ValueError("No JSON object found in model response.")
    
    raw_json = match.group(0)
    logger.debug(f"Extracted JSON: {raw_json[:200]}")
    
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}\nJSON: {raw_json[:300]}")
        raise ValueError(f"Invalid JSON in response: {e}")


def validate_response(data: dict) -> CausalityResponse:
    """
    Validate and coerce Gemini response to CausalityResponse.
    
    Handles missing fields, type coercion, and missing safety flags.
    
    Args:
        data: Parsed JSON from Gemini
    
    Returns:
        Validated CausalityResponse object
    
    Raises:
        ValueError: If validation fails
    """
    try:
        # Ensure safety_flags exist
        if "safety_flags" not in data:
            data["safety_flags"] = {"self_harm": False, "urgent": False}
        
        # Coerce empty/missing lists
        for key in ["symptoms", "triggers", "environment_factors", "uncertainties", "questions", "micro_actions", "causal_chains"]:
            if key not in data:
                data[key] = []
            elif not isinstance(data[key], list):
                data[key] = []
        
        # Validate with Pydantic
        response = CausalityResponse.model_validate(data)
        logger.info(f"Validated response: {len(response.causal_chains)} causal chains, urgent={response.safety_flags.urgent}")
        return response
    
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise ValueError(f"Response validation failed: {e}")
