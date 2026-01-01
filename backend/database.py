from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./causalitycare.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================================================
# Database Models
# ============================================================================

class CheckInRecord(Base):
    """Stores daily check-in entries with Gemini analysis results."""
    __tablename__ = "check_ins"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    user_input = Column(String, nullable=False)
    audio_transcript = Column(String, nullable=True)
    image_filename = Column(String, nullable=True)
    audio_filename = Column(String, nullable=True)
    
    # Analysis results (stored as JSON)
    summary = Column(String, nullable=False)
    symptoms = Column(JSON, default=list)  # List[str]
    triggers = Column(JSON, default=list)  # List[str]
    environment_factors = Column(JSON, default=list)  # List[str]
    causal_chains = Column(JSON, default=list)  # List[dict]
    uncertainties = Column(JSON, default=list)  # List[str]
    questions = Column(JSON, default=list)  # List[str]
    micro_actions = Column(JSON, default=list)  # List[str]
    
    # Safety flags
    self_harm_detected = Column(Boolean, default=False)
    urgent_flag = Column(Boolean, default=False)
    
    # Multimodal analysis data
    mood_board_analysis = Column(JSON, nullable=True)  # Image mood analysis
    voice_sentiment_analysis = Column(JSON, nullable=True)  # Audio sentiment analysis
    
    # Metadata
    gemini_raw_response = Column(String, nullable=True)  # For debugging
    has_image = Column(Boolean, default=False, index=True)
    has_audio = Column(Boolean, default=False, index=True)


class Template(Base):
    """User-created causal analysis templates for reuse."""
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)  # Future: FK to users table
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Template definition
    prompt_template = Column(String, nullable=False)  # Customizable prompt
    expected_symptoms = Column(JSON, default=list)  # Suggested symptoms
    expected_triggers = Column(JSON, default=list)  # Suggested triggers
    environment_factors = Column(JSON, default=list)  # Common environmental factors
    micro_action_templates = Column(JSON, default=list)  # Reusable actions
    
    # Usage
    is_public = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)


class TrendAnalysis(Base):
    """Aggregated trends over time periods (weekly, monthly)."""
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    period_start = Column(DateTime, nullable=False, index=True)
    period_end = Column(DateTime, nullable=False)
    period_type = Column(String, default="weekly")  # weekly|monthly|custom
    
    # Aggregated data
    total_checkins = Column(Integer, default=0)
    avg_stress_level = Column(Float, default=0.0)
    
    # Top symptoms/triggers (stored as JSON for flexibility)
    top_symptoms = Column(JSON, default=list)
    top_triggers = Column(JSON, default=list)
    top_environment_factors = Column(JSON, default=list)
    
    # Patterns detected
    patterns = Column(JSON, default=list)  # Detected causal patterns
    cycles_detected = Column(JSON, default=list)  # Time-based cycles
    
    # Predictions
    predicted_high_stress_days = Column(JSON, default=list)
    risk_indicators = Column(JSON, default=list)
    
    # Safety
    crisis_events = Column(Integer, default=0)
    urgent_flags = Column(Integer, default=0)
    
    # Analysis metadata
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting DB session in FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
