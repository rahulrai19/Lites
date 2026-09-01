import { useState } from 'react';

interface DocsProps {
  activeSection: string;
}

export function Documentation({ activeSection }: DocsProps) {
  const [activeTab, setActiveTab] = useState<'rules' | 'ai' | 'cache'>('rules');

  if (activeSection === 'Rule Optimization' || activeSection === 'AI Compression' || activeSection === 'Semantic Caching') {
    return (
      <div>
        <h2 className="section-header">Core Concepts</h2>
        <div className="prose">
          <p>Lites uses a multi-layered pipeline to compress your prompts and cache the results. Select a tab below to see how each layer works:</p>
          
          <div className="tabs-container">
            <div className="tabs-header">
              <button 
                className={`tab-btn ${activeTab === 'rules' ? 'active' : ''}`}
                onClick={() => setActiveTab('rules')}
              >
                Rule Optimization
              </button>
              <button 
                className={`tab-btn ${activeTab === 'ai' ? 'active' : ''}`}
                onClick={() => setActiveTab('ai')}
              >
                AI Compression
              </button>
              <button 
                className={`tab-btn ${activeTab === 'cache' ? 'active' : ''}`}
                onClick={() => setActiveTab('cache')}
              >
                Semantic Caching
              </button>
            </div>
            <div className="tab-content">
              {activeTab === 'rules' && (
                <div>
                  <h3 style={{ marginTop: 0 }}>Deterministic Rule Compression</h3>
                  <p>Lites applies extremely fast, deterministic rules to strip out unnecessary tokens before hitting the LLM. This includes:</p>
                  <ul>
                    <li>Whitespace normalization (removing trailing spaces, extra newlines)</li>
                    <li>Removing duplicate or repetitive sentences</li>
                    <li>Stripping out filler words ("please", "thank you", "can you") depending on the context profile</li>
                  </ul>
                  <p style={{ marginTop: '1rem' }}>This layer executes in roughly <span className="highlight">~2ms</span> and guarantees identical semantic meaning.</p>
                </div>
              )}
              {activeTab === 'ai' && (
                <div>
                  <h3 style={{ marginTop: 0 }}>LLM-in-the-middle Compression</h3>
                  <p>If a prompt is extremely large (e.g., &gt;2000 tokens) and isn't cached, Lites will spawn a concurrent background task to a cheaper, faster LLM (like `gpt-3.5-turbo`) to summarize and compress the context *before* sending it to your expensive target model.</p>
                  <p>The AI Engine uses a strict system prompt to ensure that only redundant information is removed while preserving all critical code blocks and constraints.</p>
                </div>
              )}
              {activeTab === 'cache' && (
                <div>
                  <h3 style={{ marginTop: 0 }}>Vector-based Semantic Caching</h3>
                  <p>Unlike standard Exact Caches, Lites calculates a high-dimensional vector embedding for every incoming prompt.</p>
                  <p>When a new prompt arrives, Lites checks the Semantic Cache using cosine similarity. If the new prompt is semantically identical (e.g. <code>"How do I reverse a string?"</code> vs <code>"Can you tell me how to reverse a string?"</code>), Lites will return the cached response immediately, saving 100% of the token cost!</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Default to Getting Started / Quick Start
  return (
    <div>
      <h2 className="section-header">{activeSection}</h2>
      
      <div className="prose">
        <p>
          Lites runs as a transparent middleware proxy. To integrate it into your existing applications, 
          you only need to change the <span className="highlight">Base URL</span> of your OpenAI client to point to Lites.
        </p>

        <h3>Python Integration</h3>
        <p>Using the official OpenAI Python SDK:</p>
        
        <div className="code-block-container">
          <div className="code-header">
            <div className="window-controls">
              <div className="window-control wc-red"></div>
              <div className="window-control wc-yellow"></div>
              <div className="window-control wc-green"></div>
            </div>
            <div className="code-title">app.py</div>
          </div>
          <div className="code-content">
            <div><span className="code-keyword">import</span> openai</div>
            <br />
            <div><span className="code-comment"># Point the client to the local Lites proxy</span></div>
            <div>
              <span className="code-variable">client</span> = openai.<span className="code-function">Client</span>(
            </div>
            <div style={{ paddingLeft: '1rem' }}>
              base_url=<span className="code-string">"http://localhost:8000/v1"</span>,
            </div>
            <div style={{ paddingLeft: '1rem' }}>
              api_key=<span className="code-string">"YOUR_OPENAI_API_KEY"</span>
            </div>
            <div>)</div>
            <br />
            <div><span className="code-comment"># Lites will automatically compress the prompt, cache it, and execute it!</span></div>
            <div>
              <span className="code-variable">response</span> = client.chat.completions.<span className="code-function">create</span>(
            </div>
            <div style={{ paddingLeft: '1rem' }}>
              model=<span className="code-string">"gpt-4o"</span>,
            </div>
            <div style={{ paddingLeft: '1rem' }}>
              messages=[&#123; <span className="code-string">"role"</span>: <span className="code-string">"user"</span>, <span className="code-string">"content"</span>: <span className="code-string">"Please explain quantum mechanics in simple terms."</span> &#125;],
            </div>
            <div style={{ paddingLeft: '1rem' }}>
              extra_headers=&#123; <span className="code-string">"x-lites-context"</span>: <span className="code-string">"code"</span> &#125; <span className="code-comment"># Optional: Guide optimization</span>
            </div>
            <div>)</div>
            <br />
            <div><span className="code-function">print</span>(response.choices[<span className="code-keyword">0</span>].message.content)</div>
          </div>
        </div>
      </div>
    </div>
  );
}
