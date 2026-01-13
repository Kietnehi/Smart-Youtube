import React, { useEffect, useRef, useState } from 'react';
import './TranscriptPanel.css'; // Import file CSS trên

const TranscriptPanel = ({ transcript, currentTime, onTranslate, isTranslating }) => {
  const containerRef = useRef(null);
  const activeRef = useRef(null);
  const [selectedLang, setSelectedLang] = useState('vi');
  const [allLanguages, setAllLanguages] = useState([
    { code: 'vi', name: 'Vietnamese' },
    { code: 'en', name: 'English' },
    { code: 'zh-cn', name: 'Chinese (Simplified)' },
    { code: 'zh-tw', name: 'Chinese (Traditional)' }
  ]);
  const [searchTerm, setSearchTerm] = useState('');
  const lastScrolledIndex = useRef(-1);

  // GIỮ NGUYÊN LOGIC CỦA BẠN
  const getActiveIndex = () => {
    return transcript.findIndex(seg => 
      currentTime >= seg.start && 
      currentTime < seg.start + seg.duration
    );
  };

  const activeIndex = getActiveIndex();

  // GIỮ NGUYÊN LOGIC SCROLL
  useEffect(() => {
    if (activeIndex !== -1 && activeIndex !== lastScrolledIndex.current && activeRef.current) {
      activeRef.current.scrollIntoView({
        behavior: 'auto',
        block: 'nearest',
        inline: 'nearest'
      });
      lastScrolledIndex.current = activeIndex;
    }
  }, [activeIndex]);

  // GIỮ NGUYÊN LOGIC CLICK SEEK
  const handleSegmentClick = (startTime) => {
    if (window.seekToTime) {
      window.seekToTime(startTime);
    }
  };

  // GIỮ NGUYÊN LOGIC FORMAT TIME
  const formatTime = (seconds) => {
    if (seconds === undefined || seconds === null || Number.isNaN(Number(seconds))) return '';
    const total = Math.floor(Number(seconds));
    const mins = Math.floor(total / 60);
    const secs = Math.floor(total % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // GIỮ NGUYÊN LOGIC FETCH LANGUAGES
  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const res = await fetch('/api/languages');
        if (!res.ok) throw new Error('Failed to fetch languages');
        const data = await res.json();
        const list = Object.entries(data.languages).map(([code, name]) => ({ code, name }));
        setAllLanguages(list);
        // Ensure selectedLang is valid after languages load
        const codes = list.map(l => l.code.toLowerCase());
        if (!codes.includes(selectedLang.toLowerCase())) {
          setSelectedLang(list[0]?.code || selectedLang);
        }
      } catch (err) {
        // keep initial defaults already in state
        console.warn('Failed to fetch languages, using defaults', err);
      }
    };
    fetchLanguages();
  }, []);

  // GIỮ NGUYÊN LOGIC FILTER
  const filteredLanguages = allLanguages.filter(l =>
    l.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    l.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // If the user types a search that yields exactly one match, auto-select it
  useEffect(() => {
    if (searchTerm.trim() === '') return;
    if (filteredLanguages.length === 1) {
      const only = filteredLanguages[0];
      if (only && only.code && only.code.toLowerCase() !== selectedLang.toLowerCase()) {
        setSelectedLang(only.code);
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm, filteredLanguages]);

  const handleSearchKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredLanguages.length > 0) {
        setSelectedLang(filteredLanguages[0].code);
      }
    }
  };

  return (
    <div className="transcript-panel">
      <div className="transcript-header">
        <h2>Transcript</h2>
        <div className="translate-controls">
          <input
            type="text"
            placeholder="Search languages (type and press Enter or select)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={handleSearchKeyDown}
            className="language-search"
            disabled={isTranslating}
          />
          <select
            className="language-select"
            value={selectedLang}
            onChange={(e) => setSelectedLang(e.target.value)}
            disabled={isTranslating}
          >
            {filteredLanguages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {`${lang.code.toUpperCase()} — ${lang.name}`}
              </option>
            ))}
          </select>
          <button
            className="translate-btn"
            onClick={() => onTranslate(selectedLang)}
            disabled={isTranslating}
          >
            {isTranslating ? '...' : 'Translate'}
          </button>
        </div>
      </div>
      
      <div className="transcript-content" ref={containerRef}>
        {transcript.length === 0 ? (
          <div className="transcript-empty">
            <p>No transcript available</p>
          </div>
        ) : (
          transcript.map((segment, index) => (
            <div
              key={index}
              ref={index === activeIndex ? activeRef : null}
              className={`transcript-segment ${index === activeIndex ? 'active' : ''}`}
              onClick={() => handleSegmentClick(segment.start)}
            >
              <span className="timestamp">{formatTime(segment.start)}</span>
              <div className="text-group">
                {/* Luôn hiển thị gốc */}
                <span className="original-text" title="Original">
                  [Original] {segment.original || segment.text}
                </span>
                {/* Luôn hiển thị bản dịch */}
                <span className="text">
                  [Translated] {segment.text}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TranscriptPanel;