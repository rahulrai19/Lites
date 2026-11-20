import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  Maximize2, 
  RotateCcw, 
  FastForward, 
  Rewind, 
  Bot, 
  User, 
  Zap, 
  Database, 
  Sparkles, 
  Cpu
} from 'lucide-react';

interface TutorialVideoCardProps {
  title?: string;
  subtitle?: string;
  autoPlay?: boolean;
  hideFooter?: boolean;
}

interface Scenario {
  id: number;
  timeRange: [number, number];
  title: string;
  badge: string;
  badgeColor: string;
  icon: React.ElementType;
  chat: {
    user: string;
    bot: string;
    botTag: string;
  };
  engine: {
    stage: string;
    metricLabel: string;
    metricValue: string;
    latency: string;
    costSaved: string;
    details: string;
  };
}

const SCENARIOS: Scenario[] = [
  {
    id: 1,
    timeRange: [0, 7.5],
    title: '1. Exact Cache Hit (Instant $0 FAQ)',
    badge: '⚡ 100% EXACT HIT • $0 COST',
    badgeColor: '#10b981',
    icon: Zap,
    chat: {
      user: 'How do I configure my API key in Lites?',
      bot: 'Set LITES_API_KEY in your .env or pass apiKey to LitesClient.',
      botTag: 'Instant Cache Response'
    },
    engine: {
      stage: 'Exact Match Cache (Redis)',
      metricLabel: 'SHA-256 Hash',
      metricValue: '9f2b8a7c... (Match Found)',
      latency: '11.8 ms (180x speedup)',
      costSaved: '$0.015 (100% LLM bypassed)',
      details: 'Normalized prompt hash matches stored response in memory.'
    }
  },
  {
    id: 2,
    timeRange: [7.5, 15],
    title: '2. Semantic Vector Match (Zero False Positives)',
    badge: '🧠 SEMANTIC HIT • COSINE: 0.96',
    badgeColor: '#06b6d4',
    icon: Database,
    chat: {
      user: "What's the right way to setup auth token?",
      bot: 'Set LITES_API_KEY in your .env or pass apiKey to LitesClient.',
      botTag: 'Semantic Match Response'
    },
    engine: {
      stage: 'Semantic Vector Cache (Cosine θ)',
      metricLabel: 'Vector Similarity',
      metricValue: '0.96 (Threshold ≥ 0.92)',
      latency: '31.2 ms (65x speedup)',
      costSaved: '$0.022 (Zero tokens billed)',
      details: 'Rephrased question maps to identical intent in embedding space.'
    }
  },
  {
    id: 3,
    timeRange: [15, 22.5],
    title: '3. Context & Token Pruning (-51.2%)',
    badge: '📉 TOKEN PRUNED: -51.2% • SAVED $0.038',
    badgeColor: '#f59e0b',
    icon: Sparkles,
    chat: {
      user: 'Debug this code error: IndexError: list index out of range at line 42...',
      bot: 'The list is empty before indexing. Add a length check before accessing items.',
      botTag: 'Optimized LLM Execution'
    },
    engine: {
      stage: 'Sliding-Window AST Compression',
      metricLabel: 'Tokens Pruned',
      metricValue: '2,480 -> 1,210 tokens (-51.2%)',
      latency: '1,020 ms (Overhead: 0.9 ms)',
      costSaved: '$0.038 saved on prompt tokens',
      details: 'Stale conversation turns pruned while preserving system prompt & code.'
    }
  },
  {
    id: 4,
    timeRange: [22.5, 30],
    title: '4. Adaptive Model Routing (Cost Downscaling)',
    badge: '🔀 ROUTED TO FLASH • SAVED 98.5% COST',
    badgeColor: '#8b5cf6',
    icon: Cpu,
    chat: {
      user: 'Good morning! What time is it?',
      bot: 'Good morning! It is 11:00 AM UTC. How can I help you today?',
      botTag: 'Routed to Gemini Flash'
    },
    engine: {
      stage: 'Adaptive Routing Decision Engine',
      metricLabel: 'Target Dispatched',
      metricValue: 'gpt-4o -> gemini-1.5-flash',
      latency: '340 ms (sub-second return)',
      costSaved: '$0.024 saved (98.5% cheaper rate)',
      details: 'Simple query (<200 tokens) dispatched to fast model without quality loss.'
    }
  }
];

export const TutorialVideoCard: React.FC<TutorialVideoCardProps> = ({
  title = "30-Second Real-World Walkthrough: Chatbot Caching & Adaptive Routing",
  subtitle = "Watch how Lites intercepts real chatbot calls, delivers 12ms cache hits, compresses tokens, and downscales models.",
  autoPlay = false,
  hideFooter = false
}) => {
  const [isPlaying, setIsPlaying] = useState(autoPlay);
  const [currentTime, setCurrentTime] = useState(3.5); // Start midway through scenario 1 for preview
  const [speed, setSpeed] = useState<number>(1);
  const [isMuted, setIsMuted] = useState(false);
  const duration = 30; // 30-second video
  const scrubberRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (isPlaying) {
      // 100ms interval for fluid animations
      const step = 0.1 * speed;
      interval = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= duration) {
            setIsPlaying(false);
            return 0;
          }
          return Math.min(duration, +(prev + step).toFixed(2));
        });
      }, 100);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, speed, duration]);

  const togglePlay = () => setIsPlaying((prev) => !prev);

  const forward5s = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentTime((prev) => Math.min(duration, +(prev + 5).toFixed(1)));
  };

  const rewind5s = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentTime((prev) => Math.max(0, +(prev - 5).toFixed(1)));
  };

  const cycleSpeed = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSpeed((prev) => (prev === 1 ? 1.5 : prev === 1.5 ? 2 : 1));
  };

  const resetVideo = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentTime(0);
    setIsPlaying(true);
  };

  const handleScrubberClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!scrubberRef.current) return;
    const rect = scrubberRef.current.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const fraction = Math.max(0, Math.min(1, clickX / rect.width));
    setCurrentTime(+(fraction * duration).toFixed(1));
  };

  const formatTime = (secs: number) => {
    const s = Math.floor(secs);
    const ms = Math.floor((secs - s) * 10);
    const m = Math.floor(s / 60);
    const remS = s % 60;
    return `${m.toString().padStart(2, '0')}:${remS.toString().padStart(2, '0')}.${ms}`;
  };

  const currentScenario = SCENARIOS.find(
    (sc) => currentTime >= sc.timeRange[0] && currentTime < sc.timeRange[1]
  ) || SCENARIOS[SCENARIOS.length - 1];

  const progressPercent = Math.min(100, (currentTime / duration) * 100);
  const CurrentIcon = currentScenario.icon;

  // Animation phase inside the 7.5s scenario window
  const scenarioElapsed = currentTime - currentScenario.timeRange[0];
  const isTyping = scenarioElapsed < 1.2;
  const isProcessing = scenarioElapsed >= 1.2 && scenarioElapsed < 2.8;
  const isComplete = scenarioElapsed >= 2.8;

  return (
    <div className="video-glass-card">
      {/* Video Screen Area */}
      <div 
        className="video-screen video-screen-enhanced"
        onClick={togglePlay}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === ' ' || e.key === 'Enter') togglePlay(); }}
        aria-label={isPlaying ? "Pause video" : "Play video"}
      >
        <div className="video-grid-overlay" />
        <div className="video-ambient-glow" />

        {/* Floating Play/Pause Orb */}
        <div 
          className={`play-orb ${isPlaying ? 'is-playing' : ''}`}
          title={isPlaying ? "Click to Pause" : "Click to Play"}
        >
          {isPlaying ? <Pause size={30} /> : <Play size={30} style={{ marginLeft: '4px' }} />}
        </div>

        {/* Video Canvas Content Overlay */}
        <div className="video-canvas-content">
          {/* Top Bar */}
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
              {isPlaying ? `DEMO RUNNING (${speed}x)` : 'PAUSED • CLICK TO PLAY'}
            </span>

            <span className="video-badge" style={{ borderColor: currentScenario.badgeColor, color: currentScenario.badgeColor, background: 'rgba(0,0,0,0.5)' }}>
              <CurrentIcon size={13} />
              {currentScenario.badge}
            </span>
          </div>

          {/* Split-View Real-World Animation Stage */}
          <div className="video-split-container">
            {/* Left: Simulated Chatbot UI */}
            <div className="sim-chat-window">
              <div className="sim-window-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#e2e8f0' }}>
                  <Bot size={13} color="#10b981" />
                  <span>Production AI Chatbot</span>
                </div>
                <span style={{ fontSize: '0.65rem', color: isComplete ? '#10b981' : '#f59e0b', fontFamily: 'var(--font-mono)' }}>
                  {isComplete ? '● 200 OK' : isProcessing ? '● Intercepting...' : '● Receiving'}
                </span>
              </div>

              {/* Chat Message 1: User Prompt */}
              <div className="chat-bubble-user">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.15rem', color: '#94a3b8', fontSize: '0.65rem' }}>
                  <User size={10} />
                  <span>End User</span>
                </div>
                <div>{currentScenario.chat.user}</div>
              </div>

              {/* Chat Message 2: Bot Response */}
              <div className="chat-bubble-bot" style={{ opacity: isTyping ? 0.3 : 1, transition: 'opacity 0.25s ease' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.15rem', color: '#6ee7b7', fontSize: '0.65rem' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <Bot size={10} />
                    <span>Lites Proxy</span>
                  </span>
                  <span style={{ fontSize: '0.6rem', color: '#ccff00', fontFamily: 'var(--font-mono)' }}>
                    {currentScenario.chat.botTag}
                  </span>
                </div>
                <div>
                  {isTyping ? 'Streaming response from cache...' : currentScenario.chat.bot}
                </div>
              </div>
            </div>

            {/* Right: Lites Proxy Engine Telemetry */}
            <div className="sim-engine-window">
              <div className="sim-window-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#ffffff' }}>
                  <Zap size={13} color="#ef4444" />
                  <span>Lites Optimization Engine</span>
                </div>
                <span style={{ color: '#06b6d4', fontSize: '0.65rem', fontFamily: 'var(--font-mono)' }}>
                  Port :8000
                </span>
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>Strategy</span>
                <span style={{ color: '#ffffff', fontWeight: 600 }}>{currentScenario.engine.stage}</span>
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>{currentScenario.engine.metricLabel}</span>
                <span className="engine-highlight-val">{currentScenario.engine.metricValue}</span>
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>Round-trip Latency</span>
                <span style={{ color: '#06b6d4', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                  {currentScenario.engine.latency}
                </span>
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>Cost Savings</span>
                <span style={{ color: '#10b981', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                  {currentScenario.engine.costSaved}
                </span>
              </div>

              <div style={{ fontSize: '0.68rem', color: '#cbd5e1', background: 'rgba(255,255,255,0.03)', padding: '0.35rem 0.5rem', borderRadius: '4px', marginTop: 'auto', borderLeft: `2px solid ${currentScenario.badgeColor}` }}>
                {currentScenario.engine.details}
              </div>
            </div>
          </div>

          {/* Bottom Scenario Tracker Indicator */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ 
              background: 'rgba(0, 0, 0, 0.65)', 
              backdropFilter: 'blur(8px)',
              padding: '0.35rem 0.75rem', 
              borderRadius: '8px',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Active Scenario:</span>
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#ffffff' }}>
                {currentScenario.title}
              </span>
            </div>

            <div style={{ display: 'flex', gap: '0.35rem' }}>
              {SCENARIOS.map((sc) => (
                <div 
                  key={sc.id}
                  style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    background: currentScenario.id === sc.id ? sc.badgeColor : 'rgba(255,255,255,0.2)',
                    boxShadow: currentScenario.id === sc.id ? `0 0 8px ${sc.badgeColor}` : 'none',
                    transition: 'all 0.2s ease'
                  }}
                  title={sc.title}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Controls Bar */}
      <div className="video-controls-bar">
        {/* Scrubber Track with 4 Scenario Dividers */}
        <div 
          className="video-scrubber-track" 
          ref={scrubberRef}
          onClick={handleScrubberClick}
          title="Click or drag to seek across 30 seconds"
          style={{ position: 'relative' }}
        >
          {/* Milestone markers at 25%, 50%, 75% */}
          <div style={{ position: 'absolute', left: '25%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.3)', zIndex: 2 }} />
          <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.3)', zIndex: 2 }} />
          <div style={{ position: 'absolute', left: '75%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.3)', zIndex: 2 }} />

          <div 
            className="video-scrubber-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Buttons Row with Fast-Forward, Rewind, and Speed Toggle */}
        <div className="video-buttons-row">
          <div className="video-btn-group">
            {/* Play/Pause */}
            <button 
              className="video-icon-btn" 
              onClick={togglePlay}
              aria-label={isPlaying ? "Pause" : "Play"}
            >
              {isPlaying ? <Pause size={17} /> : <Play size={17} />}
            </button>

            {/* Rewind 5s */}
            <button 
              className="video-icon-btn" 
              onClick={rewind5s}
              title="Rewind 5 seconds"
              aria-label="Rewind 5s"
            >
              <Rewind size={16} />
            </button>

            {/* Fast-Forward 5s */}
            <button 
              className="video-icon-btn" 
              onClick={forward5s}
              title="Fast-forward 5 seconds"
              aria-label="Fast-forward 5s"
            >
              <FastForward size={16} />
            </button>

            {/* Speed Toggle (1x / 1.5x / 2x) */}
            <button 
              className="speed-badge"
              onClick={cycleSpeed}
              title="Toggle playback speed (1x, 1.5x, 2x)"
            >
              {speed}x
            </button>

            {/* Restart */}
            <button 
              className="video-icon-btn" 
              onClick={resetVideo}
              title="Restart 30s demo"
              aria-label="Restart video"
            >
              <RotateCcw size={15} />
            </button>

            {/* Mute */}
            <button 
              className="video-icon-btn" 
              onClick={() => setIsMuted(!isMuted)}
              aria-label={isMuted ? "Unmute" : "Mute"}
            >
              {isMuted ? <VolumeX size={17} /> : <Volume2 size={17} />}
            </button>

            {/* Time readout */}
            <span className="video-time-display">
              {formatTime(currentTime)} / 00:30.0
            </span>
          </div>

          <div className="video-btn-group">
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              30s Real Use Cases
            </span>
            <button 
              className="video-icon-btn" 
              onClick={togglePlay}
              title="Toggle Full View"
              aria-label="Expand"
            >
              <Maximize2 size={15} />
            </button>
          </div>
        </div>
      </div>

      {/* Optional Card Header / Summary Footer */}
      {!hideFooter && (title || subtitle) && (
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
