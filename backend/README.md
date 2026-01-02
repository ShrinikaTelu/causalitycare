# CausalityCare API Backend

A multimodal AI-powered mental health analysis API that leverages Google Gemini to process text, audio, and image inputs for comprehensive check-in assessments.

## 🎯 Features

- **Multimodal Analysis**: Process text, audio (transcription + sentiment), and image (mood board analysis) in a single check-in
- **AI-Powered Insights**: Utilizes Google Gemini AI for intelligent analysis and personalized responses
- **Real-time Processing**: Async request handling with configurable timeouts for each modality
- **Database Persistence**: SQLite database for storing check-in records and analysis results
- **Health Monitoring**: Built-in health check endpoint with Docker HEALTHCHECK support
- **CORS Enabled**: Configured for frontend integration
- **Production Ready**: Deployed on Railway with automatic health checks

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **AI Engine**: Google Generative AI (Gemini)
- **Database**: SQLAlchemy + SQLite
- **File Processing**: python-multipart, aiofiles
- **Containerization**: Docker
- **Deployment**: Railway

## 📋 Prerequisites

- Python 3.9+
- Google Gemini API Key ([Get it here](https://ai.google.dev))
- Docker (for containerized deployment)

## 🚀 Local Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd causalitycare/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the backend directory:
```bash
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./causalitycare.db
```

Or use the provided template:
```bash
cp .env.example .env
# Edit .env with your values
```

### 4. Run Locally
```bash
python main.py
```

The API will start on `http://localhost:8000`

### 5. Access Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health Check
```
GET /health
```
Returns status of the API server.

### Check-in Analysis
```
POST /checkin
```
Analyzes a check-in with text, audio, and/or image inputs.

**Request Body**:
- `text` (string, optional): Check-in text
- `audio_file` (file, optional): Audio file (.m4a, .wav, etc.)
- `image_file` (file, optional): Image file (.png, .jpg, etc.)

**Response**:
```json
{
  "checkin_id": "uuid",
  "timestamp": "2024-01-02T00:00:00",
  "text_analysis": {...},
  "audio_analysis": {...},
  "image_analysis": {...},
  "overall_assessment": "...",
  "recommendations": [...]
}
```

### Get Check-in History
```
GET /checkins
```
Retrieves all stored check-in records.

## 🐳 Docker Deployment

### Build Locally
```bash
docker build -f Dockerfile -t causalitycare-backend .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e ENVIRONMENT=production \
  causalitycare-backend
```

### System Dependencies
The Dockerfile includes:
- `gcc` - C compiler
- `libffi-dev` - Foreign Function Interface
- `libssl-dev` - SSL/TLS support

## 🚢 Production Deployment (Railway)

### Automatic Deployment
The application is configured for Railway deployment via `railway.json`:
- Uses Dockerfile for building
- Automatically exposes port 8000
- Includes health check for reliability

### Environment Variables on Railway
Set these in your Railway project:
1. `GEMINI_API_KEY` - Your Google Gemini API key
2. `ENVIRONMENT` - Set to `production`
3. `DEBUG` - Set to `false`
4. `PORT` - Railway automatically sets this (default: 8000)

### Health Check Configuration
The Dockerfile includes a health check:
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Start Period**: 5 seconds
- **Retries**: 3

Railway will restart the container if health checks fail continuously.

### Live Deployment URL
Once deployed on Railway:
- **API Base URL**: `https://your-railway-project.up.railway.app`
- **Swagger Docs**: `https://your-railway-project.up.railway.app/docs`
- **Health Check**: `https://your-railway-project.up.railway.app/health`

## ⚙️ Configuration

### Application Settings
All settings are configured via environment variables in `config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | - | Google Gemini API key (required for analysis) |
| `ENVIRONMENT` | development | `development` or `production` |
| `DEBUG` | true | Enable debug mode |
| `DATABASE_URL` | sqlite:///./causalitycare.db | Database connection string |
| `API_HOST` | 0.0.0.0 | Server bind address |
| `API_PORT` | 8000 | Server port |

### Processing Timeouts
```python
IMAGE_PROCESSING_TIMEOUT = 30  # seconds
AUDIO_PROCESSING_TIMEOUT = 40  # seconds
TEXT_PROCESSING_TIMEOUT = 20   # seconds
MAX_FILE_SIZE_MB = 50           # megabytes
```

## 📦 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── database.py            # SQLAlchemy models and database setup
├── schemas.py             # Pydantic request/response schemas
├── gemini_service.py      # Google Gemini API integration
├── audio_processor.py     # Audio transcription and sentiment analysis
├── image_processor.py     # Image mood board analysis
├── prompts.py             # AI prompt templates
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── railway.json          # Railway deployment config
├── DEPLOYMENT.md         # Detailed deployment guide
└── uploads/              # Uploaded files storage
```

## 🔐 Security Notes

- **API Key**: Keep `GEMINI_API_KEY` secure. Use Railway secrets, not in code.
- **CORS**: Currently allows all origins (`"*"`). Configure for production.
- **Database**: SQLite is development-only. Use PostgreSQL for production.
- **File Uploads**: Limited to 50MB. Configure based on needs.

## 🧪 Testing the API

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Text-only check-in
curl -X POST http://localhost:8000/checkin \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=I'm feeling stressed about work"

# With audio and image
curl -X POST http://localhost:8000/checkin \
  -F "text=Daily check-in" \
  -F "audio_file=@/path/to/audio.m4a" \
  -F "image_file=@/path/to/mood.png"
```

### Using Swagger UI
Navigate to `http://localhost:8000/docs` and use the interactive API explorer.

## 🐛 Troubleshooting

### API Key Not Found
```
⚠️  GEMINI_API_KEY not set!
```
**Solution**: Set the environment variable before running:
```bash
export GEMINI_API_KEY=your_api_key
python main.py
```

### Health Check Fails
The `/health` endpoint requires the API to respond. Ensure:
- The application is running
- No critical errors in logs
- Network connectivity is available

### Database Locked
SQLite may have locking issues with multiple processes. For production, use PostgreSQL:
```
DATABASE_URL=postgresql://user:password@host/dbname
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Docs](https://ai.google.dev/tutorials/python_quickstart)
- [Railway Documentation](https://docs.railway.app/)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org/)

## 📝 License

This project is part of the CausalityCare initiative for mental health support.

## 👥 Support

For issues, feature requests, or questions, please open an issue in the repository or contact the development team.

---

**Last Updated**: January 2, 2025
**Version**: 2.1.0
