import './DetailedFlowchart.css';

export function DetailedFlowchart() {
  return (
    <div className="detailed-flowchart-container">
      <div className="flowchart-header">
        <h3>How <span style={{color: 'var(--accent-red)'}}>Lites</span> Works</h3>
        <p>Lites optimizes every request intelligently to save tokens, reduce cost, and improve latency.</p>
        <div className="legend">
          <div className="legend-item"><span className="dot dot-green"></span> Hit / Success</div>
          <div className="legend-item"><span className="dot dot-yellow"></span> Processing</div>
          <div className="legend-item"><span className="dot dot-red"></span> Miss / Action</div>
          <div className="legend-item"><span className="dot dot-gray"></span> Skipped</div>
        </div>
      </div>

      <div className="svg-wrapper">
        <svg viewBox="0 0 800 1200" className="flowchart-svg-main" preserveAspectRatio="xMidYMin meet">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
            </marker>
            <marker id="arrowhead-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#1eb854" />
            </marker>
            <marker id="arrowhead-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#ff416c" />
            </marker>
            <marker id="arrowhead-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#7b61ff" />
            </marker>
          </defs>

          {/* Connectors (Main Vertical) */}
          <line x1="400" y1="80" x2="400" y2="130" stroke="#666" strokeWidth="2" markerEnd="url(#arrowhead)" />
          <line x1="400" y1="230" x2="400" y2="280" stroke="#ff416c" strokeWidth="2" markerEnd="url(#arrowhead-red)" />
          <line x1="400" y1="380" x2="400" y2="430" stroke="#ff416c" strokeWidth="2" markerEnd="url(#arrowhead-red)" />
          <line x1="400" y1="490" x2="400" y2="540" stroke="#666" strokeWidth="2" markerEnd="url(#arrowhead)" />
          <line x1="400" y1="600" x2="400" y2="650" stroke="#666" strokeWidth="2" markerEnd="url(#arrowhead)" />
          
          <path id="path-router-gpt4" d="M 400 750 L 400 780 L 300 780 L 300 810" fill="none" stroke="#7b61ff" strokeWidth="2" markerEnd="url(#arrowhead-purple)" />
          <path id="path-router-gpt3" d="M 400 750 L 400 780 L 500 780 L 500 810" fill="none" stroke="#7b61ff" strokeWidth="2" markerEnd="url(#arrowhead-purple)" />
          
          <path d="M 300 890 L 300 920 L 400 920 L 400 950" fill="none" stroke="#666" strokeWidth="2" markerEnd="url(#arrowhead)" />
          <path d="M 500 890 L 500 920 L 400 920" fill="none" stroke="#666" strokeWidth="2" />
          
          <line x1="400" y1="1010" x2="400" y2="1060" stroke="#666" strokeWidth="2" markerEnd="url(#arrowhead)" />

          {/* Connectors (Returns - Hit) */}
          <path id="path-exact-return" d="M 300 180 L 250 180 L 250 210" fill="none" stroke="#1eb854" strokeWidth="2" markerEnd="url(#arrowhead-green)" />
          <path id="path-vector-return" d="M 300 330 L 250 330 L 250 360" fill="none" stroke="#1eb854" strokeWidth="2" markerEnd="url(#arrowhead-green)" />

          {/* Connectors (Dashed info lines) */}
          <line x1="500" y1="180" x2="550" y2="180" stroke="#666" strokeWidth="1" strokeDasharray="4" />
          <line x1="500" y1="330" x2="550" y2="330" stroke="#666" strokeWidth="1" strokeDasharray="4" />
          <line x1="480" y1="460" x2="550" y2="460" stroke="#666" strokeWidth="1" strokeDasharray="4" />
          <line x1="480" y1="570" x2="550" y2="570" stroke="#666" strokeWidth="1" strokeDasharray="4" />
          <line x1="500" y1="700" x2="550" y2="700" stroke="#666" strokeWidth="1" strokeDasharray="4" />
          <line x1="480" y1="980" x2="550" y2="980" stroke="#666" strokeWidth="1" strokeDasharray="4" />
          <line x1="480" y1="1090" x2="550" y2="1090" stroke="#666" strokeWidth="1" strokeDasharray="4" />

          {/* Animated Flow Packets */}
          <circle cx="0" cy="0" r="4" fill="#ff416c" className="flow-packet">
            <animateMotion dur="4s" repeatCount="indefinite" path="M 400 80 L 400 130 L 400 230 L 400 280 L 400 380 L 400 430 L 400 490 L 400 540 L 400 600 L 400 650" />
          </circle>
          
          <circle cx="0" cy="0" r="4" fill="#7b61ff" className="flow-packet">
            <animateMotion dur="2s" repeatCount="indefinite" path="M 400 750 L 400 780 L 300 780 L 300 810" />
          </circle>
          
          <circle cx="0" cy="0" r="4" fill="#1eb854" className="flow-packet">
            <animateMotion dur="1.5s" repeatCount="indefinite" path="M 300 180 L 250 180 L 250 210" />
          </circle>

          {/* --- Main Nodes --- */}
          
          {/* App Request */}
          <rect x="320" y="20" width="160" height="60" rx="8" fill="#161b22" stroke="#ff416c" strokeWidth="2" />
          <text x="400" y="45" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">App Request</text>
          <text x="400" y="65" textAnchor="middle" fill="#8b949e" fontSize="12">Incoming Request</text>

          {/* Exact Cache (Diamond) */}
          <g className="flow-node hoverable">
            <polygon points="400,130 500,180 400,230 300,180" fill="#161b22" stroke="#1eb854" strokeWidth="2" />
            <text x="400" y="175" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">Exact Cache</text>
            <text x="400" y="195" textAnchor="middle" fill="#8b949e" fontSize="12">Check exact match</text>
          </g>

          {/* Vector Cache (Diamond) */}
          <g className="flow-node hoverable">
            <polygon points="400,280 500,330 400,380 300,330" fill="#161b22" stroke="#1eb854" strokeWidth="2" />
            <text x="400" y="325" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">Vector Cache</text>
            <text x="400" y="345" textAnchor="middle" fill="#8b949e" fontSize="12">Semantic similarity</text>
          </g>

          {/* Rule Optimizer */}
          <g className="flow-node hoverable">
            <rect x="320" y="430" width="160" height="60" rx="8" fill="#161b22" stroke="#ff416c" strokeWidth="2" />
            <text x="400" y="455" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">Rule Optimizer</text>
            <text x="400" y="475" textAnchor="middle" fill="#8b949e" fontSize="12">Strip whitespace</text>
          </g>

          {/* AI Compression */}
          <g className="flow-node hoverable">
            <rect x="320" y="540" width="160" height="60" rx="8" fill="#161b22" stroke="#ff416c" strokeWidth="2" />
            <text x="400" y="565" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">AI Compression</text>
            <text x="400" y="585" textAnchor="middle" fill="#8b949e" fontSize="12">LLMLingua</text>
          </g>

          {/* Adaptive Router (Diamond) */}
          <g className="flow-node hoverable">
            <polygon points="400,650 500,700 400,750 300,700" fill="#161b22" stroke="#7b61ff" strokeWidth="2" />
            <text x="400" y="695" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">Adaptive Router</text>
            <text x="400" y="715" textAnchor="middle" fill="#8b949e" fontSize="12">Select best model</text>
          </g>

          {/* GPT-4 */}
          <g className="flow-node hoverable">
            <rect x="220" y="810" width="160" height="80" rx="8" fill="#161b22" stroke="#7b61ff" strokeWidth="2" />
            <text x="300" y="845" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">GPT-4</text>
            <text x="300" y="865" textAnchor="middle" fill="#8b949e" fontSize="12">Complex tasks</text>
          </g>

          {/* GPT-3.5 */}
          <g className="flow-node hoverable">
            <rect x="420" y="810" width="160" height="80" rx="8" fill="#161b22" stroke="#7b61ff" strokeWidth="2" />
            <text x="500" y="845" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">GPT-3.5</text>
            <text x="500" y="865" textAnchor="middle" fill="#8b949e" fontSize="12">Simple tasks</text>
          </g>

          {/* LLM Response */}
          <g className="flow-node hoverable">
            <rect x="320" y="950" width="160" height="60" rx="8" fill="#161b22" stroke="#3b82f6" strokeWidth="2" />
            <text x="400" y="975" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">LLM Response</text>
            <text x="400" y="995" textAnchor="middle" fill="#8b949e" fontSize="12">From selected model</text>
          </g>

          {/* Metrics */}
          <g className="flow-node hoverable">
            <rect x="320" y="1060" width="160" height="60" rx="8" fill="#161b22" stroke="#1eb854" strokeWidth="2" />
            <text x="400" y="1085" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="bold">Metrics Tracker</text>
            <text x="400" y="1105" textAnchor="middle" fill="#8b949e" fontSize="12">Cost & latency</text>
          </g>

          {/* --- Return Nodes --- */}
          <rect x="170" y="210" width="160" height="60" rx="8" fill="#161b22" stroke="#4b5563" strokeWidth="1" />
          <circle cx="190" cy="240" r="10" fill="none" stroke="#1eb854" strokeWidth="2" />
          <path d="M 186 240 L 189 244 L 195 236" fill="none" stroke="#1eb854" strokeWidth="2" />
          <text x="210" y="235" fill="#fff" fontSize="13" fontWeight="bold">Return Cached</text>
          <text x="210" y="255" fill="#8b949e" fontSize="11">Instant response</text>

          <rect x="170" y="360" width="160" height="60" rx="8" fill="#161b22" stroke="#4b5563" strokeWidth="1" />
          <circle cx="190" cy="390" r="10" fill="none" stroke="#1eb854" strokeWidth="2" />
          <path d="M 186 390 L 189 394 L 195 386" fill="none" stroke="#1eb854" strokeWidth="2" />
          <text x="210" y="385" fill="#fff" fontSize="13" fontWeight="bold">Return Cached</text>
          <text x="210" y="405" fill="#8b949e" fontSize="11">Semantic match</text>

          {/* --- Info Panels --- */}
          <g transform="translate(550, 140)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">Exact Cache Stats</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Lookup: 1.24ms</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Hit Rate: 68.4%</text>
          </g>
          
          <g transform="translate(550, 290)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">Vector Cache Stats</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Threshold: 0.85</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Hit Rate: 21.7%</text>
          </g>

          <g transform="translate(550, 420)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">Optimizer Stats</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Saved: 349 (18.9%)</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Latency: 0.1ms</text>
          </g>

          <g transform="translate(550, 530)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">AI Compression</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Model: gpt-4o-mini</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Saved: 612 tokens</text>
          </g>

          <g transform="translate(550, 660)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">Router Stats</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Complexity: High</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Est Cost: $0.021</text>
          </g>

          <g transform="translate(550, 940)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">LLM Response</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Output: 702 tokens</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Time: 2.83s</text>
          </g>

          <g transform="translate(550, 1050)">
            <rect width="180" height="80" rx="6" fill="#161b22" stroke="#30363d" strokeWidth="1" />
            <text x="15" y="25" fill="#fff" fontSize="13" fontWeight="bold">Metrics</text>
            <text x="15" y="45" fill="#8b949e" fontSize="11">• Saved: 961 (24.1%)</text>
            <text x="15" y="65" fill="#8b949e" fontSize="11">• Est Saved: $0.018</text>
          </g>
          
        </svg>
      </div>
    </div>
  );
}
