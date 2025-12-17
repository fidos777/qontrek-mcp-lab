"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { CREDIT_PACKS } from '@/lib/constants';
import { trackConversionClick } from '@/lib/track';

export default function PricingPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'pricing' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handleBuyClick = (packId: string) => {
    trackConversionClick('pricing_page', `buy_${packId}`);
  };

  const handleAPIClick = () => {
    trackConversionClick('pricing_page', 'api_access');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Simple <span className="text-yellow-300">Credit</span> Pricing
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Pay per use dengan transparent pricing. No hidden fees, no monthly commitments. 
            Credits never expire dan can be used across all widgets.
          </p>
        </div>
      </section>

      {/* Pricing Philosophy */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Why <span className="text-gradient">Credit-Based</span> Pricing?
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">💰</div>
                  <h3 className="font-semibold text-lg">Pay What You Use</h3>
                  <p className="text-gray-600 text-sm">
                    Only pay for actual AI generations. No wasted subscription fees untuk unused features.
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🔄</div>
                  <h3 className="font-semibold text-lg">Flexible Usage</h3>
                  <p className="text-gray-600 text-sm">
                    Use credits across all widgets - operations, sales, creative. Switch between tasks as needed.
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">⏰</div>
                  <h3 className="font-semibold text-lg">Never Expire</h3>
                  <p className="text-gray-600 text-sm">
                    Credits never expire. Buy when you need, use when you want. Perfect untuk irregular usage.
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Credit Packs */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">
              Choose Your <span className="text-gradient">Credit Pack</span>
            </h2>
            <p className="text-xl text-gray-600">
              Start small atau buy in bulk untuk better value
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {CREDIT_PACKS.map((pack) => (
              <Card 
                key={pack.id}
                variant="bordered"
                className={`text-center relative ${pack.popular ? 'border-primary border-2 shadow-lg' : ''}`}
              >
                {pack.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <Badge variant="primary" size="md">
                      Most Popular
                    </Badge>
                  </div>
                )}
                
                <div className="space-y-6 p-2">
                  <div>
                    <h3 className="font-bold text-2xl mb-2">{pack.name}</h3>
                    <div className="text-4xl font-bold text-primary mb-2">
                      RM{pack.price}
                    </div>
                    <div className="text-gray-600 text-lg">
                      {pack.credits.toLocaleString()} credits
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <p className="text-sm text-gray-600">{pack.description}</p>
                    <div className="text-xs text-gray-500">
                      ~RM{(pack.price / pack.credits).toFixed(3)} per credit
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="text-sm text-gray-600">
                      <strong>Enough for:</strong>
                    </div>
                    <div className="space-y-1 text-xs text-gray-500">
                      <div>• {Math.floor(pack.credits / 2)} social captions</div>
                      <div>• {Math.floor(pack.credits / 3)} invoices</div>
                      <div>• {Math.floor(pack.credits / 5)} proposals</div>
                    </div>
                  </div>
                  
                  <Button
                    variant={pack.popular ? "primary" : "outline"}
                    size="lg"
                    className="w-full"
                    onClick={() => handleBuyClick(pack.id)}
                  >
                    Buy {pack.name}
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Credit Usage Guide */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Credit <span className="text-gradient">Usage Guide</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">Low Cost (1-2 Credits)</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-center space-x-2">
                      <span className="text-green-500">•</span>
                      <span>Attendance tracking</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <span className="text-green-500">•</span>
                      <span>Expense categorization</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <span className="text-green-500">•</span>
                      <span>Task scheduling</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <span className="text-green-500">•</span>
                      <span>Social media captions</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">Medium Cost (3-5 Credits)</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-center space-x-2">
                      <span className="text-blue-500">•</span>
                      <span>Invoice generation</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <span className="text-blue-500">•</span>
                      <span>Lead qualification</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <span className="text-blue-500">•</span>
                      <span>Proposal generation</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <span className="text-blue-500">•</span>
                      <span>Follow-up scheduling</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Enterprise Section */}
      <section className="section-padding bg-secondary text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">
            Need <span className="text-yellow-300">Enterprise</span> Solutions?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            High volume usage, custom integrations, atau dedicated support? 
            Get API access dengan enterprise features.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="text-3xl mb-2">🔑</div>
              <h3 className="font-semibold mb-1">API Access</h3>
              <p className="text-sm text-gray-300">Direct integration dengan your systems</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-semibold mb-1">Volume Discounts</h3>
              <p className="text-sm text-gray-300">Better rates untuk high usage</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">🛠️</div>
              <h3 className="font-semibold mb-1">Priority Support</h3>
              <p className="text-sm text-gray-300">Dedicated technical assistance</p>
            </div>
          </div>
          
          <Button
            variant="secondary"
            size="lg"
            onClick={handleAPIClick}
          >
            <Link href="/api-access">Request API Access</Link>
          </Button>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Frequently Asked <span className="text-gradient">Questions</span>
            </h2>
            
            <div className="space-y-6">
              <Card variant="bordered">
                <div className="space-y-2">
                  <h3 className="font-semibold">Do credits expire?</h3>
                  <p className="text-gray-600 text-sm">
                    No, credits never expire. Buy once, use anytime. Perfect untuk businesses dengan irregular AI usage.
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-2">
                  <h3 className="font-semibold">Can I use credits across different widgets?</h3>
                  <p className="text-gray-600 text-sm">
                    Yes! Credits work across all widgets - operations, sales, creative. Switch between tasks as your business needs change.
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-2">
                  <h3 className="font-semibold">What happens if a generation fails?</h3>
                  <p className="text-gray-600 text-sm">
                    Credits are only charged for successful generations. If something goes wrong, you don't pay.
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-2">
                  <h3 className="font-semibold">Can I get a refund?</h3>
                  <p className="text-gray-600 text-sm">
                    Unused credits can be refunded within 30 days of purchase. Contact support untuk assistance.
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}