import React, { useState } from 'react';
import { TutorialVideoCard } from './TutorialVideoCard';
import { 
  PlayCircle, 
  Clock, 
  CheckCircle2, 
  Terminal, 
  Copy, 
  Check 
} from 'lucide-react';

interface TutorialChapter {
  id: number;
  title: string;
  description: string;
  duration: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  tags: string[];
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
  const [activeCodeLang, setActiveCodeLang] = useState<'node' | 'python' | 'curl'>('node');

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
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

      {/* Hands-on Interactive Code Snippets */}
      <div style={{ 
        background: 'var(--bg-secondary)', 
        border: '1px solid var(--border-color)', 
        borderRadius: '12px', 
        padding: '1.75rem',
        marginTop: '0.5rem'
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Terminal size={20} color="#ccff00" />
              Follow Along: Instant Integration Code
            </h3>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: '0.25rem 0 0 0' }}>
              Replace your standard client endpoint with Lites to start saving immediately
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(0,0,0,0.3)', padding: '0.25rem', borderRadius: '8px' }}>
            <button 
              className={`pill-btn ${activeCodeLang === 'node' ? 'active' : ''}`}
              style={{ padding: '0.4rem 0.85rem', fontSize: '0.85rem', background: activeCodeLang === 'node' ? 'var(--accent-red)' : 'transparent', color: '#fff' }}
              onClick={() => setActiveCodeLang('node')}
            >
              TypeScript / Node
            </button>
            <button 
              className={`pill-btn ${activeCodeLang === 'python' ? 'active' : ''}`}
              style={{ padding: '0.4rem 0.85rem', fontSize: '0.85rem', background: activeCodeLang === 'python' ? 'var(--accent-red)' : 'transparent', color: '#fff' }}
              onClick={() => setActiveCodeLang('python')}
            >
              Python
            </button>
            <button 
              className={`pill-btn ${activeCodeLang === 'curl' ? 'active' : ''}`}
              style={{ padding: '0.4rem 0.85rem', fontSize: '0.85rem', background: activeCodeLang === 'curl' ? 'var(--accent-red)' : 'transparent', color: '#fff' }}
              onClick={() => setActiveCodeLang('curl')}
            >
              cURL
            </button>
          </div>
        </div>

        <div style={{ position: 'relative' }}>
          <button 
            className="copy-btn"
            style={{ 
              position: 'absolute', 
              top: '0.75rem', 
              right: '0.75rem', 
              background: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '6px',
              padding: '0.4rem 0.75rem',
              color: '#ffffff',
              fontSize: '0.8rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              cursor: 'pointer'
            }}
            onClick={() => copyToClipboard(codeSnippets[activeCodeLang], activeCodeLang)}
          >
            {copiedCode === activeCodeLang ? <Check size={14} color="#ccff00" /> : <Copy size={14} />}
            {copiedCode === activeCodeLang ? 'Copied!' : 'Copy Code'}
          </button>

          <pre style={{ 
            background: '#070b11', 
            padding: '1.25rem', 
            borderRadius: '8px', 
            border: '1px solid rgba(255,255,255,0.06)',
            overflowX: 'auto',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.875rem',
            lineHeight: 1.5,
            color: '#e2e8f0',
            margin: 0
          }}>
            {codeSnippets[activeCodeLang]}
          </pre>
        </div>
      </div>
    </div>
  );
};
