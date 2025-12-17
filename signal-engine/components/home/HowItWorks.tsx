"use client";

import Card from '@/components/shared/Card';

export default function HowItWorks() {
  const steps = [
    {
      step: '1',
      title: 'Choose Your Work',
      description: 'Select from Operations, Sales, atau Creative widgets based on your needs',
      icon: '🎯',
    },
    {
      step: '2',
      title: 'Fill the Form',
      description: 'Provide context dan details through dynamic forms yang mudah digunakan',
      icon: '📝',
    },
    {
      step: '3',
      title: 'AI Generates',
      description: 'Our lightweight engine processes your request dan generates output dalam seconds',
      icon: '⚡',
    },
    {
      step: '4',
      title: 'Review & Use',
      description: 'Get draft output yang boleh di-edit, save, atau integrate dengan your workflow',
      icon: '✅',
    },
  ];

  return (
    <section className="section-padding bg-gray-50">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            How It <span className="text-gradient">Works</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Simple 4-step process untuk automate your daily business tasks
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div key={step.step} className="relative">
              <Card variant="elevated" className="text-center h-full">
                <div className="space-y-4">
                  <div className="text-4xl mb-4">{step.icon}</div>
                  <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto">
                    {step.step}
                  </div>
                  <h3 className="font-semibold text-lg">{step.title}</h3>
                  <p className="text-gray-600 text-sm">{step.description}</p>
                </div>
              </Card>
              
              {/* Arrow for desktop */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 text-primary">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 max-w-2xl mx-auto">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <span className="text-2xl">🚧</span>
              <span className="font-semibold text-yellow-800">Draft Mode Only</span>
            </div>
            <p className="text-yellow-700 text-sm">
              Currently operating in draft mode. Witness verification dan proof generation coming soon!
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}