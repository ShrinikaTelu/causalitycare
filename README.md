# CausalityCare

A multimodal AI-powered mental health analysis platform that leverages Google Gemini to process text, audio, and image inputs for comprehensive wellbeing check-in assessments.

## 🎯 Features

- **Multimodal Analysis**: Process text, audio (transcription + sentiment), and image (mood board analysis) in a single check-in
- **AI-Powered Insights**: Utilizes Google Gemini AI for intelligent analysis and personalized responses
- **Real-time Processing**: Async request handling with configurable timeouts for each modality
- **Database Persistence**: SQLite database for storing check-in records and analysis results
- **Health Monitoring**: Built-in health check endpoint with Docker HEALTHCHECK support
- **CORS Enabled**: Configured for frontend integration
- **Production Ready**: Deployed on Railway with automatic health checks

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **AI Engine**: Google Generative AI (Gemini)
- **Database**: SQLAlchemy + SQLite
- **File Processing**: python-multipart, aiofiles
- **Containerization**: Docker
- **Deployment**: Railway

### Frontend
- **Framework**: Angular
- **Build**: TypeScript with Angular CLI

## 📋 Prerequisites

- Python 3.9+ (Backend)
- Node.js 16+ (Frontend)
- Google Gemini API Key ([Get it here](https://ai.google.dev))
- Docker (for containerized deployment)

## 📁 Project Structure

```
causalitycare/
├── backend/                    # FastAPI backend service
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration
│   ├── database.py            # Database models
│   ├── schemas.py             # Request/response schemas
│   ├── gemini_service.py      # Gemini integration
│   ├── audio_processor.py     # Audio processing
│   ├── image_processor.py     # Image processing
│   ├── prompts.py             # AI prompt templates
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Container config
│   ├── railway.json           # Railway deployment
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── uploads/               # File storage
│
├── frontend/                   # Angular frontend
│   ├── src/                   # Source code
│   ├── package.json           # Node dependencies
│   ├── angular.json           # Angular config
│   └── tsconfig.json          # TypeScript config
│
├── README.md                   # This file
├── GEMINI_3_INTEGRATION.md     # Gemini API documentation
└── .env.example                # Example environment variables
```

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Run locally
python main.py
```

The API will start on `http://localhost:8000`
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
ng serve
```

The frontend will start on `http://localhost:4200`

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
docker build -f backend/Dockerfile -t causalitycare-backend .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e ENVIRONMENT=production \
  causalitycare-backend
```

## 🚢 Production Deployment

### Deployment on Railway

See [DEPLOYMENT.md](./backend/DEPLOYMENT.md) for detailed deployment instructions.

**Quick Summary:**
1. Connect your GitHub repository to Railway
2. Set environment variables (especially `GEMINI_API_KEY`)
3. Railway will auto-detect and deploy using the Dockerfile
4. Application will be available at your Railway project URL

## ⚙️ Configuration

### Environment Variables

```env
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=development          # or production
DEBUG=true                        # or false for production
DATABASE_URL=sqlite:///./causalitycare.db
API_HOST=0.0.0.0
API_PORT=8000
```

### Processing Timeouts
```python
IMAGE_PROCESSING_TIMEOUT = 30    # seconds
AUDIO_PROCESSING_TIMEOUT = 40    # seconds
TEXT_PROCESSING_TIMEOUT = 20     # seconds
MAX_FILE_SIZE_MB = 50             # megabytes
```

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

## 🔐 Security Notes

- **API Key**: Keep `GEMINI_API_KEY` secure. Use environment variables or secrets management.
- **CORS**: Configure for production environment.
- **Database**: SQLite is for development only. Use PostgreSQL for production.
- **File Uploads**: Limited to 50MB. Configure based on your needs.

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
Ensure:
- The application is running
- No critical errors in logs
- Network connectivity is available

### Database Locked (SQLite)
For production, use PostgreSQL:
```
DATABASE_URL=postgresql://user:password@host/dbname
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Docs](https://ai.google.dev/tutorials/python_quickstart)
- [Angular Documentation](https://angular.io/docs)
- [Railway Documentation](https://docs.railway.app/)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org/)

## 📖 Documentation

- **[Backend Deployment Guide](./backend/DEPLOYMENT.md)** - Detailed setup and deployment instructions
- **[Gemini 3 Integration](./GEMINI_3_INTEGRATION.md)** - AI model integration details

## 📝 License

This project is part of the CausalityCare initiative for mental health support.

## 👥 Support

For issues, feature requests, or questions, please open an issue in the repository or contact the development team.

---

**Last Updated**: January 4, 2026
**Version**: 2.1.0
**Status**: MVP - Feature Development
