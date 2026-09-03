interface DocsProps {
  activeSection: string;
  hideSidebar?: boolean;
  stepRange?: [number, number];
  hideTitle?: boolean;
}

export function Documentation({ activeSection, hideSidebar = false, stepRange, hideTitle = false }: DocsProps) {
  const containerClass = hideSidebar ? "" : "docs-main-area";

  // If the user clicks on Core Concepts, show MVP Cards
  if (activeSection === 'Rule Optimization' || activeSection === 'AI Compression' || activeSection === 'Semantic Caching' || activeSection === 'Core Concepts') {
    return (
      <div className={containerClass}>
        <div>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>Core Concepts</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', marginBottom: '2rem' }}>
            Lites intercepts and optimizes requests using a progressive sequence of techniques. 
            By avoiding unnecessary LLM calls, it significantly reduces inference expenditure and latency.
          </p>

          <div className="mvp-grid">

            <div className="card">
              <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', fontSize: '1.2rem' }}>1. Rule-Based Prompts</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                Deterministic optimization that removes duplicate content, extra whitespaces, and repeating sentences.
                Executes in ~2ms with zero token cost.
              </p>
            </div>
            
            <div className="card">
              <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', fontSize: '1.2rem' }}>2. Context Compression</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                Long-running conversations are compressed by summarizing historical context while preserving recent task-relevant messages.
              </p>
            </div>

            <div className="card">
              <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', fontSize: '1.2rem' }}>3. Semantic Caching</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                Creates a vector embedding of the request. If an identical semantic match exists in Redis, it returns the cached response instantly.
              </p>
            </div>

            <div className="card">
              <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', fontSize: '1.2rem' }}>4. AI Compression</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                For highly complex prompts, an optional small/fast LLM is used to summarize and strip out noise before passing it to an expensive model like GPT-4.
              </p>
            </div>
            
            <div className="card" style={{ gridColumn: '1 / -1' }}>
              <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', fontSize: '1.2rem' }}>5. Adaptive Routing</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                Evaluates task complexity, required quality, cost, and latency constraints to dynamically select the most appropriate LLM from the provider pool, ensuring the lowest cost for the required capability.
              </p>
            </div>
          </div>
        </div>
        
        {/* Right Sidebar */}
        {!hideSidebar && (
          <div>
            <div className="toc-container">
              <div className="toc-title">On this page</div>
              <ul className="toc-list">
                <li><a href="#">Overview</a></li>
                <li><a href="#">Rule-Based Prompts</a></li>
                <li><a href="#">Context Compression</a></li>
                <li><a href="#">Semantic Caching</a></li>
                <li><a href="#">AI Compression</a></li>
                <li><a href="#">Adaptive Routing</a></li>
              </ul>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (activeSection === 'What is Lites' || activeSection === 'Why it exists' || activeSection === 'Introduction') {
    return (
      <div className={containerClass}>
        <div>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>{activeSection}</h2>
          <div className="prose">
            {activeSection === 'What is Lites' || activeSection === 'Introduction' ? (
              <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>Lites is a cost-aware LLM optimization gateway for efficient AI inference. It sits between your application and your LLM providers, analyzing token and context characteristics to apply deterministic optimization, semantic caching, and adaptive model routing—drastically reducing your token consumption and latency.</p>
            ) : (
              <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>As applications generate longer prompts and maintain multi-turn conversations, unnecessary token processing becomes a significant operational cost. Lites exists to eliminate redundant content, cache reusable responses, and dynamically select the cheapest viable model to ensure you only pay for useful computation.</p>
            )}
          </div>
        </div>
        {!hideSidebar && (
          <div>
            <div className="toc-container">
              <div className="toc-title">On this page</div>
              <ul className="toc-list">
                <li><a href="#">Overview</a></li>
                <li><a href="#">Architecture</a></li>
              </ul>
            </div>
          </div>
        )}
      </div>
    );
  }

  // Default to Getting Started / Quick Start
  return (
    <div className={containerClass}>
      <div>
        {!hideTitle && (
          <>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>Quick Start</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', marginBottom: '2.5rem' }}>
              Lites runs as a transparent middleware proxy. The fastest way to optimize your LLM costs is to integrate it into your existing codebase by simply pointing your client to the local gateway.
            </p>
          </>
        )}

        {(!stepRange || (stepRange[0] <= 1 && stepRange[1] >= 1)) && (
          <div className="step-item">
          <div className="step-number">1</div>
          <div className="step-line"></div>
          <div className="step-content">
            <div className="step-title">Start the Lites Gateway</div>
            <div className="step-desc">Open your terminal and boot up the Lites Python backend with Redis caching enabled.</div>
            <div className="code-block-container" style={{ margin: 0 }}>
              <div className="code-header">
                <div className="window-controls">
                  <div className="window-control wc-red"></div>
                  <div className="window-control wc-yellow"></div>
                  <div className="window-control wc-green"></div>
                </div>
              </div>
              <div className="code-content">
                <div><span style={{ color: 'var(--accent-red)' }}>$</span> python -m lites.cli up</div>
              </div>
            </div>
          </div>
        </div>
        )}

        {(!stepRange || (stepRange[0] <= 2 && stepRange[1] >= 2)) && (
        <div className="step-item">
          <div className="step-number">2</div>
          <div className="step-line"></div>
          <div className="step-content">
            <div className="step-title">Node.js / TypeScript Integration</div>
            <div className="step-desc">Change the base URL of your OpenAI client to point to the proxy.</div>
            <div className="code-block-container" style={{ margin: 0 }}>
              <div className="code-header">
                <div className="window-controls">
                  <div className="window-control wc-red"></div>
                  <div className="window-control wc-yellow"></div>
                  <div className="window-control wc-green"></div>
                </div>
                <div className="code-title">index.ts</div>
              </div>
              <div className="code-content">
                <div><span style={{ color: '#ff7b72' }}>import</span> OpenAI <span style={{ color: '#ff7b72' }}>from</span> <span style={{ color: '#a5d6ff' }}>'openai'</span>;</div>
                <br />
                <div><span style={{ color: '#8b949e' }}>// Point the client to the local Lites proxy</span></div>
                <div><span style={{ color: '#ff7b72' }}>const</span> client = <span style={{ color: '#ff7b72' }}>new</span> <span style={{ color: '#d2a8ff' }}>OpenAI</span>(&#123;</div>
                <div style={{ paddingLeft: '1rem' }}>baseURL: <span style={{ color: '#a5d6ff' }}>"http://localhost:8000/v1"</span>,</div>
                <div style={{ paddingLeft: '1rem' }}>apiKey: <span style={{ color: '#a5d6ff' }}>"test-lites-key"</span></div>
                <div>&#125;);</div>
              </div>
            </div>
          </div>
        </div>
        )}

        {(!stepRange || (stepRange[0] <= 3 && stepRange[1] >= 3)) && (
        <div className="step-item">
          <div className="step-number">3</div>
          <div className="step-line"></div>
          <div className="step-content">
            <div className="step-title">Python Integration</div>
            <div className="step-desc">You can also use the official OpenAI Python SDK.</div>
            <div className="code-block-container" style={{ margin: 0 }}>
              <div className="code-header">
                <div className="window-controls">
                  <div className="window-control wc-red"></div>
                  <div className="window-control wc-yellow"></div>
                  <div className="window-control wc-green"></div>
                </div>
                <div className="code-title">app.py</div>
              </div>
              <div className="code-content">
                <div><span style={{ color: '#ff7b72' }}>import</span> openai</div>
                <div><span style={{ color: '#ff7b72' }}>from</span> lites <span style={{ color: '#ff7b72' }}>import</span> LitesClient</div>
                <br />
                <div><span style={{ color: '#8b949e' }}># Initialize proxy</span></div>
                <div>client = openai.<span style={{ color: '#d2a8ff' }}>Client</span>(</div>
                <div style={{ paddingLeft: '1rem' }}>base_url=<span style={{ color: '#a5d6ff' }}>"http://localhost:8000/v1"</span>,</div>
                <div style={{ paddingLeft: '1rem' }}>api_key=<span style={{ color: '#a5d6ff' }}>"test-lites-key"</span></div>
                <div>)</div>
              </div>
            </div>
          </div>
        </div>
        )}

        {(!stepRange || (stepRange[0] <= 4 && stepRange[1] >= 4)) && (
        <div className="step-item">
          <div className="step-number">4</div>
          <div className="step-line"></div>
          <div className="step-content">
            <div className="step-title">Observe Optimization</div>
            <div className="step-desc">All requests are automatically optimized. Check the Dashboard to see real-time metrics on token savings and semantic cache hits.</div>
            <div className="code-block-container" style={{ margin: 0 }}>
              <div className="code-header">
                <div className="window-controls">
                  <div className="window-control wc-red"></div>
                  <div className="window-control wc-yellow"></div>
                  <div className="window-control wc-green"></div>
                </div>
              </div>
              <div className="code-content">
                <div>response = client.chat.completions.<span style={{ color: '#d2a8ff' }}>create</span>(</div>
                <div style={{ paddingLeft: '1rem' }}>model=<span style={{ color: '#a5d6ff' }}>"gpt-4"</span>,</div>
                <div style={{ paddingLeft: '1rem' }}>messages=[&#123; <span style={{ color: '#a5d6ff' }}>"role"</span>: <span style={{ color: '#a5d6ff' }}>"user"</span>, <span style={{ color: '#a5d6ff' }}>"content"</span>: <span style={{ color: '#a5d6ff' }}>"Hello"</span> &#125;]</div>
                <div>)</div>
              </div>
            </div>
          </div>
        </div>
        )}

      </div>

      {/* Right Sidebar */}
      {!hideSidebar && (
        <div>
          <div className="toc-container">
            <div className="toc-title">On this page</div>
            <ul className="toc-list">
              <li><a href="#">Overview</a></li>
              <li><a href="#">Start the Gateway</a></li>
              <li><a href="#">Node.js Integration</a></li>
              <li><a href="#">Python Integration</a></li>
              <li><a href="#">Testing</a></li>
            </ul>
          </div>
        </div>
      )}

    </div>
  );
}
