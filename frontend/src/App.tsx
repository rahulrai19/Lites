import { useState } from 'react';
import { Dashboard } from './components/Dashboard';
import { Documentation } from './components/Documentation';
import { Sidebar } from './components/Sidebar';
import { DetailedFlowchart } from './components/DetailedFlowchart';
import { TutorialVideoCard } from './components/TutorialVideoCard';
import { Tutorials } from './components/Tutorials';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'tutorials' | 'docs'>('dashboard');
  const [activeSection, setActiveSection] = useState('Quick Start');

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="navbar-brand">
          Lites
        </div>
        <div className="navbar-nav">
          <button 
            className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={`nav-link ${activeTab === 'tutorials' ? 'active' : ''}`}
            onClick={() => setActiveTab('tutorials')}
          >
            Tutorials
          </button>
          <button 
            className={`nav-link ${activeTab === 'docs' ? 'active' : ''}`}
            onClick={() => setActiveTab('docs')}
          >
            Docs
          </button>
          <a href="https://github.com/rahulrai19/Lites" target="_blank" rel="noreferrer" className="nav-link">
            GitHub
          </a>
        </div>
        <div>
          <button className="btn-primary" onClick={() => setActiveTab('docs')}>
            Get Started
          </button>
        </div>
      </nav>

      <main className={activeTab === 'dashboard' ? "main-content" : activeTab === 'tutorials' ? "tutorials-layout" : "docs-layout"}>
        {activeTab === 'dashboard' && (
          <>
            {/* Hero Section */}
            <div className="hero-section" style={{ gridColumn: '1 / -1' }}>
              <h1 className="hero-title">Welcome to Lites</h1>
              <p className="hero-subtitle">
                The fastest way to optimize your LLM costs and latency with exact caching, semantic caching, and AI compression.
              </p>
              <div className="hero-actions">
                <button className="pill-btn" onClick={() => setActiveTab('tutorials')}>
                  Watch Tutorial
                </button>
                <button 
                  className="pill-btn" 
                  style={{ background: 'transparent', border: '1px solid rgba(255,255,255,0.2)', color: '#fff' }} 
                  onClick={() => setActiveTab('docs')}
                >
                  Documentation
                </button>
                <a href="https://www.npmjs.com/package/lites-sdk" target="_blank" rel="noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div className="pill-code">
                    <span className="pkg-mgr">NPM</span>
                    <code>npm i lites-sdk</code>
                  </div>
                </a>
                <a href="https://pypi.org/project/lites-sdk/" target="_blank" rel="noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div className="pill-code">
                    <span className="pkg-mgr">PyPI</span>
                    <code>pip install lites-sdk</code>
                  </div>
                </a>
              </div>
            </div>

            {/* Glassmorphic Tutorial Video Showcase in Dashboard */}
            <div style={{ gridColumn: '1 / -1', marginBottom: '1rem' }}>
              <TutorialVideoCard 
                title="Lites in Action: Interactive Architecture & Compression Demo"
                subtitle="Watch how Lites intercepts incoming LLM completions, resolves semantic Redis cache hits in 12ms, and compresses token context by up to 48%."
              />
            </div>

            {/* Left Column */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              <Dashboard />
              <div style={{ marginTop: '2rem' }}>
                <Documentation activeSection="Integration Guide" hideSidebar={true} stepRange={[1, 2]} />
              </div>
            </div>

            {/* Right Column */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              <DetailedFlowchart />
              <div style={{ marginTop: '2rem', paddingLeft: '1rem' }}>
                <Documentation activeSection="Integration Guide" hideSidebar={true} stepRange={[3, 4]} hideTitle={true} />
              </div>
            </div>
          </>
        )}

        {activeTab === 'tutorials' && (
          <Tutorials />
        )}

        {activeTab === 'docs' && (
          <>
            <Sidebar 
              activeSection={activeSection}
              setActiveSection={setActiveSection}
            />
            <div style={{ padding: '2rem 4rem', maxWidth: '1100px', width: '100%', margin: '0 auto' }}>
              <Documentation activeSection={activeSection} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
