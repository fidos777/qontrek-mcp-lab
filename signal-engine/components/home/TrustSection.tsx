"use client";

import Link from 'next/link';
import Card from '@/components/shared/Card';

export default function TrustSection() {
  const trustFeatures = [
    {
      title: 'Draft Mode First',
      description: 'All outputs are drafts yang boleh di-review before final use',
      icon: '📝',
    },
    {
      title: 'Transparent Pricing',
      description: 'No hidden fees, pay per use dengan clear credit system',
      icon: '💰',
    },
    {
      title: 'Local Data',
      description: 'Your data stays secure dan processed locally when possible',
      icon: '🔒',
    },
    {
      title: 'Open Source Ready',
      description: 'Built with open standards untuk easy integration',
      icon: '🔓',
    },
  ];

  return (
    <section className="section-padding bg-gray-50">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Built for <span className="text-gradient">Trust</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transparency dan security are core to our platform design
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {trustFeatures.map((feature) => (
            <Card key={feature.title} variant="bordered" className="text-center">
              <div className="space-y-4">
                <div className="text-3xl">{feature.icon}</div>
                <h3 className="font-semibold text-lg">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.description}</p>
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 max-w-3xl mx-auto">
            <h3 className="font-semibold text-blue-900 mb-4">🛡️ Trust & Safety Commitment</h3>
            <p className="text-blue-800 text-sm mb-4">
              We're committed to building AI tools yang safe, reliable, dan beneficial untuk SME operations. 
              Our platform follows best practices untuk data privacy, security, dan ethical AI use.
            </p>
            <Link 
              href="/trust" 
              className="text-blue-600 hover:text-blue-800 font-medium text-sm"
            >
              Read our full Trust & Safety policy →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}