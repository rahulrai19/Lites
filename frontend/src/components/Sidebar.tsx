import { useState } from 'react';
import { Search, ChevronDown } from 'lucide-react';

interface SidebarProps {
  onSearch: (query: string) => void;
  activeSection: string;
  setActiveSection: (section: string) => void;
}

export function Sidebar({ onSearch, activeSection, setActiveSection }: SidebarProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set());
  
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    onSearch(value);
  };

  const toggleSection = (title: string) => {
    setCollapsedSections(prev => {
      const next = new Set(prev);
      if (next.has(title)) next.delete(title);
      else next.add(title);
      return next;
    });
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
      title: 'Guides',
      items: ['Using context effectively', 'Best Practices', 'Configuration', 'Docker']
    },
    {
      title: 'Reference',
      items: ['CLI Reference', 'Architecture Overview']
    },
    {
      title: 'Advanced',
      items: [
        'How Exact Caching works',
        'How Rule-based Prompts work',
        'How Context Compression works',
        'How Semantic Caching works',
        'How AI Compression works',
        'How Adaptive Routing works'
      ]
    },
    {
      title: 'Community',
      items: ['Contributing', 'FAQ']
    },
    {
      title: 'Comparison',
      items: ['Lites vs existing tools']
    }
  ];

  return (
    <aside className="sidebar">
      <nav>
        {menu.map((section, idx) => (
          <div key={idx} className="sidebar-section">
            <div 
              className="sidebar-heading" 
              onClick={() => toggleSection(section.title)}
              style={{ userSelect: 'none' }}
            >
              {section.title}
              <ChevronDown 
                size={14} 
                style={{ 
                  transform: collapsedSections.has(section.title) ? 'rotate(-90deg)' : 'none', 
                  transition: 'transform 0.2s ease' 
                }} 
              />
            </div>
            
            {!collapsedSections.has(section.title) && (
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
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
