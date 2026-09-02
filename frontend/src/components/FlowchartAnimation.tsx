import React from 'react';
import './FlowchartAnimation.css';

export function FlowchartAnimation() {
  return (
    <div className="flowchart-container">
      <svg viewBox="0 0 800 250" className="flowchart-svg">
        <defs>
          <linearGradient id="line-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="var(--accent-red)" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#ff416c" stopOpacity="0.5" />
          </linearGradient>
          
          <linearGradient id="node-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--bg-secondary)" />
            <stop offset="100%" stopColor="var(--bg-tertiary)" />
          </linearGradient>
        </defs>

        {/* Connecting Lines */}
        {/* Main Flow: Client -> Tokenizer -> Rules -> Cache -> LLM */}
        <path 
          d="M 80 125 L 180 125 L 340 125 L 500 125 L 680 125" 
          fill="none" 
          stroke="url(#line-gradient)" 
          strokeWidth="4" 
          className="flow-line" 
        />
        
        {/* Cache -> AI Engine -> LLM (Secondary Flow) */}
        <path 
          d="M 420 100 C 420 40, 420 40, 500 40 C 600 40, 600 40, 600 100" 
          fill="none" 
          stroke="url(#line-gradient)" 
          strokeWidth="2" 
          strokeDasharray="5,5"
          className="flow-line ai-line" 
        />

        {/* Animated Packets */}
        <circle cx="0" cy="0" r="4" fill="#ff4b2b" className="packet p1">
          <animateMotion dur="3s" repeatCount="indefinite" path="M 80 125 L 680 125" />
        </circle>
        
        <circle cx="0" cy="0" r="4" fill="#ff416c" className="packet p2">
          <animateMotion dur="3s" repeatCount="indefinite" path="M 420 125 C 420 40, 500 40, 680 125" begin="1.5s" />
        </circle>

        {/* --- Nodes --- */}
        
        {/* 1. Client Node */}
        <g className="node-group" transform="translate(10, 95)">
          <rect width="80" height="60" rx="10" fill="url(#node-gradient)" stroke="var(--border-color)" strokeWidth="2" />
          <text x="40" y="35" textAnchor="middle" fill="var(--text-primary)" fontSize="13" fontWeight="600">App</text>
        </g>

        {/* 2. Tokenizer Layer */}
        <g className="node-group pulse-node" transform="translate(140, 95)">
          <rect width="100" height="60" rx="12" fill="var(--bg-secondary)" stroke="var(--accent-red)" strokeWidth="2" />
          <text x="50" y="35" textAnchor="middle" fill="var(--accent-red)" fontSize="14" fontWeight="bold">Tokenizer</text>
        </g>

        {/* 3. Rule Optimizer Layer */}
        <g className="node-group pulse-node" transform="translate(280, 95)">
          <rect width="110" height="60" rx="12" fill="var(--bg-secondary)" stroke="var(--accent-red)" strokeWidth="2" />
          <text x="55" y="35" textAnchor="middle" fill="var(--accent-red)" fontSize="13" fontWeight="bold">Rule Optimizer</text>
        </g>

        {/* 4. Semantic Cache Layer */}
        <g className="node-group pulse-node" transform="translate(430, 95)">
          <rect width="110" height="60" rx="12" fill="var(--bg-secondary)" stroke="var(--accent-red)" strokeWidth="2" />
          <text x="55" y="35" textAnchor="middle" fill="var(--accent-red)" fontSize="13" fontWeight="bold">Vector Cache</text>
        </g>

        {/* 5. AI Engine (Sub-node) */}
        <g className="node-group" transform="translate(440, 20)">
          <rect width="130" height="40" rx="8" fill="var(--bg-secondary)" stroke="#ff416c" strokeWidth="1.5" strokeDasharray="4,2" />
          <text x="65" y="25" textAnchor="middle" fill="#ff416c" fontSize="13" fontWeight="500">AI Compression</text>
        </g>

        {/* 6. Target LLM Node */}
        <g className="node-group" transform="translate(640, 95)">
          <rect width="100" height="60" rx="10" fill="url(#node-gradient)" stroke="var(--border-color)" strokeWidth="2" />
          <text x="50" y="35" textAnchor="middle" fill="var(--text-primary)" fontSize="14" fontWeight="600">OpenAI</text>
        </g>
      </svg>
    </div>
  );
}
