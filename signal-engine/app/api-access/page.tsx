"use client";

import { useEffect, useState } from 'react';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import ApiAccessForm from '@/components/forms/ApiAccessForm';
import { trackConversionClick } from '@/lib/track';

export default function ApiAccessPage() {
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'api_access' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handleGetAccessClick = () => {
    trackConversionClick('api_access_page', 'get_access');
    setShowForm(true);
  };

  const handleWhatsAppClick = () => {
    trackConversionClick('api_access_page', 'whatsapp');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Get <span className="text-yellow-300">API Access</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Integrate KuasaTurbo's AI capabilities into your applications, websites, dan workflows
          </p>
          <Badge variant="secondary" size="md" className="bg-yellow-400 text-yellow-900">
            Free Tier Available
          </Badge>
        </div>
      </section>

      {/* Access Tiers */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              API Access <span className="text-gradient">Tiers</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700">Developer</Badge>
                  <div className="text-3xl font-bold text-blue-600">FREE</div>
                  <h3 className="font-semibold text-lg">Sandbox Access</h3>
                  <ul className="space-y-2 text-sm text-gray-600 text-left">
                    <li>• 100 API calls per month</li>
                    <li>• All widgets available</li>
                    <li>• Mock data responses</li>
                    <li>• Community support</li>
                    <li>• Rate limit: 10 req/min</li>
                  </ul>
                  <Button variant="outline" className="w-full" onClick={handleGetAccessClick}>
                    Get Free Access
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center border-2 border-primary">
                <div className="space-y-4">
                  <Badge variant="secondary" size="sm" className="bg-primary text-white">Production</Badge>
                  <div className="text-3xl font-bold text-primary">RM99</div>
                  <p className="text-sm text-gray-500">per month</p>
                  <h3 className="font-semibold text-lg">Business API</h3>
                  <ul className="space-y-2 text-sm text-gray-600 text-left">
                    <li>• 10,000 API calls per month</li>
                    <li>• Real AI processing</li>
                    <li>• Webhook support</li>
                    <li>• Email support</li>
                    <li>• Rate limit: 100 req/min</li>
                    <li>• Custom integrations</li>
                  </ul>
                  <Button variant="primary" className="w-full" onClick={handleGetAccessClick}>
                    Start Business Plan
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <Badge variant="outline" size="sm" className="border-purple-300 text-purple-700">Enterprise</Badge>
                  <div className="text-3xl font-bold text-purple-600">Custom</div>
                  <h3 className="font-semibold text-lg">Enterprise API</h3>
                  <ul className="space-y-2 text-sm text-gray-600 text-left">
                    <li>• Unlimited API calls</li>
                    <li>• Dedicated infrastructure</li>
                    <li>• Custom widgets</li>
                    <li>• Priority support</li>
                    <li>• SLA guarantees</li>
                    <li>• White-label options</li>
                  </ul>
                  <Button variant="outline" className="w-full" onClick={handleWhatsAppClick}>
                    Contact Sales
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              API <span className="text-gradient">Use Cases</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🌐 Website Integration</h3>
                  <p className="text-gray-600 text-sm mb-3">
                    Add AI-powered forms dan calculators directly to your website.
                  </p>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• Loan calculators for banks</li>
                    <li>• Quote generators for services</li>
                    <li>• Lead capture forms</li>
                    <li>• Content generation tools</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">💬 WhatsApp Bots</h3>
                  <p className="text-gray-600 text-sm mb-3">
                    Power your WhatsApp Business bots with intelligent responses.
                  </p>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• Automated customer service</li>
                    <li>• Product recommendations</li>
                    <li>• Appointment booking</li>
                    <li>• Order processing</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-purple-900">📱 Mobile Apps</h3>
                  <p className="text-gray-600 text-sm mb-3">
                    Integrate AI features into your mobile applications.
                  </p>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• In-app calculators</li>
                    <li>• Smart form validation</li>
                    <li>• Content suggestions</li>
                    <li>• Automated workflows</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-orange-900">🔗 System Integration</h3>
                  <p className="text-gray-600 text-sm mb-3">
                    Connect KuasaTurbo with your existing business systems.
                  </p>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• CRM automation</li>
                    <li>• ERP integrations</li>
                    <li>• Marketing platforms</li>
                    <li>• Custom dashboards</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* API Features */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              API <span className="text-gradient">Features</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🚀 Easy Integration</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>RESTful API with JSON responses</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Simple Bearer token authentication</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Comprehensive documentation</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>SDKs for popular languages</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">⚡ High Performance</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Average response time < 2 seconds</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>99.9% uptime SLA</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Global CDN for fast access</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Automatic scaling</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Getting Started */}
      <section className="section-padding bg-secondary text-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Getting <span className="text-yellow-300">Started</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { step: '1', title: 'Sign Up', desc: 'Create your developer account' },
                { step: '2', title: 'Get API Key', desc: 'Generate your authentication token' },
                { step: '3', title: 'Make First Call', desc: 'Test with our playground' },
                { step: '4', title: 'Go Live', desc: 'Deploy to production' },
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

      {/* Support */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Developer <span className="text-gradient">Support</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">📚</div>
                  <h3 className="font-semibold text-lg">Documentation</h3>
                  <p className="text-gray-600 text-sm">
                    Complete API reference with examples dan tutorials
                  </p>
                  <Button variant="outline" size="sm">
                    View Docs
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">💬</div>
                  <h3 className="font-semibold text-lg">Community</h3>
                  <p className="text-gray-600 text-sm">
                    Join our Discord for discussions dan support
                  </p>
                  <Button variant="outline" size="sm">
                    Join Discord
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🎯</div>
                  <h3 className="font-semibold text-lg">Playground</h3>
                  <p className="text-gray-600 text-sm">
                    Test API calls interactively before coding
                  </p>
                  <Button variant="outline" size="sm">
                    Try Playground
                  </Button>
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
            Ready to <span className="text-yellow-300">Integrate</span>?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Get your API key today dan start building AI-powered features into your applications.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              size="lg"
              onClick={handleGetAccessClick}
            >
              Get API Access
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleWhatsAppClick}
            >
              <a href="https://wa.me/60123456789" target="_blank" rel="noopener noreferrer">
                Contact Sales
              </a>
            </Button>
          </div>
          
          <p className="text-sm text-orange-200 mt-6">
            API support: api@kuasaturbo.com | Documentation: docs.kuasaturbo.com
          </p>
        </div>
      </section>

      {/* API Access Form Modal */}
      <ApiAccessForm 
        isOpen={showForm} 
        onClose={() => setShowForm(false)} 
      />
    </div>
  );
}