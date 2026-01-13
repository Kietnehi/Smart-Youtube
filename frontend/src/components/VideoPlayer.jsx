/**
 * VideoPlayer Component
 * Embeds YouTube video with seek control
 */

import React, { useEffect, useRef } from 'react';
import YouTube from 'react-youtube';

const VideoPlayer = ({ videoId, onReady, onStateChange, onTimeUpdate }) => {
  const playerRef = useRef(null);
  const intervalRef = useRef(null);

  // Player options
  const opts = {
    height: '100%',
    width: '100%',
    playerVars: {
      autoplay: 0,
      modestbranding: 1,
      rel: 0,
    },
  };

  // Handle player ready
  const handleReady = (event) => {
    playerRef.current = event.target;
    
    // Start polling current time
    intervalRef.current = setInterval(() => {
      if (playerRef.current && playerRef.current.getCurrentTime) {
        const currentTime = playerRef.current.getCurrentTime();
        onTimeUpdate(currentTime);
      }
    }, 200); // Poll every 200ms for smooth sync
    
    // Expose seek method after player is ready
    window.seekToTime = (time) => {
      try {
        playerRef.current.seekTo(time, true);
      } catch (err) {
        // ignore if seek fails
      }
    };

    onReady(event);
  };

  // Cleanup interval on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      // Remove global seek helper when component unmounts
      try {
        if (window.seekToTime) delete window.seekToTime;
      } catch (e) {}
    };
  }, []);

  return (
    <div className="video-container">
      <YouTube
        videoId={videoId}
        opts={opts}
        onReady={handleReady}
        onStateChange={onStateChange}
      />
    </div>
  );
};

export default VideoPlayer;
