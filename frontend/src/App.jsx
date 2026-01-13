/**
 * Smart YouTube Analyzer - Main App Component
 * Orchestrates video player, transcript, and AI analysis
 */

import React, { useState } from 'react';
import axios from 'axios';
import VideoPlayer from './components/VideoPlayer.jsx';
import TranscriptPanel from './components/TranscriptPanel.jsx';
import AIPanel from './components/AIPanel.jsx';
import './App.css';

// API base URL (proxied through package.json)
const API_BASE = '/api';

function App() {
  // State management
  const [videoUrl, setVideoUrl] = useState('');
  const [videoId, setVideoId] = useState('');
  const [transcript, setTranscript] = useState([]);
  const [currentTime, setCurrentTime] = useState(0);
  const [summary, setSummary] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState('');

  // Extract video ID from YouTube URL
  const extractVideoId = (url) => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/,
      /^([a-zA-Z0-9_-]{11})$/
    ];

    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return null;
  };

  // Handle video URL submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    const extractedId = extractVideoId(videoUrl);
    if (!extractedId) {
      setError('Invalid YouTube URL or video ID');
      return;
    }

    setVideoId(extractedId);
    setTranscript([]);
    setSummary('');
    setAnalysis(null);
    setIsLoading(true);

    try {
      // Fetch transcript
      const response = await axios.post(`${API_BASE}/transcript`, {
        video_url: videoUrl
      });

      if (response.data.success) {
        setTranscript(response.data.transcript);
        console.log(`Transcript loaded: ${response.data.source}`);
      } else {
        setError(response.data.error || 'Failed to load transcript');
      }
    } catch (err) {
      console.error('Transcript fetch error:', err);
      setError('Failed to fetch transcript. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Generate AI analysis (summary + chapters + notes)
  const handleGenerateAI = async () => {
    if (transcript.length === 0) {
      setError('Transcript not available');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Parallel requests for summary and analysis
      const [summaryRes, analysisRes] = await Promise.all([
        axios.post(`${API_BASE}/summary`, { transcript }),
        axios.post(`${API_BASE}/analyze`, { transcript })
      ]);

      if (summaryRes.data.success) {
        setSummary(summaryRes.data.summary);
      }

      if (analysisRes.data.success) {
        setAnalysis({
          chapters: analysisRes.data.chapters,
          key_notes: analysisRes.data.key_notes
        });
      }

      console.log('AI analysis complete');
    } catch (err) {
      console.error('AI generation error:', err);
      setError('Failed to generate AI analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Translate transcript to selected language
  const handleTranslate = async (targetLang = 'vi') => {
    if (transcript.length === 0) return;

    setIsTranslating(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE}/translate`, {
        transcript,
        target_lang: targetLang
      });

      if (response.data.success) {
        setTranscript(response.data.translated_transcript);
        console.log(`Translation complete to ${targetLang}`);
      }
    } catch (err) {
      console.error('Translation error:', err);
      setError('Failed to translate transcript.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>🎥 Smart YouTube Analyzer</h1>
        <p className="tagline">AI-Powered Video Analysis & Note-Taking</p>
      </header>

      {/* URL Input */}
      <div className="url-section">
        <form onSubmit={handleSubmit} className="url-form">
          <input
            type="text"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            placeholder="Enter YouTube URL or Video ID"
            className="url-input"
          />
          <button type="submit" className="submit-btn" disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Analyze Video'}
          </button>
        </form>
        {error && <div className="error-message">{error}</div>}
      </div>

      {/* Main Content Grid */}
      {videoId && (
        <div className="content-grid">
          {/* Left Column: Video */}
          <div className="video-section">
            <VideoPlayer
              videoId={videoId}
              onReady={(e) => console.log('Player ready')}
              onStateChange={(e) => console.log('State changed')}
              onTimeUpdate={setCurrentTime}
            />
          </div>

          {/* Right Column: Transcript & AI */}
          <div className="sidebar">
            <TranscriptPanel
              transcript={transcript}
              currentTime={currentTime}
              onTranslate={handleTranslate}
              isTranslating={isTranslating}
            />
            
            <AIPanel
              summary={summary}
              analysis={analysis}
              onGenerate={handleGenerateAI}
              isLoading={isLoading}
            />
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="app-footer">
        <p>Powered by Google Gemini 2.0 Flash • Whisper • YouTube API</p>
      </footer>
    </div>
  );
}

export default App;
