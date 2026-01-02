# 🧠 CausalityCare 
https://ShrinikaTelu.github.io/causalitycare/


- **Backend**
- **Framework**: FastAPI 0.104.1 (Python async)
- **AI/ML**: Goog
1. **Enter Check-in**: Text + optional image/audio
2. **Analyze**: AI processes all inputs with Gemini 3 Pro
3. **Explore**: See causal graph, confidence scores, micro-actions
4. **Track**: Monitor patterns over timeemini 3 API (REST) - Early Access
- **Database**: SQLite + SQLAlchemy ORM
- **Server**: Uvicorn ASGIered Causal Reasoning for Wellbeing

**A multimodal AI platform that helps you understand the root causes of stress, anxiety, and burnout through structured causal reasoning—not therapy, not chatbots, just clarity.**

![Status](https://img.shields.io/badge/status-MVP-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Node.js](https://img.shields.io/badge/node.js-16+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎯 What is CausalityCare?

CausalityCare is a **structured causal reasoning engine** that analyzes your emotional state using multimodal AI (text, images, and audio) to identify root causes of stress. Unlike generic chatbots:

- **Outputs structured JSON** with causal chains (not conversational text)
- **Separates concepts**: Symptoms (feelings) vs Triggers (events) vs Environment (context)
- **Tracks uncertainty** with confidence scores (0.0 to 1.0)
- **Provides micro-actions**: Tiny, actionable steps to take today
- **Detects safety risks**: Flags self-harm intent for human follow-up
- **Stores history**: Analyze stress patterns over time

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1 (Python async)
- **AI/ML**: Google Gemini 3 Pro API (Early Access) - REST
- **Database**: SQLite + SQLAlchemy ORM
- **Server**: Uvicorn ASGI

### Frontend
- **Framework**: Angular 17 (TypeScript)
- **Visualization**: vis-network 9.1.2 (interactive graphs)
- **HTTP**: Angular HttpClient

## 🚀 Key Features

- ✅ **Multimodal Analysis**: Text + Image + Audio analyzed together
- ✅ **Causal Chains**: Visual graph showing how symptoms connect to root causes
- ✅ **Confidence Scores**: Honesty about uncertainty (0.0-1.0) on each causal link
- ✅ **Micro-Actions**: Small, low-effort steps you can take right now
- ✅ **Safety Detection**: Crisis flags for human mental health professionals
- ✅ **Pattern Analysis**: Detect recurring triggers and symptoms over time
- ✅ **Interactive Graph**: Visualize causal relationships with vis-network
- ✅ **Persistent Storage**: SQLite database tracks your wellbeing journey

## 📋 Prerequisites

- Python 3.9+
- Node.js v16+
- Gemini API Key (get from [ai.google.dev](https://ai.google.dev))

## 🔧 Installation

### Backend Setup
```bash
cd backend

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_actual_api_key_here
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./causalitycare.db
EOF

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## ▶️ Running

### Terminal 1: Backend
```bash
cd backend
python3 main.py
```

### Terminal 2: Frontend
```bash
cd frontend
npm start
```

### Open Browser
```
http://localhost:4200
```

## 📊 How It Works

1. **Enter Check-in**: Text + optional image/audio
2. **Analyze**: AI processes all inputs with Gemini 3 Pro API
3. **Explore**: See causal graph, confidence scores, micro-actions
4. **Track**: Monitor patterns over time

## 🔑 Exclusive Gemini 3 Pro API Usage (Early Access)

Why Gemini 3 Pro (Early Access)?
- ✅ **Multimodal Native**: Text + Image + Audio in one call
- ✅ **Fastest**: Sub-200ms response time
- ✅ **Cost-Effective**: Most economical per token
- ✅ **Structured Output**: JSON format enforced
- ✅ **Next-Gen**: Advanced reasoning (Gemini 3 Pro - Early Access)

## 📄 Documentation

- **README.md** (this file) - Quick start guide
- **TECHNICAL_DOCUMENTATION.md** - Complete implementation guide
- **LICENSE** - MIT License

## 🔒 Safety & Privacy

- ✅ Check-in text stored locally
- ✅ Images/audio stored locally
- ✅ API key in .env (never committed)
- ❌ No third-party data sharing
- ❌ No model training on user data

## 📞 Support

- **Issues**: GitHub Issues
- **Docs**: See TECHNICAL_DOCUMENTATION.md
- **Email**: support@causalitycare.com (coming soon)

---

**Built with ❤️ for clarity in wellbeing. Not a replacement for professional mental health care.**

**Current Status**: MVP v2.1.0 - Production Ready ✅
