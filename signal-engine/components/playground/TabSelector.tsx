"use client";

import { PLAYGROUND_TABS } from '@/lib/constants';
import type { PlaygroundTab } from '@/lib/types';
import { trackTabView } from '@/lib/track';

interface TabSelectorProps {
  activeTab: PlaygroundTab;
  onTabChange: (tab: PlaygroundTab) => void;
}

export default function TabSelector({ activeTab, onTabChange }: TabSelectorProps) {
  const handleTabClick = (tabId: PlaygroundTab) => {
    onTabChange(tabId);
    trackTabView(tabId);
  };

  const activeIndex = PLAYGROUND_TABS.findIndex(tab => tab.id === activeTab);

  return (
    <div className="border-b border-gray-200 mb-6">
      <nav className="-mb-px flex space-x-8 relative">
        {/* Sliding indicator */}
        <div 
          className="absolute bottom-0 h-0.5 bg-primary transition-all duration-300 ease-out"
          style={{
            left: `${activeIndex * 120}px`,
            width: '80px',
          }}
        />
        
        {PLAYGROUND_TABS.map((tab, index) => (
          <button
            key={tab.id}
            onClick={() => handleTabClick(tab.id as PlaygroundTab)}
            className={`py-3 px-4 font-medium text-sm transition-all duration-200 min-h-[44px] rounded-t-lg ${
              activeTab === tab.id
                ? 'text-primary bg-primary/5'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <span className="flex items-center space-x-2">
              <span className="text-base">{tab.icon}</span>
              <span>{tab.label}</span>
            </span>
          </button>
        ))}
      </nav>
    </div>
  );
}