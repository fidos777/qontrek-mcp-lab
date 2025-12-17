"use client";

import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import { trackConversionClick } from '@/lib/track';

export default function PartnerTeaser() {
  const partnerTypes = [
    {
      title: 'Consultants',
      description: 'Help clients implement AI workflows',
      icon: '👨‍💼',
      benefits: ['Revenue sharing', 'Training provided', 'Client referrals'],
      cta: 'Become Consultant',
      href: '/consultant',
    },
    {
      title: 'Resellers',
      description: 'Sell KuasaTurbo to your network',
      icon: '🤝',
      benefits: ['Wholesale pricing', 'Marketing support', 'Technical training'],
      cta: 'Join Reseller Program',
      href: '/reseller',
    },
    {
      title: 'Partners',
      description: 'Integrate with our platform',
      icon: '🔗',
      benefits: ['API access', 'Co-marketing', 'Technical support'],
      cta: 'Explore Partnership',
      href: '/partners',
    },
  ];

  const handlePartnerClick = (type: string) => {
    trackConversionClick('partner_teaser', type);
  };

  return (
    <section className="section-padding bg-white">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Partner <span className="text-gradient">Ecosystem</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Join our growing network of consultants, resellers, dan technology partners
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {partnerTypes.map((partner) => (
            <Card key={partner.title} variant="bordered" className="text-center hover:shadow-lg transition-shadow">
              <div className="space-y-6">
                <div className="text-4xl">{partner.icon}</div>
                
                <div>
                  <h3 className="font-bold text-xl mb-2">{partner.title}</h3>
                  <p className="text-gray-600 mb-4">{partner.description}</p>
                </div>
                
                <div className="space-y-2">
                  {partner.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center justify-center space-x-2 text-sm text-gray-600">
                      <span className="text-green-500">✓</span>
                      <span>{benefit}</span>
                    </div>
                  ))}
                </div>
                
                <Button 
                  variant="outline" 
                  className="w-full"
                  onClick={() => handlePartnerClick(partner.title.toLowerCase())}
                >
                  <Link href={partner.href}>{partner.cta}</Link>
                </Button>
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12">
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-6 max-w-2xl mx-auto">
            <h3 className="font-semibold text-purple-900 mb-2">🚀 Early Partner Benefits</h3>
            <p className="text-purple-800 text-sm">
              Join now during our growth phase untuk exclusive benefits dan priority support. 
              Limited spots available!
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}