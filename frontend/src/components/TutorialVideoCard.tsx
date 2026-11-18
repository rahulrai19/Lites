import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, Volume2, VolumeX, Maximize2, RotateCcw, Sparkles, Terminal, Cpu, Database } from 'lucide-react';

interface TutorialVideoCardProps {
  title?: string;
  subtitle?: string;
  autoPlay?: boolean;
}

const CHAPTERS = [
  {
    range: [0, 45],
    title: '1. Architecture & Proxy Setup',
    icon: Terminal,
    badge: 'Exact Cache: 12ms',
    code: `curl https://lites.sbs/v1/chat/completions \\
  -H "Authorization: Bearer $KEY" \\
  -d '{"model": "gpt-4o", "messages": [...]}'`,
    status: 'Routing through Redis Layer'
  },
  {
    range: [45, 95],
    title: '2. Semantic Caching with Redis',
    icon: Database,
    badge: 'Saved $0.042 / 850 tokens',
    code: `// Cosine similarity 0.94 > threshold (0.90)
const hit = await lites.cache.findSemanticMatch(prompt);
// Return cached embedding response`,
    status: 'Embedding Vector Match: HIT'
  },
  {
    range: [95, 140],
    title: '3. Lossless & AI Token Compression',
    icon: Sparkles,
    badge: 'Prompt Compressed: -48.2%',
    code: `prompt: "Summarize this system architecture..."
compressed_tokens: 1,420 -> 735 tokens
latency_reduced: 420ms -> 180ms`,
    status: 'AST & Whitespace Optimization Active'
  },
  {
    range: [140, 184],
    title: '4. SDK Integration: Node & Python',
    icon: Cpu,
    badge: 'Ready for Production',
    code: `import { LitesClient } from 'lites-sdk';
const client = new LitesClient({ 
  apiKey: process.env.LITES_API_KEY 
});`,
    status: 'Drop-in OpenAI Replacement'
  }
];

export const TutorialVideoCard: React.FC<TutorialVideoCardProps> = ({
  title = "Interactive Walkthrough: How Lites Accelerates LLM Calls",
  subtitle = "Learn how proxy caching, vector similarity, and lossless prompt compression slash your AI bills.",
  autoPlay = false
}) => {
  const [isPlaying, setIsPlaying] = useState(autoPlay);
  const [currentTime, setCurrentTime] = useState(14); // start partway for nice preview
  const [isMuted, setIsMuted] = useState(false);
  const duration = 184; // 3m 04s
  const scrubberRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= duration) {
            setIsPlaying(false);
            return 0;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, duration]);

  const togglePlay = () => setIsPlaying((prev) => !prev);

  const handleScrubberClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!scrubberRef.current) return;
    const rect = scrubberRef.current.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const fraction = Math.max(0, Math.min(1, clickX / rect.width));
    setCurrentTime(Math.floor(fraction * duration));
  };

  const resetVideo = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentTime(0);
    setIsPlaying(true);
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const currentChapter = CHAPTERS.find(
    (ch) => currentTime >= ch.range[0] && currentTime <= ch.range[1]
  ) || CHAPTERS[0];

  const progressPercent = Math.min(100, (currentTime / duration) * 100);

  const CurrentIcon = currentChapter.icon;

  return (
    <div className="video-glass-card">
      {/* Video Screen Area */}
      <div 
        className="video-screen"
        onClick={togglePlay}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === ' ' || e.key === 'Enter') togglePlay(); }}
        aria-label={isPlaying ? "Pause tutorial video" : "Play tutorial video"}
      >
        <div className="video-grid-overlay" />
        <div className="video-ambient-glow" />

        {/* Floating Play/Pause Orb */}
        <div 
          className={`play-orb ${isPlaying ? 'is-playing' : ''}`}
          title={isPlaying ? "Click to Pause" : "Click to Play"}
        >
          {isPlaying ? <Pause size={32} /> : <Play size={32} style={{ marginLeft: '4px' }} />}
        </div>

        {/* Video Canvas Content Overlay */}
        <div className="video-canvas-content">
          <div className="video-top-bar">
            <span className="video-badge video-badge-red">
              <span style={{ 
                width: '6px', 
                height: '6px', 
                borderRadius: '50%', 
                background: isPlaying ? '#ef4444' : '#94a3b8',
                display: 'inline-block',
                boxShadow: isPlaying ? '0 0 8px #ef4444' : 'none',
                animation: isPlaying ? 'pulse 1.5s infinite' : 'none'
              }} />
              {isPlaying ? 'STREAMING LITES DEMO' : 'PAUSED - CLICK TO PLAY'}
            </span>

            <span className="video-badge video-badge-green">
              <CurrentIcon size={14} />
              {currentChapter.badge}
            </span>
          </div>

          {/* Center visual stage */}
          <div className="video-stage-preview">
            <div className="mock-code-box">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '0.35rem', marginBottom: '0.35rem' }}>
                <span style={{ color: '#ffffff', fontWeight: 600, fontSize: '0.8rem' }}>
                  {currentChapter.title}
                </span>
                <span className="mock-line-highlight" style={{ fontSize: '0.75rem' }}>
                  {currentChapter.status}
                </span>
              </div>
              <pre style={{ margin: 0, whiteSpace: 'pre-wrap', lineHeight: 1.4 }}>
                {currentChapter.code}
              </pre>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
            <div style={{ 
              background: 'rgba(0, 0, 0, 0.55)', 
              backdropFilter: 'blur(8px)',
              padding: '0.4rem 0.8rem', 
              borderRadius: '8px',
              border: '1px solid rgba(255, 255, 255, 0.08)'
            }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Topic Chapter</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#ffffff' }}>
                {currentChapter.title}
              </div>
            </div>

            <div style={{ 
              background: 'rgba(0, 0, 0, 0.55)', 
              backdropFilter: 'blur(8px)',
              padding: '0.4rem 0.8rem', 
              borderRadius: '8px',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              fontSize: '0.8rem',
              color: '#ccff00',
              fontFamily: 'var(--font-mono)'
            }}>
              Latency: 14ms (98% faster)
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Controls Bar */}
      <div className="video-controls-bar">
        {/* Scrubber Track */}
        <div 
          className="video-scrubber-track" 
          ref={scrubberRef}
          onClick={handleScrubberClick}
          title="Click to seek"
        >
          <div 
            className="video-scrubber-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Buttons Row */}
        <div className="video-buttons-row">
          <div className="video-btn-group">
            <button 
              className="video-icon-btn" 
              onClick={togglePlay}
              aria-label={isPlaying ? "Pause" : "Play"}
            >
              {isPlaying ? <Pause size={18} /> : <Play size={18} />}
            </button>

            <button 
              className="video-icon-btn" 
              onClick={resetVideo}
              title="Restart from beginning"
              aria-label="Restart video"
            >
              <RotateCcw size={16} />
            </button>

            <button 
              className="video-icon-btn" 
              onClick={() => setIsMuted(!isMuted)}
              aria-label={isMuted ? "Unmute" : "Mute"}
            >
              {isMuted ? <VolumeX size={18} /> : <Volume2 size={18} />}
            </button>

            <span className="video-time-display">
              {formatTime(currentTime)} / {formatTime(duration)}
            </span>
          </div>

          <div className="video-btn-group">
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              1080p 60fps HD
            </span>
            <button 
              className="video-icon-btn" 
              onClick={togglePlay}
              title="Toggle Full View"
              aria-label="Expand"
            >
              <Maximize2 size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Optional Card Header / Summary Footer */}
      {(title || subtitle) && (
        <div style={{ padding: '1.25rem 1.5rem', background: 'rgba(255, 255, 255, 0.02)', borderTop: '1px solid rgba(255, 255, 255, 0.05)' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
            {title}
          </h3>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: 0, lineHeight: 1.5 }}>
            {subtitle}
          </p>
        </div>
      )}
    </div>
  );
};
