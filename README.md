# 🎥 Smart YouTube Analyzer

> AI-Powered YouTube Video Analysis & Note-Taking with Real-Time Transcript Synchronization

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Node.js-16+-339933?style=for-the-badge&logo=node.js&logoColor=white" />
  <img src="https://img.shields.io/badge/npm-8+-CB3837?style=for-the-badge&logo=npm&logoColor=white" />
  <img src="https://img.shields.io/badge/Gemini-2.0%20Flash-8A2BE2?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-Whisper-000000?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Machine%20Learning-FF8C00?style=for-the-badge" />
  <img src="https://img.shields.io/badge/NLP-Natural%20Language%20Processing-FFD700?style=for-the-badge" />
  <img src="https://img.shields.io/badge/YouTube-Transcript-FF0000?style=for-the-badge&logo=youtube&logoColor=white" />
  <img src="https://img.shields.io/badge/ffmpeg-Audio%20Processing-1DB954?style=for-the-badge&logo=ffmpeg&logoColor=white" />
  <img src="https://img.shields.io/badge/yt--dlp-Downloader-808080?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Open%20Source-❤️-FF4500?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PRs-Welcome-32CD32?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Contributions-Welcome-1E90FF?style=for-the-badge" />
</p>


## 🌟 Features

- **🎬 YouTube Video Embedding**: Seamless video playback with full controls
- **📝 Smart Transcription**: 
  - Primary: Official YouTube transcript API
  - Fallback: Local Whisper transcription with audio download
- **🔄 Real-Time Sync**: Transcript highlighting synchronized with video playback (200ms polling)
 - **🔄 Real-Time Sync**: Transcript highlighting synchronized with video playback (200ms polling) — the transcript always shows which timeline/segment is currently playing so you can follow along in real time.
- **🌐 Translation**: One-click translation to Vietnamese (expandable to other languages)
- **🤖 AI Intelligence** (Powered by Google Gemini 2.0 Flash):
  - **Summary**: Concise video content summary
  - **Smart Chapters**: Auto-generated timeline with topic segmentation
  - **Key Notes**: Timestamped important insights and takeaways
- **🎯 Click-to-Seek**: Click any transcript line or timestamp to jump to that moment
 - **🎯 Click-to-Seek**: Click any transcript line or timestamp to jump to that moment in the video — the player will seek to the selected timeline so you can instantly replay that segment.
- **📱 Responsive Design**: Clean, modern UI with split-screen layout

## 🖼️ UI Preview
Below are screenshots showing key UI panels and AI outputs produced by the app. Each image is centered and includes a concise title and a short professional description explaining what the view demonstrates.

---

### AI Summary
<p align="center">
  <img src="images/AIsummary.png" alt="AI Summary" style="max-width:900px; width:100%; height:auto;" />
</p>
<p align="center"><strong>AI Summary</strong></p>
<p align="center">A concise, human-readable summary produced by the AI panel. The summary highlights the main ideas, concise bullet-style takeaways, and the key argument of the video so you can grasp the content at a glance.</p>

---

### AI Chapters
<p align="center">
  <img src="images/AIchapters.png" alt="AI Chapters" style="max-width:900px; width:100%; height:auto;" />
</p>
<p align="center"><strong>AI Chapters</strong></p>
<p align="center">Automatically generated chapter markers with timestamps and descriptive titles. Use these chapters to quickly jump between major sections of the video and understand the high-level structure.</p>

---

### AI Key Notes
<p align="center">
  <img src="images/AIKeynotes.png" alt="AI Keynotes" style="max-width:900px; width:100%; height:auto;" />
</p>
<p align="center"><strong>AI Key Notes</strong></p>
<p align="center">Context-aware, timestamped highlights and important takeaways extracted from the transcript. Ideal for quick review, sharing, or converting into study notes.</p>

---

### Main Interface
<p align="center">
  <img src="images/giaodienhethong.png" alt="Main Interface" style="max-width:900px; width:100%; height:auto;" />
</p>
<p align="center"><strong>Main Interface</strong></p>
<p align="center">The primary application layout showing the embedded YouTube player, synchronized transcript (with active timeline highlighting), and the AI Analysis panel (Summary, Chapters, Key Notes).</p>

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)

## 🏗 Architecture

```
User → React Frontend → FastAPI Backend → [YouTube API | Whisper] → Gemini AI → UI
```

**Data Flow:**
1. User inputs YouTube URL
2. Backend extracts transcript (YouTube API or Whisper fallback)
3. Frontend displays video + synchronized transcript
4. User triggers AI analysis
5. Gemini processes transcript → generates summary/chapters/notes
6. Results displayed in organized tabs

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed flow diagrams.

## 📦 Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher
- **ffmpeg**: Required for audio processing (Whisper fallback)

### Getting ffmpeg

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### API Keys

#### Google Gemini API Key (Required)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "**Get API Key**" or "**Create API Key**"
3. Choose an existing project or create a new one
4. Copy the generated API key
5. Store it securely (you'll add it to `.env` later)

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Sufficient for personal use

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Smart_Youtube.git
cd Smart_Youtube
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: Installing Whisper may take 5-10 minutes as it downloads model weights.

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

## ⚙️ Configuration

### Backend Configuration

1. **Create `.env` file** in the `backend/` directory:

```bash
cd backend
cp .env.example .env
```

2. **Edit `.env`** with your configuration:

```env
# REQUIRED: Your Google Gemini API Key
GEMINI_API_KEY=your_actual_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Origins (add your frontend URL)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Whisper Model Size (tiny, base, small, medium, large)
# Recommendation: "base" for balance of speed and accuracy
WHISPER_MODEL=base

# Temp Directory for Audio Files
TEMP_DIR=./temp_audio
```

**Whisper Model Sizes:**
| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny | 39 MB | Very Fast | Lower | Quick testing |
| base | 74 MB | Fast | Good | **Recommended** |
| small | 244 MB | Medium | Better | Higher accuracy |
| medium | 769 MB | Slow | High | Professional use |
| large | 1550 MB | Very Slow | Highest | Maximum accuracy |

### Frontend Configuration

The frontend automatically proxies API requests to `http://localhost:8000` via the `proxy` setting in `package.json`. No additional configuration needed for local development.

For production, update the API base URL in `frontend/src/App.js`:

```javascript
const API_BASE = 'https://your-api-domain.com/api';
```

## 🏃 Running the Application

### Development Mode

#### Terminal 1: Start Backend

```bash
cd backend

# Activate virtual environment (if not already active)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run FastAPI server
python main.py
```

Backend will start at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs** (Swagger UI)

#### Terminal 2: Start Frontend

```bash
cd frontend

# Start React development server
npm start
```

Frontend will open automatically at: **http://localhost:3000**

### Quick Start Script (Optional)

Create a `start.sh` (macOS/Linux) or `start.bat` (Windows) in the project root:

**start.sh**:
```bash
#!/bin/bash
cd backend && source venv/bin/activate && python main.py &
cd frontend && npm start
```

**start.bat**:
```batch
@echo off
start cmd /k "cd backend && venv\Scripts\activate && python main.py"
start cmd /k "cd frontend && npm start"
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. Get Transcript
```http
POST /api/transcript
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "transcript": [
    {
      "text": "We're no strangers to love",
      "start": 0.5,
      "duration": 2.3
    }
  ],
  "source": "youtube_api",
  "success": true
}
```

#### 2. Generate Summary
```http
POST /api/summary
Content-Type: application/json

{
  "transcript": [...]
}
```

**Response:**
```json
{
  "summary": "This video discusses...",
  "success": true
}
```

#### 3. Generate Analysis
```http
POST /api/analyze
Content-Type: application/json

{
  "transcript": [...]
}
```

**Response:**
```json
{
  "chapters": [
    {"timestamp": "0:00", "title": "Introduction"},
    {"timestamp": "2:30", "title": "Main Topic"}
  ],
  "key_notes": [
    {"time": "0:15", "note": "Important point here"}
  ],
  "success": true
}
```

#### 4. Translate Transcript
```http
POST /api/translate
Content-Type: application/json

{
  "transcript": [...],
  "target_lang": "vi"
}
```

**Response:**
```json
{
  "translated_transcript": [
    {
      "text": "Chúng tôi không xa lạ với tình yêu",
      "start": 0.5,
      "duration": 2.3,
      "original": "We're no strangers to love"
    }
  ],
  "success": true
}
```

## 🔧 Technical Details

### Backend Stack

- **FastAPI**: Modern async Python web framework
- **youtube-transcript-api**: Official transcript extraction
- **yt-dlp**: YouTube audio downloader (fallback)
- **OpenAI Whisper**: Local speech-to-text transcription
- **google-genai**: New Google Gemini SDK (`from google import genai`)
- **googletrans**: Translation service

### Frontend Stack

- **React 18**: Component-based UI
- **Axios**: HTTP client for API calls
- **react-youtube**: YouTube player integration
- **react-markdown**: Markdown rendering for summaries

### Synchronization Logic

The frontend uses a **200ms polling interval** to check the video's current time:

```javascript
setInterval(() => {
  const currentTime = player.getCurrentTime();
  const activeSegment = transcript.find(seg => 
    currentTime >= seg.start && 
    currentTime < seg.start + seg.duration
  );
  highlightTranscript(activeSegment);
}, 200);
```

**Why 200ms?**
- Fast enough for smooth user experience
- Low enough CPU usage
- Balances accuracy vs performance

### Gemini Integration

**Model Used**: `gemini-2.0-flash-exp` (or `gemini-1.5-flash`)

**Why Flash Models?**
- **Speed**: 2-3 second response time
- **Cost**: Free tier friendly
- **Capacity**: 1M token context window
- **Quality**: Excellent for summarization tasks

**Code Example**:
```python
from google import genai

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=prompt
)
summary = response.text
```

### Whisper Fallback Strategy

**Trigger Conditions:**
- Official transcript disabled by creator
- Video lacks captions
- Regional restrictions

**Process:**
1. Download audio with `yt-dlp` (MP3, 192kbps)
2. Transcribe with Whisper (`base` model)
3. Format timestamps to match YouTube API output
4. Clean up temporary files

**Performance:**
- 10-minute video: ~30-60 seconds transcription time
- Memory: ~2GB RAM (base model)
- GPU acceleration supported (CUDA)

## 🐛 Troubleshooting

### Common Issues

#### 1. "GEMINI_API_KEY not found"
**Solution**: Ensure `.env` file exists in `backend/` with your API key:
```bash
cd backend
cat .env  # Should show GEMINI_API_KEY=your_key
```

#### 2. "ffmpeg not found"
**Solution**: Install ffmpeg and add to PATH:
```bash
ffmpeg -version  # Verify installation
```

#### 3. "Failed to fetch transcript"
**Possible Causes:**
- Video has disabled captions
- Age-restricted content
- Regional restrictions

**Solution**: The system will automatically try Whisper fallback. Check backend logs:
```bash
# In backend terminal
INFO: Using Whisper fallback for video: abc123
```

#### 4. "Module not found: react-youtube"
**Solution**: Reinstall frontend dependencies:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 5. CORS Errors
**Solution**: Verify backend `.env` includes your frontend URL:
```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### 6. Slow Whisper Transcription
**Solutions:**
- Use smaller model: `WHISPER_MODEL=tiny`
- Enable GPU acceleration (NVIDIA GPUs):
  ```bash
  pip install openai-whisper[cuda]
  ```

### Debug Mode

Enable verbose logging in backend:

**backend/main.py**:
```python
logging.basicConfig(level=logging.DEBUG)
```

Check backend logs at: `http://localhost:8000` (terminal output)

## 📈 Performance Tips

1. **First Run**: Whisper downloads models (~74MB for base), causing initial delay
2. **Caching**: Whisper models are cached after first use
3. **GPU Acceleration**: Install CUDA-enabled Whisper for 5x faster transcription
4. **Chunking**: For videos >30 minutes, consider chunking transcript for Gemini
5. **Rate Limits**: Free tier has limits; implement request queuing for production

## 🔐 Security Best Practices

- **Never commit `.env` files** to version control
- Use environment variables in production
- Implement rate limiting on API endpoints
- Validate YouTube URLs before processing
- Sanitize user inputs
- Use HTTPS in production

## 🚢 Deployment

### Backend (Example: Railway)

1. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Add environment variables in Railway dashboard
3. Ensure ffmpeg is available in container

### Frontend (Example: Vercel)

1. Build command: `npm run build`
2. Output directory: `build`
3. Update API base URL to production backend

## 🔮 Future Enhancements

- [ ] Multi-language support (Spanish, French, etc.)
- [ ] PDF/Markdown export of notes
- [ ] User accounts and save history
- [ ] Playlist batch processing
- [ ] Advanced AI features (Q&A, quiz generation)
- [ ] Video clip extraction by chapter
- [ ] Collaborative note-taking
- [ ] Browser extension for one-click analysis

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Submit a pull request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Smart_Youtube/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Smart_Youtube/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- **Google Gemini**: AI-powered analysis
- **OpenAI Whisper**: Speech transcription
- **YouTube**: Video platform
- **FastAPI Community**: Backend framework
- **React Community**: Frontend framework

---

**Built with ❤️ by [Your Name]**

*Powered by Google Gemini 2.0 Flash • OpenAI Whisper • YouTube API*

---


## 🎬 Smart-Youtube

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=120&section=header"/>

<p align="center">
  <a href="https://github.com/Kietnehi">
    <img src="https://github.com/Kietnehi.png" width="140" height="140" style="border-radius: 50%; border: 4px solid #A371F7;" alt="Avatar Truong Phu Kiet"/>
  </a>
</p>

<h3>🚀 Smart-Youtube</h3>

<a href="https://github.com/Kietnehi/Smart-Youtube">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=FF0000&background=00000000&center=true&vCenter=true&width=520&lines=AI-powered+YouTube+Assistant;Smart+Search+%26+Summarization;Transcript+Analysis+%26+Chatbot;Built+with+FastAPI+%26+LLMs" alt="Typing SVG" />
</a>

<br/><br/>

<p align="center">
  <img src="https://img.shields.io/badge/AI-YouTube%20Intelligence-FF0000?style=flat-square&logo=youtube&logoColor=white"/>
  <img src="https://img.shields.io/badge/Use--Case-Study%20%7C%20Research-6A5ACD?style=flat-square&logo=openai&logoColor=white"/>
</p>

<h3>🛠 Tech Stack</h3>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,docker,react,nodejs,mongodb,pytorch,git&theme=light" alt="Tech Stack"/>
  </a>
</p>

<br/>

<h3>🌟 Smart YouTube </h3>
<p align="center">
  <a href="https://github.com/Kietnehi/Smart-Youtube">
    <img src="https://img.shields.io/github/stars/Kietnehi/Smart-Youtube?style=for-the-badge&color=yellow" alt="Stars"/>
    <img src="https://img.shields.io/github/forks/Kietnehi/Smart-Youtube?style=for-the-badge&color=orange" alt="Forks"/>
    <img src="https://img.shields.io/github/issues/Kietnehi/Smart-Youtube?style=for-the-badge&color=red" alt="Issues"/>
  </a>
</p>

<p align="center">
  <img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark" alt="Daily Quote"/>
</p>

<p align="center">
  <i>⭐ Star the repo if Smart-Youtube helps you understand videos faster & smarter!</i>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=80&section=footer"/>

</div>
