"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { trackConversionClick } from '@/lib/track';

export default function ResellerPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'reseller' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handleApplyClick = () => {
    trackConversionClick('reseller_page', 'apply');
  };

  const handleWhatsAppClick = () => {
    trackConversionClick('reseller_page', 'whatsapp');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Become a KuasaTurbo <span className="text-yellow-300">Reseller</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Earn recurring revenue by selling AI automation solutions to SMEs in your network
          </p>
          <Badge variant="secondary" size="md" className="bg-yellow-400 text-yellow-900">
            High Commission Program
          </Badge>
        </div>
      </section>

      {/* Why Become a Reseller */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Why Become a <span className="text-gradient">Reseller</span>?
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">💰</div>
                  <h3 className="font-semibold text-lg">High Commissions</h3>
                  <p className="text-gray-600 text-sm">
                    Earn 25-40% commission on all sales plus recurring revenue from client usage
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🚀</div>
                  <h3 className="font-semibold text-lg">Growing Market</h3>
                  <p className="text-gray-600 text-sm">
                    AI automation is exploding - be first to market in your area
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🎯</div>
                  <h3 className="font-semibold text-lg">Easy to Sell</h3>
                  <p className="text-gray-600 text-sm">
                    Proven ROI, instant demos, dan clear value proposition for SMEs
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Reseller Benefits */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Reseller <span className="text-gradient">Benefits</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">💼 Sales Support</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Complete sales training dan certification</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Marketing materials dan demo scripts</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Lead generation support dan referrals</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Joint sales calls for large deals</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">🛠️ Technical Support</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Technical training on all features</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Implementation support for clients</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Dedicated technical support channel</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Custom integration assistance</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Commission Structure */}
      <section className="section-padding bg-secondary text-white">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6">
              Commission <span className="text-yellow-300">Structure</span>
            </h2>
            <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
              Earn more as you sell more. Our tiered commission structure rewards top performers.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700">Bronze</Badge>
                  <div className="text-3xl font-bold text-blue-600">25%</div>
                  <h3 className="font-semibold">Starter Reseller</h3>
                  <p className="text-sm text-gray-600">0-10 clients per month</p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    <li>• 25% on initial sales</li>
                    <li>• 10% recurring revenue</li>
                    <li>• Basic support</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-white text-gray-900 border-2 border-yellow-400">
                <div className="text-center space-y-4">
                  <Badge variant="secondary" size="sm" className="bg-yellow-400 text-yellow-900">Silver</Badge>
                  <div className="text-3xl font-bold text-yellow-600">35%</div>
                  <h3 className="font-semibold">Professional Reseller</h3>
                  <p className="text-sm text-gray-600">11-25 clients per month</p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    <li>• 35% on initial sales</li>
                    <li>• 15% recurring revenue</li>
                    <li>• Priority support</li>
                    <li>• Marketing co-op funds</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <Badge variant="outline" size="sm" className="border-orange-300 text-orange-700">Gold</Badge>
                  <div className="text-3xl font-bold text-orange-600">40%</div>
                  <h3 className="font-semibold">Elite Reseller</h3>
                  <p className="text-sm text-gray-600">25+ clients per month</p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    <li>• 40% on initial sales</li>
                    <li>• 20% recurring revenue</li>
                    <li>• Dedicated account manager</li>
                    <li>• Custom pricing authority</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Target Customers */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Perfect <span className="text-gradient">Target Customers</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">🎯 Ideal Prospects</h3>
                  <ul className="space-y-2 text-sm text-green-800">
                    <li>• SMEs with 5-50 employees</li>
                    <li>• Businesses doing repetitive tasks manually</li>
                    <li>• Companies wanting to improve customer service</li>
                    <li>• Businesses struggling with content creation</li>
                    <li>• Organizations looking to reduce costs</li>
                    <li>• Companies wanting to scale operations</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🏢 Best Industries</h3>
                  <ul className="space-y-2 text-sm text-blue-800">
                    <li>• Automotive dealerships</li>
                    <li>• F&B restaurants dan cafes</li>
                    <li>• Property agencies</li>
                    <li>• Insurance agencies</li>
                    <li>• Retail stores</li>
                    <li>• Professional services</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Requirements */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Reseller <span className="text-gradient">Requirements</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">✅ Must Have</h3>
                  <ul className="space-y-2 text-sm text-green-800">
                    <li>• Existing SME client network</li>
                    <li>• Sales experience (any industry)</li>
                    <li>• Basic understanding of business processes</li>
                    <li>• Commitment to monthly sales targets</li>
                    <li>• Fluent in BM/EN</li>
                    <li>• Based in Malaysia</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">⭐ Nice to Have</h3>
                  <ul className="space-y-2 text-sm text-blue-800">
                    <li>• Technology or SaaS sales experience</li>
                    <li>• Existing relationships with SMEs</li>
                    <li>• Understanding of AI/automation</li>
                    <li>• Digital marketing knowledge</li>
                    <li>• Industry specialization</li>
                    <li>• Business development background</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Reseller <span className="text-gradient">Success Stories</span>
            </h2>
            
            <div className="space-y-6">
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="space-y-4">
                  <div className="flex items-start space-x-4">
                    <div className="text-4xl">👨‍💼</div>
                    <div>
                      <h3 className="font-semibold text-lg text-blue-900">Ahmad, Digital Agency Owner</h3>
                      <p className="text-blue-800 text-sm mb-3">
                        "Started reselling KuasaTurbo 6 months ago. Now earning RM8,000+ monthly 
                        commission by offering AI automation to my existing web design clients."
                      </p>
                      <div className="flex space-x-4 text-xs text-blue-700">
                        <span>• 35 clients onboarded</span>
                        <span>• RM8,500 monthly commission</span>
                        <span>• 95% client retention</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="space-y-4">
                  <div className="flex items-start space-x-4">
                    <div className="text-4xl">👩‍💼</div>
                    <div>
                      <h3 className="font-semibold text-lg text-green-900">Sarah, Business Consultant</h3>
                      <p className="text-green-800 text-sm mb-3">
                        "KuasaTurbo became my secret weapon. I help SMEs automate their processes 
                        dan earn recurring revenue. My clients love the instant ROI."
                      </p>
                      <div className="flex space-x-4 text-xs text-green-700">
                        <span>• 28 clients onboarded</span>
                        <span>• RM6,200 monthly commission</span>
                        <span>• 40% upsell rate</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-primary text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">
            Ready to Start <span className="text-yellow-300">Earning</span>?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join our reseller program today dan start earning high commissions from AI automation sales.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              size="lg"
              onClick={handleApplyClick}
            >
              <Link href="/api-access">Apply as Reseller</Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleWhatsAppClick}
            >
              <a href="https://wa.me/60123456789" target="_blank" rel="noopener noreferrer">
                WhatsApp Us
              </a>
            </Button>
          </div>
          
          <p className="text-sm text-orange-200 mt-6">
            Reseller inquiries: resellers@kuasaturbo.com
          </p>
        </div>
      </section>
    </div>
  );
}