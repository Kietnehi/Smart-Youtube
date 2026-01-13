# Quick Start Guide

## 🚀 Setup (First Time Only)

### 1. Install Prerequisites

**Windows:**
```bash
# Install Python 3.9+ from https://www.python.org/
# Install Node.js from https://nodejs.org/
# Install ffmpeg
choco install ffmpeg
```

**macOS:**
```bash
brew install python node ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip nodejs npm ffmpeg
```

### 2. Get API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Create API key
3. Copy it (you'll need it next)

### 3. Setup Project

```bash
# Backend
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Frontend
cd ../frontend
npm install
```

## ▶️ Run Application

**Windows:**
```bash
# Double-click start.bat
# OR run in terminal:
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Manual (Two Terminals):**

Terminal 1:
```bash
cd backend
# Activate venv
python main.py
```

Terminal 2:
```bash
cd frontend
npm start
```

## 🎯 Using the App

1. Open browser: http://localhost:3000
2. Paste YouTube URL
3. Click "Analyze Video"
4. Watch transcript sync with video
5. Click "Generate AI Analysis"
6. Explore Summary, Chapters, and Notes tabs
7. Click any timestamp to jump to that moment
8. Click "Translate to Vietnamese" for translation

## 🔧 Troubleshooting

**Issue: "Module not found"**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

**Issue: "API key not found"**
```bash
cd backend
cat .env  # Verify GEMINI_API_KEY is set
```

**Issue: "ffmpeg not found"**
```bash
ffmpeg -version  # Should show version
# If not, install ffmpeg (see Setup section)
```

## 📚 More Help

See full [README.md](README.md) for detailed documentation.
