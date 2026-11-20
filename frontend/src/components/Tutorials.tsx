import React, { useState } from 'react';
import { TutorialVideoCard } from './TutorialVideoCard';
import { 
  PlayCircle, 
  Clock, 
  CheckCircle2, 
  Terminal, 
  Copy, 
  Check,
  Zap,
  Code2,
  Sparkles,
  ShieldCheck,
  Layers
} from 'lucide-react';

interface TutorialChapter {
  id: number;
  title: string;
  description: string;
  duration: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  tags: string[];
}

interface CodeRow {
  num: number;
  isHighlighted?: boolean;
  highlightBadge?: string;
  content: React.ReactNode;
}

const CHAPTERS: TutorialChapter[] = [
  {
    id: 1,
    title: '5-Minute Setup: OpenAI Drop-in Replacement',
    description: 'Learn how to point your existing OpenAI / Anthropic client code to Lites with zero changes to prompt structures or schemas.',
    duration: '04:15',
    level: 'Beginner',
    tags: ['Proxy', 'OpenAI', 'Quickstart']
  },
  {
    id: 2,
    title: 'Semantic Caching with Redis & Vector Embeddings',
    description: 'Configure cosine similarity thresholds to answer semantically equivalent questions directly from Redis cache without upstream LLM calls.',
    duration: '06:40',
    level: 'Intermediate',
    tags: ['Redis', 'Embeddings', 'Cost Optimization']
  },
  {
    id: 3,
    title: 'Lossless & AI Context Compression',
    description: 'Compress AST, codeblocks, and repetitive system prompts by up to 48% while maintaining 100% LLM response quality.',
    duration: '08:10',
    level: 'Advanced',
    tags: ['Compression', 'Tokens', 'Context Windows']
  },
  {
    id: 4,
    title: 'Production Docker & Cloud Deployment',
    description: 'Deploy Lites on Docker, Render, or Kubernetes behind high-availability Redis instances with streaming response support.',
    duration: '05:30',
    level: 'Intermediate',
    tags: ['Docker', 'DevOps', 'Scaling']
  },
  {
    id: 5,
    title: 'Telemetry, Cost Dashboards & Realtime Metrics',
    description: 'Monitor tokens saved, hit/miss ratios, average round-trip latency, and estimated cloud dollar savings across your cluster.',
    duration: '03:50',
    level: 'Beginner',
    tags: ['Metrics', 'Telemetry', 'Analytics']
  }
];

export const Tutorials: React.FC = () => {
  const [selectedChapter, setSelectedChapter] = useState(1);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [copiedInstall, setCopiedInstall] = useState<string | null>(null);
  const [activeCodeLang, setActiveCodeLang] = useState<'node' | 'python' | 'curl'>('node');

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const copyInstallCmd = (cmd: string, lang: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedInstall(lang);
    setTimeout(() => setCopiedInstall(null), 2000);
  };

  const installCommands = {
    node: 'npm install lites-sdk',
    python: 'pip install lites-sdk',
    curl: 'curl -I https://lites.sbs/health'
  };

  const fileMeta = {
    node: { name: 'client.ts', icon: Code2, color: '#38bdf8' },
    python: { name: 'client.py', icon: Terminal, color: '#facc15' },
    curl: { name: 'request.sh', icon: Zap, color: '#4ade80' }
  };

  const codeSnippets = {
    node: `// Step 1: Install SDK
// npm install lites-sdk

import OpenAI from 'openai';

// Step 2: Initialize OpenAI client pointing to Lites Proxy
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: 'https://lites.sbs/v1' // Automatically routes through Lites caching
});

async function main() {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'What is semantic caching?' }]
  });

  console.log(response.choices[0].message.content);
}

main();`,
    python: `# Step 1: Install SDK
# pip install lites-sdk

from openai import OpenAI
import os

# Step 2: Point OpenAI client to Lites Proxy
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://lites.sbs/v1" # Automatic caching & compression
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain Lites caching in one sentence."}]
)

print(response.choices[0].message.content)`,
    curl: `# Direct cURL request through Lites Proxy
curl -X POST "https://lites.sbs/v1/chat/completions" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer $OPENAI_API_KEY" \\
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "How do I optimize LLM costs?"}
    ]
  }'`
  };

  const nodeCodeRows: CodeRow[] = [
    {
      num: 1,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}>// Step 1: Install the official SDK</span>
    },
    {
      num: 2,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}>// npm install lites-sdk</span>
    },
    {
      num: 3,
      content: <span />
    },
    {
      num: 4,
      content: (
        <span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>import </span>
          <span style={{ color: '#38bdf8' }}>OpenAI </span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>from </span>
          <span style={{ color: '#4ade80' }}>'openai'</span>;
        </span>
      )
    },
    {
      num: 5,
      content: <span />
    },
    {
      num: 6,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}>// Step 2: Initialize OpenAI client pointing to Lites Proxy</span>
    },
    {
      num: 7,
      content: (
        <span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>const </span>
          <span>openai = </span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>new </span>
          <span style={{ color: '#38bdf8' }}>OpenAI</span>({'{'}
        </span>
      )
    },
    {
      num: 8,
      content: (
        <span>
          {'  '}
          <span style={{ color: '#93c5fd' }}>apiKey</span>: process.env.
          <span style={{ color: '#e2e8f0' }}>OPENAI_API_KEY</span>,
        </span>
      )
    },
    {
      num: 9,
      isHighlighted: true,
      highlightBadge: '⚡ 1-LINE DROP-IN',
      content: (
        <span>
          {'  '}
          <span style={{ color: '#ccff00', fontWeight: 700 }}>baseURL</span>:{' '}
          <span style={{ color: '#4ade80', fontWeight: 700 }}>'https://lites.sbs/v1'</span>{' '}
          <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>// Automatically routes through Lites caching & routing</span>
        </span>
      )
    },
    {
      num: 10,
      content: <span>{'}'});</span>
    },
    {
      num: 11,
      content: <span />
    },
    {
      num: 12,
      content: (
        <span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>async function </span>
          <span style={{ color: '#60a5fa' }}>main</span>() {'{'}
        </span>
      )
    },
    {
      num: 13,
      content: (
        <span>
          {'  '}
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>const </span>
          <span>response = </span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>await </span>
          <span>openai.chat.completions.</span>
          <span style={{ color: '#60a5fa' }}>create</span>({'{'}
        </span>
      )
    },
    {
      num: 14,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>model</span>: <span style={{ color: '#4ade80' }}>'gpt-4o'</span>,
        </span>
      )
    },
    {
      num: 15,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>messages</span>: [{'{ '}
          <span style={{ color: '#93c5fd' }}>role</span>: <span style={{ color: '#4ade80' }}>'user'</span>,{' '}
          <span style={{ color: '#93c5fd' }}>content</span>: <span style={{ color: '#4ade80' }}>'What is semantic caching?'</span>
          {' }'}]
        </span>
      )
    },
    {
      num: 16,
      content: <span>{'  }'});</span>
    },
    {
      num: 17,
      content: <span />
    },
    {
      num: 18,
      content: (
        <span>
          {'  '}console.<span style={{ color: '#60a5fa' }}>log</span>(response.choices[0].message.content);
        </span>
      )
    },
    {
      num: 19,
      content: <span>{'}'}</span>
    },
    {
      num: 20,
      content: <span />
    },
    {
      num: 21,
      content: <span><span style={{ color: '#60a5fa' }}>main</span>();</span>
    }
  ];

  const pythonCodeRows: CodeRow[] = [
    {
      num: 1,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}># Step 1: Install SDK</span>
    },
    {
      num: 2,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}># pip install lites-sdk</span>
    },
    {
      num: 3,
      content: <span />
    },
    {
      num: 4,
      content: (
        <span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>from </span>
          <span>openai </span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>import </span>
          <span style={{ color: '#38bdf8' }}>OpenAI</span>
        </span>
      )
    },
    {
      num: 5,
      content: (
        <span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>import </span>
          <span>os</span>
        </span>
      )
    },
    {
      num: 6,
      content: <span />
    },
    {
      num: 7,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}># Step 2: Point standard OpenAI client to Lites Proxy</span>
    },
    {
      num: 8,
      content: (
        <span>
          <span>client = </span>
          <span style={{ color: '#38bdf8' }}>OpenAI</span>(
        </span>
      )
    },
    {
      num: 9,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>api_key</span>=os.environ.<span style={{ color: '#60a5fa' }}>get</span>(<span style={{ color: '#4ade80' }}>"OPENAI_API_KEY"</span>),
        </span>
      )
    },
    {
      num: 10,
      isHighlighted: true,
      highlightBadge: '⚡ 1-LINE DROP-IN',
      content: (
        <span>
          {'    '}
          <span style={{ color: '#ccff00', fontWeight: 700 }}>base_url</span>=<span style={{ color: '#4ade80', fontWeight: 700 }}>"https://lites.sbs/v1"</span>{' '}
          <span style={{ color: '#94a3b8', fontStyle: 'italic' }}># Automatic caching & model routing</span>
        </span>
      )
    },
    {
      num: 11,
      content: <span>)</span>
    },
    {
      num: 12,
      content: <span />
    },
    {
      num: 13,
      content: (
        <span>
          <span>response = client.chat.completions.</span>
          <span style={{ color: '#60a5fa' }}>create</span>(
        </span>
      )
    },
    {
      num: 14,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>model</span>=<span style={{ color: '#4ade80' }}>"gpt-4o"</span>,
        </span>
      )
    },
    {
      num: 15,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>messages</span>=[{'{'}
          <span style={{ color: '#4ade80' }}>"role"</span>: <span style={{ color: '#4ade80' }}>"user"</span>,{' '}
          <span style={{ color: '#4ade80' }}>"content"</span>: <span style={{ color: '#4ade80' }}>"Explain Lites caching in one sentence."</span>
          {'}'}]
        </span>
      )
    },
    {
      num: 16,
      content: <span>)</span>
    },
    {
      num: 17,
      content: <span />
    },
    {
      num: 18,
      content: (
        <span>
          <span style={{ color: '#60a5fa' }}>print</span>(response.choices[0].message.content)
        </span>
      )
    }
  ];

  const curlCodeRows: CodeRow[] = [
    {
      num: 1,
      content: <span style={{ color: '#64748b', fontStyle: 'italic' }}># Direct cURL request through Lites Gateway</span>
    },
    {
      num: 2,
      isHighlighted: true,
      highlightBadge: '⚡ PROXY ENDPOINT',
      content: (
        <span>
          <span style={{ color: '#f43f5e', fontWeight: 600 }}>curl </span>
          <span>-X POST </span>
          <span style={{ color: '#4ade80', fontWeight: 700 }}>"https://lites.sbs/v1/chat/completions"</span> \
        </span>
      )
    },
    {
      num: 3,
      content: (
        <span>
          {'  '}-H <span style={{ color: '#4ade80' }}>"Content-Type: application/json"</span> \
        </span>
      )
    },
    {
      num: 4,
      content: (
        <span>
          {'  '}-H <span style={{ color: '#4ade80' }}>"Authorization: Bearer $OPENAI_API_KEY"</span> \
        </span>
      )
    },
    {
      num: 5,
      content: (
        <span>
          {'  '}-d <span style={{ color: '#4ade80' }}>'{"{"}</span>
        </span>
      )
    },
    {
      num: 6,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>"model"</span>: <span style={{ color: '#4ade80' }}>"gpt-4o"</span>,
        </span>
      )
    },
    {
      num: 7,
      content: (
        <span>
          {'    '}
          <span style={{ color: '#93c5fd' }}>"messages"</span>: [
        </span>
      )
    },
    {
      num: 8,
      content: (
        <span>
          {'      '}{'{'}
          <span style={{ color: '#93c5fd' }}>"role"</span>: <span style={{ color: '#4ade80' }}>"user"</span>,{' '}
          <span style={{ color: '#93c5fd' }}>"content"</span>: <span style={{ color: '#4ade80' }}>"How do I optimize LLM costs?"</span>
          {'}'}
        </span>
      )
    },
    {
      num: 9,
      content: <span>{'    '}]</span>
    },
    {
      num: 10,
      content: (
        <span>
          {'  '}<span style={{ color: '#4ade80' }}>{"}'"}</span>
        </span>
      )
    }
  ];

  const currentRows = activeCodeLang === 'node' 
    ? nodeCodeRows 
    : activeCodeLang === 'python' 
    ? pythonCodeRows 
    : curlCodeRows;

  const currentMeta = fileMeta[activeCodeLang];
  const CurrentFileIcon = currentMeta.icon;

  return (
    <div className="tutorials-page">
      {/* Header */}
      <div className="tutorials-hero">
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-red)', fontWeight: 600, fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          <PlayCircle size={18} />
          Interactive Masterclass & Guides
        </div>
        <h1>Learn Lites in Minutes</h1>
        <p>
          Discover how to cut your OpenAI and Anthropic bills in half using exact hash caching, semantic Redis vector matching, and AI context compression.
        </p>
      </div>

      {/* Main Glassmorphic Video Component */}
      <TutorialVideoCard 
        title={`Video Lesson: ${CHAPTERS.find(c => c.id === selectedChapter)?.title || 'Introduction to Lites'}`}
        subtitle="Watch the simulated request lifecycle: incoming user prompt, cache validation, vector similarity check, and prompt compression."
      />

      {/* Chapters Grid */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0 }}>Course Curriculum</h2>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: '0.25rem 0 0 0' }}>
              Select a chapter to jump into its walkthrough and code example
            </p>
          </div>
          <span style={{ fontSize: '0.85rem', color: 'var(--accent-green)', fontFamily: 'var(--font-mono)' }}>
            5 Lessons • 28 Mins Total
          </span>
        </div>

        <div className="tutorials-grid">
          {CHAPTERS.map((ch) => (
            <div 
              key={ch.id}
              className={`tutorial-chapter-card ${selectedChapter === ch.id ? 'active' : ''}`}
              onClick={() => setSelectedChapter(ch.id)}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span className="chapter-number">Module {ch.id}</span>
                <span style={{ 
                  fontSize: '0.75rem', 
                  padding: '0.2rem 0.5rem', 
                  borderRadius: '4px',
                  background: ch.level === 'Beginner' ? 'rgba(34, 197, 94, 0.15)' : ch.level === 'Intermediate' ? 'rgba(234, 179, 8, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                  color: ch.level === 'Beginner' ? '#4ade80' : ch.level === 'Intermediate' ? '#facc15' : '#f87171'
                }}>
                  {ch.level}
                </span>
              </div>

              <div className="chapter-title">{ch.title}</div>
              <div className="chapter-desc">{ch.description}</div>

              <div className="chapter-meta">
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <Clock size={14} />
                  {ch.duration}
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: selectedChapter === ch.id ? 'var(--accent-red)' : 'var(--text-muted)' }}>
                  {selectedChapter === ch.id ? <CheckCircle2 size={14} /> : <PlayCircle size={14} />}
                  {selectedChapter === ch.id ? 'Selected' : 'Start Lesson'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Hands-on Interactive Code Integration Component */}
      <div className="integration-card">
        {/* Header with Title and Segmented Tabs */}
        <div className="integration-header">
          <div className="integration-title-group">
            <h3>
              <Terminal size={20} color="#ccff00" />
              Follow Along: Instant Integration Code
            </h3>
            <p>
              Replace your standard client endpoint with Lites to start saving immediately
            </p>
          </div>

          <div className="integration-tabs">
            <button 
              className={`integration-tab-btn ${activeCodeLang === 'node' ? 'active' : ''}`}
              onClick={() => setActiveCodeLang('node')}
            >
              <Code2 size={15} />
              TypeScript / Node
            </button>
            <button 
              className={`integration-tab-btn ${activeCodeLang === 'python' ? 'active' : ''}`}
              onClick={() => setActiveCodeLang('python')}
            >
              <Terminal size={15} />
              Python
            </button>
            <button 
              className={`integration-tab-btn ${activeCodeLang === 'curl' ? 'active' : ''}`}
              onClick={() => setActiveCodeLang('curl')}
            >
              <Zap size={15} />
              cURL
            </button>
          </div>
        </div>

        {/* IDE Code Window */}
        <div className="ide-code-window">
          {/* Window Header Chrome */}
          <div className="ide-window-header">
            <div className="ide-header-left">
              <div className="ide-mac-dots">
                <div className="ide-dot red" />
                <div className="ide-dot yellow" />
                <div className="ide-dot green" />
              </div>

              <div className="ide-tab-label">
                <CurrentFileIcon size={13} color={currentMeta.color} />
                <span>{currentMeta.name}</span>
              </div>

              <button 
                className="ide-install-pill"
                onClick={() => copyInstallCmd(installCommands[activeCodeLang], activeCodeLang)}
                title="Click to copy quick install command"
              >
                {copiedInstall === activeCodeLang ? <Check size={12} color="#ccff00" /> : <Terminal size={12} />}
                <span>{copiedInstall === activeCodeLang ? 'Copied to clipboard!' : installCommands[activeCodeLang]}</span>
              </button>
            </div>

            {/* Copy Snippet Button */}
            <button 
              className={`ide-copy-btn ${copiedCode === activeCodeLang ? 'copied' : ''}`}
              onClick={() => copyToClipboard(codeSnippets[activeCodeLang], activeCodeLang)}
              title="Copy entire code snippet"
            >
              {copiedCode === activeCodeLang ? <Check size={14} color="#ccff00" /> : <Copy size={14} />}
              <span>{copiedCode === activeCodeLang ? 'Copied!' : 'Copy Code'}</span>
            </button>
          </div>

          {/* Syntax-Highlighted Code Rows */}
          <div className="ide-code-content">
            {currentRows.map((row) => (
              <div 
                key={row.num} 
                className={`ide-code-row ${row.isHighlighted ? 'is-highlighted' : ''}`}
              >
                <div className="ide-line-num">{row.num}</div>
                <div className="ide-line-code">
                  <span>{row.content}</span>
                  {row.highlightBadge && (
                    <span className="line-highlight-badge">{row.highlightBadge}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Architecture Perks Grid */}
        <div className="integration-perks-grid">
          <div className="integration-perk-card">
            <div className="perk-icon-wrap" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#ef4444' }}>
              <Zap size={18} />
            </div>
            <div>
              <div className="perk-title">11.8ms Exact Cache Hit</div>
              <div className="perk-desc">Deterministic SHA-256 in-memory Redis LRU bypasses 100% upstream LLM cost.</div>
            </div>
          </div>

          <div className="integration-perk-card">
            <div className="perk-icon-wrap" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#06b6d4' }}>
              <Sparkles size={18} />
            </div>
            <div>
              <div className="perk-title">0.96 Cosine Semantic Match</div>
              <div className="perk-desc">Redis vector search matches rephrased queries with zero false positives.</div>
            </div>
          </div>

          <div className="integration-perk-card">
            <div className="perk-icon-wrap" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' }}>
              <Layers size={18} />
            </div>
            <div>
              <div className="perk-title">-51.2% Context Compression</div>
              <div className="perk-desc">Sliding-window AST pruning of multi-turn chat turns reduces billable tokens.</div>
            </div>
          </div>

          <div className="integration-perk-card">
            <div className="perk-icon-wrap" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10b981' }}>
              <ShieldCheck size={18} />
            </div>
            <div>
              <div className="perk-title">Zero Code Refactoring</div>
              <div className="perk-desc">Drop-in compatibility with official OpenAI, Anthropic, and LangChain SDKs.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

