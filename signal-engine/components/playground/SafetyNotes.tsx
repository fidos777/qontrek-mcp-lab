"use client";

import Card from '@/components/shared/Card';

export default function SafetyNotes() {
  const safetyTips = [
    {
      icon: '📝',
      title: 'Draft Mode Only',
      description: 'All outputs are drafts yang boleh di-review dan edit before use',
    },
    {
      icon: '🔒',
      title: 'Data Privacy',
      description: 'Your input data is processed securely dan tidak disimpan permanently',
    },
    {
      icon: '⚡',
      title: 'Credit Usage',
      description: 'Credits are consumed upon successful generation, regardless of output quality',
    },
    {
      icon: '🎯',
      title: 'Best Results',
      description: 'Provide clear, specific context untuk better AI-generated outputs',
    },
  ];

  return (
    <Card variant="bordered" className="bg-blue-50 border-blue-200">
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">🛡️</span>
          <h3 className="font-semibold text-blue-900">Safety & Usage Notes</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {safetyTips.map((tip, index) => (
            <div key={index} className="flex items-start space-x-3">
              <span className="text-xl flex-shrink-0">{tip.icon}</span>
              <div>
                <h4 className="font-medium text-blue-900 text-sm">{tip.title}</h4>
                <p className="text-blue-800 text-xs">{tip.description}</p>
              </div>
            </div>
          ))}
        </div>
        
        <div className="pt-3 border-t border-blue-200">
          <p className="text-xs text-blue-700">
            <strong>Important:</strong> Always review AI-generated content before using in production. 
            KuasaTurbo provides tools to assist your work, not replace human judgment.
          </p>
        </div>
      </div>
    </Card>
  );
}