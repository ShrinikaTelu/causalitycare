"""CausalityCare API Server - Multimodal Analysis with Timeouts"""

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
import json
import asyncio
from pathlib import Path

from config import settings
from database import init_db, get_db, CheckInRecord
from schemas import CheckInRequest, CheckInResponse, CausalityResponse, extract_json, validate_response
from gemini_service import analyze_checkin
from prompts import DEFAULT_PROMPT

try:
    from image_processor import analyze_mood_board
    from audio_processor import analyze_voice_sentiment
    MULTIMODAL_ENABLED = True
except ImportError as e:
    MULTIMODAL_ENABLED = False
    print(f"⚠ Warning: Multimodal processing not available: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_PROCESSING_TIMEOUT = 30
AUDIO_PROCESSING_TIMEOUT = 40
TEXT_PROCESSING_TIMEOUT = 20
MAX_FILE_SIZE_MB = 50

app = FastAPI(title="CausalityCare API", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
def startup_event():
    logger.info("Initializing database...")
    init_db()
    logger.info(f"✓ Database ready | Multimodal: {'ENABLED' if MULTIMODAL_ENABLED else 'DISABLED'}")


@app.get("/health")
def health_check():
    from config import settings
    return {
        "status": "healthy",
        "multimodal_enabled": MULTIMODAL_ENABLED,
        "gemini_api_key_configured": settings.gemini_api_key is not None,
        "version": "2.1.0"
    }


@app.post("/analyze")
async def analyze(
    text: str = Form(...),
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Main endpoint: analyze text + optional image/audio with timeouts."""
    
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text input required")
    
    start_time = datetime.utcnow()
    image_filename = None
    audio_filename = None
    mood_board_analysis = None
    voice_sentiment_analysis = None
    audio_transcript = None
    
    try:
        # Save image if provided
        if image:
            try:
                content = await image.read()
                file_size_mb = len(content) / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    raise ValueError(f"Image too large: {file_size_mb:.1f}MB")
                
                image_filename = f"img_{int(datetime.utcnow().timestamp())}_{image.filename}"
                with open(UPLOADS_DIR / image_filename, "wb") as f:
                    f.write(content)
                logger.info(f"✓ Saved image: {image_filename}")
            except Exception as e:
                logger.error(f"✗ Image save failed: {e}")
                raise HTTPException(status_code=400, detail=f"Image save failed: {str(e)}")
        
        # Save audio if provided
        if audio:
            try:
                content = await audio.read()
                file_size_mb = len(content) / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    raise ValueError(f"Audio too large: {file_size_mb:.1f}MB")
                
                audio_filename = f"aud_{int(datetime.utcnow().timestamp())}_{audio.filename}"
                with open(UPLOADS_DIR / audio_filename, "wb") as f:
                    f.write(content)
                logger.info(f"✓ Saved audio: {audio_filename}")
            except Exception as e:
                logger.error(f"✗ Audio save failed: {e}")
                raise HTTPException(status_code=400, detail=f"Audio save failed: {str(e)}")
        
        # Process image with timeout
        if image_filename and MULTIMODAL_ENABLED:
            try:
                logger.info(f"→ Processing image: {image_filename}")
                result = await asyncio.wait_for(
                    analyze_mood_board(str(UPLOADS_DIR / image_filename)),
                    timeout=IMAGE_PROCESSING_TIMEOUT
                )
                mood_board_analysis = result
                logger.info(f"✓ Image analysis complete: {result.get('mood_analysis', {}).get('summary', 'No summary')[:100]}")
            except asyncio.TimeoutError:
                logger.warning(f"⚠ Image analysis timeout after {IMAGE_PROCESSING_TIMEOUT}s")
                mood_board_analysis = None
            except Exception as e:
                logger.warning(f"⚠ Image analysis error: {e}")
                mood_board_analysis = None
        
        # Process audio with timeout
        if audio_filename and MULTIMODAL_ENABLED:
            try:
                logger.info(f"→ Processing audio: {audio_filename}")
                result = await asyncio.wait_for(
                    analyze_voice_sentiment(str(UPLOADS_DIR / audio_filename)),
                    timeout=AUDIO_PROCESSING_TIMEOUT
                )
                voice_sentiment_analysis = result
                audio_transcript = result.get("transcription", "")
                logger.info(f"✓ Audio analysis complete: '{audio_transcript[:100]}...'")
            except asyncio.TimeoutError:
                logger.warning(f"⚠ Audio analysis timeout after {AUDIO_PROCESSING_TIMEOUT}s")
                voice_sentiment_analysis = None
                audio_transcript = None
            except Exception as e:
                logger.warning(f"⚠ Audio analysis error: {e}")
                voice_sentiment_analysis = None
                audio_transcript = None
        
        # Text analysis with timeout
        combined_input = text
        if audio_transcript:
            combined_input = f"{text}\n\n[Voice Transcription]:\n{audio_transcript}"
        
        try:
            logger.info(f"→ Analyzing text ({len(combined_input)} chars)...")
            response_text = await asyncio.wait_for(
                asyncio.to_thread(
                    analyze_checkin,
                    combined_input,
                    audio_transcript,
                    json.dumps(mood_board_analysis) if mood_board_analysis else None
                ),
                timeout=TEXT_PROCESSING_TIMEOUT
            )
            logger.info(f"✓ Text analysis done")
        except asyncio.TimeoutError:
            logger.error(f"✗ Text analysis timeout")
            raise HTTPException(status_code=504, detail="Analysis timeout. Try again.")
        except Exception as e:
            logger.error(f"✗ Text analysis error: {e}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
        # Parse response
        try:
            parsed_json = extract_json(response_text)
            analysis = validate_response(parsed_json)
            logger.info(f"✓ Response validated")
        except Exception as e:
            logger.error(f"✗ Response validation error: {e}")
            raise HTTPException(status_code=422, detail=f"Invalid AI response: {str(e)}")
        
        # Store in database
        try:
            db_record = CheckInRecord(
                user_input=text,
                audio_transcript=audio_transcript,
                image_filename=image_filename,
                audio_filename=audio_filename,
                mood_board_analysis=mood_board_analysis,
                voice_sentiment_analysis=voice_sentiment_analysis,
                has_image=image_filename is not None,
                has_audio=audio_filename is not None,
                summary=analysis.summary,
                symptoms=analysis.symptoms,
                triggers=analysis.triggers,
                environment_factors=analysis.environment_factors,
                causal_chains=[
                    {"from": c.from_, "to": c.to, "why": c.why, "confidence": c.confidence}
                    for c in analysis.causal_chains
                ],
                uncertainties=analysis.uncertainties,
                questions=analysis.questions,
                micro_actions=analysis.micro_actions,
                self_harm_detected=analysis.safety_flags.self_harm,
                urgent_flag=analysis.safety_flags.urgent,
                gemini_raw_response=response_text
            )
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
            logger.info(f"✓ Check-in #{db_record.id} stored")
        except Exception as e:
            logger.error(f"✗ Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save: {str(e)}")
        
        # Build response
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        response_data = {
            "id": db_record.id,
            "data": analysis.model_dump(by_alias=True),
            "safety_alert": analysis.safety_flags.urgent,
            "created_at": db_record.created_at.isoformat(),
            "processing_time_seconds": elapsed
        }
        
        if mood_board_analysis and "error" not in mood_board_analysis:
            response_data["mood_board"] = mood_board_analysis
        if voice_sentiment_analysis and "error" not in voice_sentiment_analysis:
            response_data["voice_sentiment"] = voice_sentiment_analysis
        
        logger.info(f"✓ Complete in {elapsed:.1f}s")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")


@app.get("/history")
def get_history(days: int = 7, db: Session = Depends(get_db)):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    records = db.query(CheckInRecord).filter(
        CheckInRecord.created_at >= cutoff_date
    ).order_by(CheckInRecord.created_at.desc()).all()
    
    return {
        "total_checkins": len(records),
        "period_days": days,
        "checkins": [
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "summary": r.summary,
                "urgent_flag": r.urgent_flag
            }
            for r in records
        ]
    }


@app.get("/trends")
def detect_trends(days: int = 14, db: Session = Depends(get_db)):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    records = db.query(CheckInRecord).filter(
        CheckInRecord.created_at >= cutoff_date
    ).all()
    
    if not records:
        return {"period_days": days, "total_checkins": 0}
    
    symptom_counts = {}
    trigger_counts = {}
    
    for record in records:
        for symptom in record.symptoms:
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        for trigger in record.triggers:
            trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
    
    return {
        "period_days": days,
        "total_checkins": len(records),
        "most_common_symptoms": sorted(
            [(s, c) for s, c in symptom_counts.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5],
        "most_common_triggers": sorted(
            [(t, c) for t, c in trigger_counts.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
    }


@app.get("/checkin/{checkin_id}")
def get_checkin(checkin_id: int, db: Session = Depends(get_db)):
    record = db.query(CheckInRecord).filter(CheckInRecord.id == checkin_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Check-in not found")
    
    return {
        "id": record.id,
        "created_at": record.created_at.isoformat(),
        "summary": record.summary,
        "causal_chains": record.causal_chains,
        "micro_actions": record.micro_actions
    }


@app.get("/debug/multimodal")
def debug_multimodal():
    """Debug endpoint to check multimodal support and available processors."""
    return {
        "multimodal_enabled": MULTIMODAL_ENABLED,
        "image_processor_available": MULTIMODAL_ENABLED,
        "audio_processor_available": MULTIMODAL_ENABLED,
        "image_timeout_seconds": IMAGE_PROCESSING_TIMEOUT,
        "audio_timeout_seconds": AUDIO_PROCESSING_TIMEOUT,
        "text_timeout_seconds": TEXT_PROCESSING_TIMEOUT,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "gemini_model": "gemini-3-pro-preview",
        "uploads_directory": str(UPLOADS_DIR),
        "uploads_exist": UPLOADS_DIR.exists()
    }


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT") == "development"
    print("=" * 60)
    print("🚀 CausalityCare API v2.1.0")
    print(f"✓ Multimodal: {'ENABLED' if MULTIMODAL_ENABLED else 'DISABLED'}")
    print(f"✓ Port: {port}")
    print("=" * 60)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=reload)
