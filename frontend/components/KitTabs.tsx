'use client';

import { useState } from 'react';

interface KitTabsProps {
  children: React.ReactNode[];
}

const tabs = [
  'Architecture',
  'Components',
  'Hotspots',
  'First Tasks',
  'Patterns',
  'Setup',
];

export default function KitTabs({ children }: KitTabsProps) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div>
      {/* Tab bar */}
      <div className="flex gap-2 flex-wrap mb-4">
        {tabs.map((tab, idx) => (
          <button
            key={idx}
            onClick={() => setActiveTab(idx)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
              activeTab === idx
                ? 'text-white border border-transparent'
                : 'bg-secondary text-muted-foreground border border-transparent hover:text-foreground hover:border-border'
            }`}
            style={activeTab === idx ? {
              background: '#0062FF',
              boxShadow: '0 0 16px rgba(0, 98, 255, 0.3)'
            } : {}}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Content area */}
      <div 
        key={activeTab}
        className="rounded-xl border border-border bg-card p-6 mt-2 animate-fade-in"
      >
        {children[activeTab]}
      </div>
    </div>
  );
}

// Made with Bob
