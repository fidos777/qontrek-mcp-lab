"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { trackConversionClick } from '@/lib/track';

export default function PartnersPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'partners' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handlePartnerClick = () => {
    trackConversionClick('partners_page', 'apply');
  };

  const handleWhatsAppClick = () => {
    trackConversionClick('partners_page', 'whatsapp');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Partner with <span className="text-yellow-300">KuasaTurbo</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Join our ecosystem of technology partners, integrators, dan solution providers
          </p>
          <Badge variant="secondary" size="md" className="bg-yellow-400 text-yellow-900">
            Partnership Opportunities Available
          </Badge>
        </div>
      </section>

      {/* Partnership Types */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Partnership <span className="text-gradient">Opportunities</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🔗</div>
                  <h3 className="font-semibold text-lg">Technology Partners</h3>
                  <p className="text-gray-600 text-sm">
                    Integrate your platform with KuasaTurbo APIs dan expand your offering
                  </p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    <li>• CRM integrations</li>
                    <li>• Accounting software</li>
                    <li>• E-commerce platforms</li>
                    <li>• WhatsApp Business APIs</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🏢</div>
                  <h3 className="font-semibold text-lg">Solution Partners</h3>
                  <p className="text-gray-600 text-sm">
                    Build custom solutions using KuasaTurbo as your AI engine
                  </p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    <li>• White-label solutions</li>
                    <li>• Industry-specific apps</li>
                    <li>• Custom integrations</li>
                    <li>• Vertical specializations</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🌐</div>
                  <h3 className="font-semibold text-lg">Channel Partners</h3>
                  <p className="text-gray-600 text-sm">
                    Resell KuasaTurbo to your existing client base dan earn commissions
                  </p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    <li>• Digital agencies</li>
                    <li>• IT consultants</li>
                    <li>• Business coaches</li>
                    <li>• System integrators</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Partner <span className="text-gradient">Benefits</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🚀 Technical Benefits</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Full API access with comprehensive documentation</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Dedicated technical support dan integration assistance</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Early access to new features dan beta programs</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>White-label options for your brand</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">💰 Business Benefits</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Revenue sharing on successful integrations</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Co-marketing opportunities dan joint campaigns</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Lead sharing dan referral programs</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Priority support for your clients</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Integration Examples */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Integration <span className="text-gradient">Examples</span>
            </h2>
            
            <div className="space-y-8">
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="flex flex-col md:flex-row items-start space-y-4 md:space-y-0 md:space-x-6">
                  <div className="text-4xl">📊</div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-blue-900 mb-2">CRM Integration</h3>
                    <p className="text-blue-800 text-sm mb-3">
                      Connect your CRM with KuasaTurbo to automatically generate proposals, 
                      follow-up messages, dan sales materials based on lead data.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700">HubSpot</Badge>
                      <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700">Salesforce</Badge>
                      <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700">Pipedrive</Badge>
                    </div>
                  </div>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="flex flex-col md:flex-row items-start space-y-4 md:space-y-0 md:space-x-6">
                  <div className="text-4xl">💬</div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-green-900 mb-2">WhatsApp Business API</h3>
                    <p className="text-green-800 text-sm mb-3">
                      Embed KuasaTurbo widgets directly in WhatsApp conversations 
                      for instant quotes, bookings, dan customer service.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline" size="sm" className="border-green-300 text-green-700">WhatsApp Business</Badge>
                      <Badge variant="outline" size="sm" className="border-green-300 text-green-700">Twilio</Badge>
                      <Badge variant="outline" size="sm" className="border-green-300 text-green-700">MessageBird</Badge>
                    </div>
                  </div>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-purple-50 border-purple-200">
                <div className="flex flex-col md:flex-row items-start space-y-4 md:space-y-0 md:space-x-6">
                  <div className="text-4xl">🛒</div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-purple-900 mb-2">E-commerce Platform</h3>
                    <p className="text-purple-800 text-sm mb-3">
                      Add AI-powered product descriptions, customer support, 
                      dan marketing content generation to your e-commerce platform.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline" size="sm" className="border-purple-300 text-purple-700">Shopify</Badge>
                      <Badge variant="outline" size="sm" className="border-purple-300 text-purple-700">WooCommerce</Badge>
                      <Badge variant="outline" size="sm" className="border-purple-300 text-purple-700">Magento</Badge>
                    </div>
                  </div>
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
              Partnership <span className="text-gradient">Requirements</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">✅ Technical Requirements</h3>
                  <ul className="space-y-2 text-sm text-green-800">
                    <li>• REST API integration experience</li>
                    <li>• Understanding of webhook implementations</li>
                    <li>• JSON data handling capabilities</li>
                    <li>• Basic authentication dan security practices</li>
                    <li>• Ability to handle async operations</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">⭐ Business Requirements</h3>
                  <ul className="space-y-2 text-sm text-blue-800">
                    <li>• Established business with existing clients</li>
                    <li>• Commitment to joint go-to-market activities</li>
                    <li>• Dedicated technical dan business resources</li>
                    <li>• Alignment with KuasaTurbo's values</li>
                    <li>• Focus on SME market segment</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Partnership Process */}
      <section className="section-padding bg-secondary text-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Partnership <span className="text-yellow-300">Process</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { step: '1', title: 'Apply', desc: 'Submit partnership application' },
                { step: '2', title: 'Evaluate', desc: 'Technical dan business assessment' },
                { step: '3', title: 'Integrate', desc: 'Technical integration dan testing' },
                { step: '4', title: 'Launch', desc: 'Go-to-market dan ongoing support' },
              ].map((item, index) => (
                <Card key={index} variant="bordered" className="text-center bg-white text-gray-900">
                  <div className="space-y-3">
                    <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto">
                      {item.step}
                    </div>
                    <h3 className="font-semibold">{item.title}</h3>
                    <p className="text-sm text-gray-600">{item.desc}</p>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-primary text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">
            Ready to <span className="text-yellow-300">Partner</span> with Us?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join our growing ecosystem of partners dan help SMEs across Malaysia leverage AI for their business growth.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              size="lg"
              onClick={handlePartnerClick}
            >
              <Link href="/api-access">Apply for Partnership</Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleWhatsAppClick}
            >
              <a href="https://wa.me/60123456789" target="_blank" rel="noopener noreferrer">
                Discuss Partnership
              </a>
            </Button>
          </div>
          
          <p className="text-sm text-orange-200 mt-6">
            Partnership inquiries: partnerships@kuasaturbo.com
          </p>
        </div>
      </section>
    </div>
  );
}