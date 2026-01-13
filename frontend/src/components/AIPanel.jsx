/**
 * AIPanel Component
 * Displays AI-generated summary, chapters, and notes with tabs
 */

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const AIPanel = ({ summary, analysis, onGenerate, isLoading }) => {
  const [activeTab, setActiveTab] = useState('summary');

  // Parse timestamp to seconds for seeking
  const parseTimestamp = (timestamp) => {
    const parts = timestamp.split(':').map(Number);
    if (parts.length === 2) {
      return parts[0] * 60 + parts[1]; // M:SS
    } else if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2]; // H:MM:SS
    }
    return 0;
  };

  // Handle chapter/note click to seek video
  const handleTimeClick = (timestamp) => {
    const seconds = parseTimestamp(timestamp);
    if (window.seekToTime) {
      window.seekToTime(seconds);
    }
  };

  return (
    <div className="ai-panel">
      <div className="ai-header">
        <h2>AI Analysis</h2>
        {!summary && !analysis && (
          <button 
            className="generate-btn"
            onClick={onGenerate}
            disabled={isLoading}
          >
            {isLoading ? '🤖 Analyzing...' : '✨ Generate AI Analysis'}
          </button>
        )}
      </div>

      {(summary || analysis) && (
        <div className="ai-tabs">
          <button
            className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveTab('summary')}
          >
            📝 Summary
          </button>
          <button
            className={`tab ${activeTab === 'chapters' ? 'active' : ''}`}
            onClick={() => setActiveTab('chapters')}
          >
            📑 Chapters
          </button>
          <button
            className={`tab ${activeTab === 'notes' ? 'active' : ''}`}
            onClick={() => setActiveTab('notes')}
          >
            💡 Key Notes
          </button>
        </div>
      )}

      <div className="ai-content">
        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>AI is analyzing the video content...</p>
          </div>
        )}

        {!isLoading && !summary && !analysis && (
          <div className="empty-state">
            <p>Click "Generate AI Analysis" to get started</p>
          </div>
        )}

        {!isLoading && activeTab === 'summary' && summary && (
          <div className="summary-content">
            <ReactMarkdown>{summary}</ReactMarkdown>
          </div>
        )}

        {!isLoading && activeTab === 'chapters' && analysis?.chapters && (
          <div className="chapters-content">
            {analysis.chapters.map((chapter, index) => (
              <div
                key={index}
                className="chapter-item"
                onClick={() => handleTimeClick(chapter.timestamp)}
              >
                <span className="chapter-time">{chapter.timestamp}</span>
                <span className="chapter-title">{chapter.title}</span>
              </div>
            ))}
          </div>
        )}

        {!isLoading && activeTab === 'notes' && analysis?.key_notes && (
          <div className="notes-content">
            {analysis.key_notes.map((note, index) => (
              <div
                key={index}
                className="note-item"
                onClick={() => handleTimeClick(note.time)}
              >
                <span className="note-time">{note.time}</span>
                <span className="note-text">{note.note}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AIPanel;
