import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  Maximize2, 
  Minimize2,
  RotateCcw, 
  FastForward, 
  Rewind, 
  Bot, 
  User, 
  Zap, 
  Database, 
  Sparkles, 
  Cpu, 
  Terminal,
  Code2
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
  pipeline: string[];
  chat: {
    user: string;
    bot: string;
    botTag: string;
  };
  engine: {
    strategy: string;
    internalHook: string;
    metricLabel: string;
    metricValue: string;
    latency: string;
    costSaved: string;
    backendLogs: string[];
  };
}

const SCENARIOS: Scenario[] = [
  {
    id: 1,
    timeRange: [0, 10.0],
    title: '1. Exact Cache Hit (Instant $0 FAQ)',
    badge: '⚡ 100% EXACT HIT • $0 COST',
    badgeColor: '#10b981',
    icon: Zap,
    pipeline: ['Client', 'Lites Normalizer', 'Redis Memory LRU', 'Cached 200 OK'],
    chat: {
      user: 'How do I configure my API key in Lites?',
      bot: 'Set LITES_API_KEY in your .env or pass apiKey to LitesClient.',
      botTag: 'Instant Cache Response'
    },
    engine: {
      strategy: 'Exact Match Cache (Redis LRU)',
      internalHook: 'app.cache.memory.ExactCache',
      metricLabel: 'SHA-256 Hash',
      metricValue: '9f2b8a7c... (Match Found)',
      latency: '11.8 ms (180x speedup)',
      costSaved: '$0.015 (100% LLM bypassed)',
      backendLogs: [
        '> [NORM] Trimmed whitespace & normalized casing',
        '> [HASH] SHA256: 9f2b8a7c4e... (Deterministic)',
        '> [REDIS] GET lites:exact:9f2b8a... -> FOUND (11.8ms)',
        '> [RESULT] $0.00 Upstream Cost • Zero LLM tokens spent'
      ]
    }
  },
  {
    id: 2,
    timeRange: [10.0, 20.0],
    title: '2. Semantic Vector Match (Zero False Positives)',
    badge: '🧠 SEMANTIC HIT • COSINE: 0.96',
    badgeColor: '#06b6d4',
    icon: Database,
    pipeline: ['Client', 'Vector Embedder', 'Cosine Search', 'Semantic 200 OK'],
    chat: {
      user: "What's the right way to setup auth token?",
      bot: 'Set LITES_API_KEY in your .env or pass apiKey to LitesClient.',
      botTag: 'Semantic Match Response'
    },
    engine: {
      strategy: 'Semantic Vector Cache (Cosine θ)',
      internalHook: 'app.cache.redis_semantic.SemanticCache',
      metricLabel: 'Vector Similarity',
      metricValue: '0.964 (Threshold ≥ 0.920)',
      latency: '31.2 ms (65x speedup)',
      costSaved: '$0.022 (Zero tokens billed)',
      backendLogs: [
        '> [EMBED] Computed 1536-dim prompt vector',
        '> [COSINE] cos(θ) = 0.964 >= 0.920 (Optimal Precision)',
        '> [INTENT] Matches "auth_configuration" (0% False Positives)',
        '> [RESULT] 31.2ms return • Avoided expensive re-generation'
      ]
    }
  },
  {
    id: 3,
    timeRange: [20.0, 30.0],
    title: '3. Context & Token Pruning (-51.2%)',
    badge: '📉 TOKEN PRUNED: -51.2% • SAVED $0.038',
    badgeColor: '#f59e0b',
    icon: Sparkles,
    pipeline: ['Client', 'AST Tokenizer', 'Sliding Window', 'Pruned Upstream'],
    chat: {
      user: 'Debug this code error: IndexError: list index out of range at line 42...',
      bot: 'The list is empty before indexing. Add a length check before accessing items.',
      botTag: 'Optimized LLM Execution'
    },
    engine: {
      strategy: 'Sliding-Window AST Compression',
      internalHook: 'app.optimizer.rules.RuleOptimizerEngine',
      metricLabel: 'Tokens Pruned',
      metricValue: '2,480 -> 1,210 tokens (-51.2%)',
      latency: '1,020 ms (Overhead: 0.9 ms)',
      costSaved: '$0.038 saved on prompt tokens',
      backendLogs: [
        '> [AST] Parsed 10 multi-turn conversation messages',
        '> [PRUNE] Sliding-window preserved latest turns + system',
        '> [CLEAN] Removed repetitive constraints & filler tokens',
        '> [SAVINGS] 2,480 -> 1,210 tokens (-51.2% billable input)'
      ]
    }
  },
  {
    id: 4,
    timeRange: [30.0, 40.0],
    title: '4. Adaptive Model Routing (Cost Downscaling)',
    badge: '🔀 ROUTED TO FLASH • SAVED 98.5% COST',
    badgeColor: '#8b5cf6',
    icon: Cpu,
    pipeline: ['Client', 'Complexity Gate', 'Adaptive Router', 'Gemini Flash'],
    chat: {
      user: 'Good morning! What time is it?',
      bot: 'Good morning! It is 11:00 AM UTC. How can I assist you today?',
      botTag: 'Routed to Gemini Flash'
    },
    engine: {
      strategy: 'Adaptive Model Routing Engine',
      internalHook: 'app.optimizer.router.AdaptiveRouter',
      metricLabel: 'Target Dispatched',
      metricValue: 'gpt-4o -> gemini-1.5-flash',
      latency: '340 ms (sub-second return)',
      costSaved: '$0.024 saved (98.5% cheaper rate)',
      backendLogs: [
        '> [ROUTER] Prompt token count: 42 tokens (< 200 threshold)',
        '> [POLICY] Context profile: CHAT (Code/Legal safety pass)',
        '> [DISPATCH] Downscaled gpt-4o ($5.00/1M) -> gemini-flash ($0.075/1M)',
        '> [DECISION] 98.5% cost reduction with 99.4% intent fidelity'
      ]
    }
  },
  {
    id: 5,
    timeRange: [40.0, 50.0],
    title: '5. Instant Project Integration (60s Setup)',
    badge: '🚀 1-LINE SETUP • WORKS WITH ANY APP',
    badgeColor: '#ec4899',
    icon: Terminal,
    pipeline: ['Your Project', 'baseURL: lites.sbs/v1', 'All 6 Pillars Active', 'Production'],
    chat: {
      user: 'import OpenAI from "openai"; // Point to Lites proxy:',
      bot: 'const client = new OpenAI({ baseURL: "https://lites.sbs/v1" });',
      botTag: 'Drop-in Compatibility'
    },
    engine: {
      strategy: 'Zero-Codebase-Refactoring Gateway',
      internalHook: 'clients.python / clients.node SDK',
      metricLabel: 'Setup Time',
      metricValue: '< 60 Seconds (1 Line Change)',
      latency: '0ms code refactoring',
      costSaved: 'Instant 77.8% Net Cost Drop',
      backendLogs: [
        '> [SDK] npm install lites-sdk | pip install lites-sdk',
        '> [GATEWAY] Point standard OpenAI client to https://lites.sbs/v1',
        '> [COMPAT] Full support for LangChain, LlamaIndex, Next.js',
        '> [AUTO] Exact Cache + Semantic Vector + Compression active!'
      ]
    }
  }
];

export const TutorialVideoCard: React.FC<TutorialVideoCardProps> = ({
  title = "Interactive Walkthrough: Production Caching & Adaptive Routing",
  subtitle = "Watch how Lites intercepts real chatbot calls, delivers 12ms cache hits, compresses tokens, downscales models, and integrates in 1 line.",
  autoPlay = false,
  hideFooter = false
}) => {
  const [isPlaying, setIsPlaying] = useState(autoPlay);
  const [hasStarted, setHasStarted] = useState(autoPlay);
  const [currentTime, setCurrentTime] = useState(0.0); // Start cleanly at 0:00
  const [speed, setSpeed] = useState<number>(1);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const duration = 50; // Ideal 50-second paced walkthrough
  
  const cardContainerRef = useRef<HTMLDivElement>(null);
  const scrubberRef = useRef<HTMLDivElement>(null);

  // Sync fullscreen state if user presses ESC or exits natively
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(Boolean(document.fullscreenElement));
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  // 100ms interval for fluid animations
  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (isPlaying) {
      const step = 0.1 * speed;
      interval = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= duration) {
            setIsPlaying(false);
            setHasStarted(false);
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
    setHasStarted(true);
    setCurrentTime((prev) => Math.min(duration, +(prev + 5).toFixed(1)));
  };

  const rewind5s = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentTime((prev) => {
      const target = Math.max(0, +(prev - 5).toFixed(1));
      if (target === 0) setHasStarted(false);
      return target;
    });
  };

  const cycleSpeed = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSpeed((prev) => (prev === 1 ? 1.5 : prev === 1.5 ? 2 : 1));
  };

  const resetVideo = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentTime(0);
    setHasStarted(false);
    setIsPlaying(false);
  };

  const jumpToScenario = (e: React.MouseEvent, startTime: number) => {
    e.stopPropagation();
    setCurrentTime(startTime);
    if (startTime > 0) {
      setHasStarted(true);
    }
  };

  const toggleFullscreen = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!cardContainerRef.current) return;
    if (!document.fullscreenElement) {
      cardContainerRef.current.requestFullscreen().catch((err) => {
        console.error('Failed to enter fullscreen:', err);
      });
    } else {
      document.exitFullscreen().catch((err) => {
        console.error('Failed to exit fullscreen:', err);
      });
    }
  };

  const handleScrubberClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!scrubberRef.current) return;
    const rect = scrubberRef.current.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const fraction = Math.max(0, Math.min(1, clickX / rect.width));
    const targetTime = +(fraction * duration).toFixed(1);
    setCurrentTime(targetTime);
    if (targetTime > 0) {
      setHasStarted(true);
    } else {
      setHasStarted(false);
    }
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

  const scenarioElapsed = currentTime - currentScenario.timeRange[0];
  const isTyping = scenarioElapsed < 2.0;
  const isProcessing = scenarioElapsed >= 2.0 && scenarioElapsed < 4.5;
  const isComplete = scenarioElapsed >= 4.5;

  return (
    <div className="video-glass-card" ref={cardContainerRef}>
      {/* Video Screen Area */}
      <div 
        className={`video-screen video-screen-enhanced ${isPlaying ? 'is-playing' : 'is-paused'}`}
        onClick={() => {
          if (!hasStarted || currentTime === 0) {
            setHasStarted(true);
            setIsPlaying(true);
          } else {
            togglePlay();
          }
        }}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { 
          if (e.key === ' ' || e.key === 'Enter') {
            if (!hasStarted || currentTime === 0) {
              setHasStarted(true);
              setIsPlaying(true);
            } else {
              togglePlay();
            }
          }
        }}
        aria-label={isPlaying ? "Pause video" : "Play video"}
      >
        <div className="video-grid-overlay" />
        <div className="video-ambient-glow" />

        {/* Central Play Orb - ONLY shown at the beginning of video at 0:00, NEVER in between or during playback */}
        {(!hasStarted || currentTime === 0) && !isPlaying && (
          <div 
            className="play-orb"
            title="Start Walkthrough"
            onClick={(e) => {
              e.stopPropagation();
              setHasStarted(true);
              setIsPlaying(true);
            }}
          >
            <Play size={32} style={{ marginLeft: '4px' }} />
          </div>
        )}

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
              {isPlaying ? `DEMO RUNNING (${speed}x)` : (!hasStarted || currentTime === 0) ? 'CLICK TO START DEMO' : 'PAUSED • CLICK TO RESUME'}
            </span>

            <span className="video-badge" style={{ borderColor: currentScenario.badgeColor, color: currentScenario.badgeColor, background: 'rgba(0,0,0,0.5)' }}>
              <CurrentIcon size={13} />
              {currentScenario.badge}
            </span>
          </div>

          {/* Split-View Real-World Animation Stage */}
          <div className="video-split-container">
            {/* Left: Simulated Chatbot UI or Project Integration */}
            <div className="sim-chat-window">
              <div className="sim-window-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#e2e8f0' }}>
                  {currentScenario.id === 5 ? <Code2 size={13} color="#ec4899" /> : <Bot size={13} color="#10b981" />}
                  <span>{currentScenario.id === 5 ? 'Project Integration Code' : 'Production AI Chatbot'}</span>
                </div>
                <span style={{ fontSize: '0.65rem', color: isComplete ? '#10b981' : '#f59e0b', fontFamily: 'var(--font-mono)' }}>
                  {currentScenario.id === 5 ? '● Production Ready' : isComplete ? '● 200 OK' : isProcessing ? '● Intercepting...' : '● Receiving'}
                </span>
              </div>

              {/* Chat Message 1: User Prompt / Code */}
              <div className="chat-bubble-user">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.15rem', color: '#94a3b8', fontSize: '0.65rem' }}>
                  {currentScenario.id === 5 ? <Terminal size={10} /> : <User size={10} />}
                  <span>{currentScenario.id === 5 ? 'Your App Code' : 'End User'}</span>
                </div>
                <div style={{ fontFamily: currentScenario.id === 5 ? 'var(--font-mono)' : 'inherit', fontSize: currentScenario.id === 5 ? '0.7rem' : '0.75rem' }}>
                  {currentScenario.chat.user}
                </div>
              </div>

              {/* Chat Message 2: Bot Response / Integration Result */}
              <div className="chat-bubble-bot" style={{ opacity: isTyping ? 0.3 : 1, transition: 'opacity 0.25s ease' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.15rem', color: '#6ee7b7', fontSize: '0.65rem' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <Bot size={10} />
                    <span>{currentScenario.id === 5 ? 'Lites Endpoint' : 'Lites Proxy'}</span>
                  </span>
                  <span style={{ fontSize: '0.6rem', color: '#ccff00', fontFamily: 'var(--font-mono)' }}>
                    {currentScenario.chat.botTag}
                  </span>
                </div>
                <div style={{ fontFamily: currentScenario.id === 5 ? 'var(--font-mono)' : 'inherit', fontSize: currentScenario.id === 5 ? '0.7rem' : '0.75rem' }}>
                  {isTyping ? 'Streaming response from cache...' : currentScenario.chat.bot}
                </div>
              </div>

              {/* Quick packages indicator for Scenario 5 */}
              {currentScenario.id === 5 && (
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto', paddingTop: '0.25rem' }}>
                  <span style={{ fontSize: '0.65rem', background: 'rgba(255,255,255,0.06)', padding: '0.2rem 0.5rem', borderRadius: '4px', color: '#38bdf8', fontFamily: 'var(--font-mono)' }}>
                    npm i lites-sdk
                  </span>
                  <span style={{ fontSize: '0.65rem', background: 'rgba(255,255,255,0.06)', padding: '0.2rem 0.5rem', borderRadius: '4px', color: '#a7f3d0', fontFamily: 'var(--font-mono)' }}>
                    pip install lites-sdk
                  </span>
                </div>
              )}
            </div>

            {/* Right: Lites Proxy Engine Telemetry & Backend Deep-Dive */}
            <div className="sim-engine-window">
              <div className="sim-window-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#ffffff' }}>
                  <Zap size={13} color="#ef4444" />
                  <span>Backend Internal Execution</span>
                </div>
                <span style={{ color: '#06b6d4', fontSize: '0.65rem', fontFamily: 'var(--font-mono)' }}>
                  {currentScenario.engine.internalHook}
                </span>
              </div>

              {/* Mini Pipeline Breadcrumb Flow */}
              <div className="pipeline-breadcrumb">
                {currentScenario.pipeline.map((step, idx) => (
                  <React.Fragment key={step}>
                    <span className={`pipeline-step ${idx === 2 ? 'active' : ''}`}>{step}</span>
                    {idx < currentScenario.pipeline.length - 1 && <span className="pipeline-arrow">➔</span>}
                  </React.Fragment>
                ))}
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>Strategy</span>
                <span style={{ color: '#ffffff', fontWeight: 600 }}>{currentScenario.engine.strategy}</span>
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>{currentScenario.engine.metricLabel}</span>
                <span className="engine-highlight-val">{currentScenario.engine.metricValue}</span>
              </div>

              <div className="engine-metric-row">
                <span style={{ color: '#94a3b8' }}>Response Latency</span>
                <span style={{ color: '#06b6d4', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                  {currentScenario.engine.latency}
                </span>
              </div>

              {/* Backend Logs Terminal Box */}
              <div style={{ 
                background: 'rgba(0, 0, 0, 0.65)', 
                padding: '0.35rem 0.5rem', 
                borderRadius: '6px', 
                border: '1px solid rgba(255, 255, 255, 0.05)',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.63rem',
                lineHeight: 1.35,
                color: '#94a3b8',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.15rem'
              }}>
                {currentScenario.engine.backendLogs.map((log, i) => (
                  <div key={i} style={{ color: i === 3 ? '#10b981' : i === 1 ? '#38bdf8' : '#cbd5e1' }}>
                    {log}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Bottom Scenario Tracker Indicator with Clickable Chapter Dots */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.25rem' }}>
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
              <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Stage:</span>
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#ffffff' }}>
                {currentScenario.title}
              </span>
            </div>

            {/* Clickable scenario chapter dots */}
            <div style={{ display: 'flex', gap: '0.45rem', alignItems: 'center' }}>
              {SCENARIOS.map((sc) => (
                <button
                  key={sc.id}
                  onClick={(e) => jumpToScenario(e, sc.timeRange[0])}
                  style={{
                    width: currentScenario.id === sc.id ? '22px' : '9px',
                    height: '9px',
                    borderRadius: '9999px',
                    background: currentScenario.id === sc.id ? sc.badgeColor : 'rgba(255,255,255,0.2)',
                    boxShadow: currentScenario.id === sc.id ? `0 0 10px ${sc.badgeColor}` : 'none',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'all 0.25s ease'
                  }}
                  title={`Jump to: ${sc.title}`}
                  aria-label={`Jump to ${sc.title}`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Controls Bar */}
      <div className="video-controls-bar">
        {/* Scrubber Track with 5 Milestone Dividers */}
        <div 
          className="video-scrubber-track" 
          ref={scrubberRef}
          onClick={handleScrubberClick}
          title="Click to seek across the 50-second timeline"
          style={{ position: 'relative' }}
        >
          {/* Milestone markers at 20%, 40%, 60%, 80% */}
          <div style={{ position: 'absolute', left: '20%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.35)', zIndex: 2 }} />
          <div style={{ position: 'absolute', left: '40%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.35)', zIndex: 2 }} />
          <div style={{ position: 'absolute', left: '60%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.35)', zIndex: 2 }} />
          <div style={{ position: 'absolute', left: '80%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.35)', zIndex: 2 }} />

          <div 
            className="video-scrubber-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Buttons Row with Real Fullscreen, Fast-Forward, Rewind, and Speed Toggle */}
        <div className="video-buttons-row">
          <div className="video-btn-group">
            {/* Play/Pause Button */}
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
              title="Restart walkthrough"
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
              {formatTime(currentTime)} / 00:50.0
            </span>
          </div>

          <div className="video-btn-group">
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              5 Real-World Scenarios
            </span>

            {/* Genuine Browser Fullscreen Toggle Button */}
            <button 
              className="video-icon-btn" 
              onClick={toggleFullscreen}
              title={isFullscreen ? "Exit Fullscreen" : "Enter Fullscreen"}
              aria-label={isFullscreen ? "Exit Fullscreen" : "Enter Fullscreen"}
            >
              {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
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
