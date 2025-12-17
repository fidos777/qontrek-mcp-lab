"use client";

import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import { CREDIT_PACKS } from '@/lib/constants';
import { trackConversionClick } from '@/lib/track';

export default function CreditTeaser() {
  const handlePricingClick = () => {
    trackConversionClick('credit_teaser', 'pricing');
  };

  return (
    <section className="section-padding bg-white">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Simple <span className="text-gradient">Credit</span> System
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Pay per use dengan transparent pricing. No hidden fees, no monthly commitments.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {CREDIT_PACKS.map((pack) => (
            <Card 
              key={pack.id} 
              variant="bordered" 
              className={`text-center relative ${pack.popular ? 'border-primary border-2' : ''}`}
            >
              {pack.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary text-white px-3 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="space-y-4">
                <h3 className="font-bold text-xl">{pack.name}</h3>
                <div className="text-3xl font-bold text-primary">
                  RM{pack.price}
                </div>
                <div className="text-gray-600">
                  {pack.credits.toLocaleString()} credits
                </div>
                <p className="text-sm text-gray-500">{pack.description}</p>
                <div className="text-xs text-gray-400">
                  ~RM{(pack.price / pack.credits).toFixed(3)} per credit
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 max-w-2xl mx-auto mb-8">
            <h3 className="font-semibold text-blue-900 mb-2">💡 How Credits Work</h3>
            <p className="text-blue-800 text-sm">
              Each widget consumes different amounts of credits based on complexity. 
              Simple tasks like attendance tracking use 1-2 credits, while complex ones like proposal generation use 3-5 credits.
            </p>
          </div>
          
          <Button 
            variant="primary" 
            size="lg"
            onClick={handlePricingClick}
          >
            <Link href="/pricing">View Full Pricing Details</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}