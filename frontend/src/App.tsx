import { useState } from 'react';
import { Dashboard } from './components/Dashboard';
import { Documentation } from './components/Documentation';
import { Sidebar } from './components/Sidebar';
import { FlowchartAnimation } from './components/FlowchartAnimation';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'docs'>('dashboard');
  const [activeSection, setActiveSection] = useState('Quick Start');

  const handleSearch = (query: string) => {
    // Basic search functionality - handled internally by Sidebar, 
    // but we could also filter content here if needed.
    console.log("Searching docs for:", query);
  };

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

      <main className={activeTab === 'dashboard' ? "main-content" : "docs-layout"}>
        {activeTab === 'dashboard' ? (
          <>
            <Dashboard />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              <FlowchartAnimation />
              <Documentation activeSection="Integration Guide" hideSidebar={true} />
            </div>
          </>
        ) : (
          <>
            <Sidebar 
              onSearch={handleSearch} 
              activeSection={activeSection}
              setActiveSection={setActiveSection}
            />
            <div style={{ paddingTop: '1.5rem' }}>
              <Documentation activeSection={activeSection} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
