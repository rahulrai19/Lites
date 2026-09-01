import { useState } from 'react';
import { Search, ChevronDown } from 'lucide-react';

interface SidebarProps {
  onSearch: (query: string) => void;
  activeSection: string;
  setActiveSection: (section: string) => void;
}

export function Sidebar({ onSearch, activeSection, setActiveSection }: SidebarProps) {
  const [searchTerm, setSearchTerm] = useState('');
  
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    onSearch(value);
  };

  const menu = [
    {
      title: 'Introduction',
      items: ['What is Lites', 'Why it exists']
    },
    {
      title: 'Getting Started',
      items: ['Installation', 'Quick Start', 'Basic Usage']
    },
    {
      title: 'Core Concepts',
      items: ['Rule Optimization', 'AI Compression', 'Semantic Caching']
    }
  ];

  return (
    <aside className="sidebar">
      <div className="search-container">
        <span className="search-icon">
          <Search size={16} />
        </span>
        <input 
          type="text" 
          className="search-input" 
          placeholder="Search documentation..." 
          value={searchTerm}
          onChange={handleSearch}
        />
      </div>

      <nav>
        {menu.map((section, idx) => (
          <div key={idx} className="sidebar-section">
            <div className="sidebar-heading">
              {section.title}
              <ChevronDown size={14} />
            </div>
            <ul className="sidebar-list">
              {section.items.map((item, itemIdx) => {
                // Determine visibility based on search
                const isVisible = item.toLowerCase().includes(searchTerm.toLowerCase());
                
                if (!isVisible && searchTerm !== '') return null;
                
                return (
                  <li key={itemIdx}>
                    <button 
                      className={`sidebar-link ${activeSection === item ? 'active' : ''}`}
                      onClick={() => setActiveSection(item)}
                      style={{ background: 'none', border: 'none', width: '100%', textAlign: 'left', cursor: 'pointer' }}
                    >
                      {item}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );
}
