"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { trackConversionClick } from '@/lib/track';

export default function DocsPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'docs' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handleGetStartedClick = () => {
    trackConversionClick('docs_page', 'get_started');
  };

  const handleApiDocsClick = () => {
    trackConversionClick('docs_page', 'api_docs');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Developer <span className="text-yellow-300">Documentation</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Everything you need to integrate KuasaTurbo into your applications dan workflows
          </p>
          <Badge variant="secondary" size="md" className="bg-yellow-400 text-yellow-900">
            API v1.0 Available
          </Badge>
        </div>
      </section>

      {/* Quick Start */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Quick <span className="text-gradient">Start</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🔑</div>
                  <h3 className="font-semibold text-lg">Get API Key</h3>
                  <p className="text-gray-600 text-sm">
                    Sign up dan get your API key from the dashboard
                  </p>
                  <Button variant="outline" size="sm">
                    <Link href="/api-access">Get API Key</Link>
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">📖</div>
                  <h3 className="font-semibold text-lg">Read Docs</h3>
                  <p className="text-gray-600 text-sm">
                    Explore our comprehensive API documentation
                  </p>
                  <Button variant="outline" size="sm">
                    View API Docs
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🚀</div>
                  <h3 className="font-semibold text-lg">Start Building</h3>
                  <p className="text-gray-600 text-sm">
                    Make your first API call dan integrate widgets
                  </p>
                  <Button variant="outline" size="sm">
                    <Link href="/playground">Try Playground</Link>
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* API Overview */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              API <span className="text-gradient">Overview</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🔗 REST API</h3>
                  <p className="text-gray-600 text-sm mb-4">
                    Simple HTTP-based API for executing widgets dan retrieving results.
                  </p>
                  <div className="bg-gray-100 rounded-lg p-3 text-xs font-mono">
                    <div className="text-green-600">POST</div>
                    <div className="text-gray-800">https://api.kuasaturbo.com/v1/engine/execute</div>
                  </div>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• JSON request/response format</li>
                    <li>• Bearer token authentication</li>
                    <li>• Rate limiting: 1000 req/hour</li>
                    <li>• Webhook support for async operations</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">⚡ Widgets</h3>
                  <p className="text-gray-600 text-sm mb-4">
                    Pre-built AI workflows for common business operations.
                  </p>
                  <div className="space-y-2">
                    <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700 mr-2">ops.invoice_gen</Badge>
                    <Badge variant="outline" size="sm" className="border-green-300 text-green-700 mr-2">sales.lead_intake</Badge>
                    <Badge variant="outline" size="sm" className="border-purple-300 text-purple-700 mr-2">creative.caption_builder</Badge>
                  </div>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• 9 widgets across 3 categories</li>
                    <li>• Dynamic form validation</li>
                    <li>• Customizable output formats</li>
                    <li>• Multi-language support</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Code Examples */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Code <span className="text-gradient">Examples</span>
            </h2>
            
            <div className="space-y-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">JavaScript / Node.js</h3>
                  <div className="bg-gray-900 text-green-400 rounded-lg p-4 text-sm font-mono overflow-x-auto">
                    <pre>{`const response = await fetch('https://api.kuasaturbo.com/v1/engine/execute', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    widget_id: 'ops.invoice_gen',
    payload: {
      customer_name: 'ABC Sdn Bhd',
      items: [
        { description: 'Web Design', amount: 2500 }
      ]
    }
  })
});

const result = await response.json();
console.log(result.output);`}</pre>
                  </div>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Python</h3>
                  <div className="bg-gray-900 text-green-400 rounded-lg p-4 text-sm font-mono overflow-x-auto">
                    <pre>{`import requests

response = requests.post(
    'https://api.kuasaturbo.com/v1/engine/execute',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'widget_id': 'sales.lead_intake',
        'payload': {
            'name': 'John Tan',
            'phone': '012-345-6789',
            'interest': 'Honda Civic'
        }
    }
)

result = response.json()
print(result['output'])`}</pre>
                  </div>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">PHP</h3>
                  <div className="bg-gray-900 text-green-400 rounded-lg p-4 text-sm font-mono overflow-x-auto">
                    <pre>{`<?php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://api.kuasaturbo.com/v1/engine/execute');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Authorization: Bearer YOUR_API_KEY',
    'Content-Type: application/json'
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'widget_id' => 'creative.caption_builder',
    'payload' => [
        'topic' => 'New product launch',
        'platform' => 'Instagram',
        'tone' => 'exciting'
    ]
]));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$result = json_decode($response, true);
echo $result['output'];
?>`}</pre>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Documentation Sections */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Documentation <span className="text-gradient">Sections</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card variant="bordered" className="hover:shadow-lg transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">🚀</div>
                    <h3 className="font-semibold text-lg">Getting Started</h3>
                  </div>
                  <p className="text-gray-600 text-sm">
                    Authentication, first API call, dan basic concepts
                  </p>
                  <Button variant="outline" size="sm" className="w-full">
                    Read Guide
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="hover:shadow-lg transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">📚</div>
                    <h3 className="font-semibold text-lg">API Reference</h3>
                  </div>
                  <p className="text-gray-600 text-sm">
                    Complete endpoint documentation with examples
                  </p>
                  <Button variant="outline" size="sm" className="w-full">
                    View Reference
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="hover:shadow-lg transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">🧩</div>
                    <h3 className="font-semibold text-lg">Widget Catalog</h3>
                  </div>
                  <p className="text-gray-600 text-sm">
                    All available widgets with input/output schemas
                  </p>
                  <Button variant="outline" size="sm" className="w-full">
                    Browse Widgets
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="hover:shadow-lg transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">🔗</div>
                    <h3 className="font-semibold text-lg">Webhooks</h3>
                  </div>
                  <p className="text-gray-600 text-sm">
                    Async processing dan real-time notifications
                  </p>
                  <Button variant="outline" size="sm" className="w-full">
                    Setup Webhooks
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="hover:shadow-lg transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">🛠️</div>
                    <h3 className="font-semibold text-lg">SDKs & Libraries</h3>
                  </div>
                  <p className="text-gray-600 text-sm">
                    Official SDKs for popular programming languages
                  </p>
                  <Button variant="outline" size="sm" className="w-full">
                    Download SDKs
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="hover:shadow-lg transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">❓</div>
                    <h3 className="font-semibold text-lg">FAQ & Troubleshooting</h3>
                  </div>
                  <p className="text-gray-600 text-sm">
                    Common questions dan solutions to integration issues
                  </p>
                  <Button variant="outline" size="sm" className="w-full">
                    Get Help
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Support */}
      <section className="section-padding bg-secondary text-white">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6">
              Developer <span className="text-yellow-300">Support</span>
            </h2>
            <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
              Get help from our developer community dan support team.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <div className="text-4xl">💬</div>
                  <h3 className="font-semibold">Discord Community</h3>
                  <p className="text-sm text-gray-600">
                    Join our developer community for discussions dan support
                  </p>
                  <Button variant="outline" size="sm">
                    Join Discord
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <div className="text-4xl">📧</div>
                  <h3 className="font-semibold">Email Support</h3>
                  <p className="text-sm text-gray-600">
                    Technical support for integration questions
                  </p>
                  <Button variant="outline" size="sm">
                    Contact Support
                  </Button>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <div className="text-4xl">📞</div>
                  <h3 className="font-semibold">Priority Support</h3>
                  <p className="text-sm text-gray-600">
                    Phone support for enterprise customers
                  </p>
                  <Button variant="outline" size="sm">
                    Upgrade Plan
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
            Ready to <span className="text-yellow-300">Build</span>?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Get your API key dan start integrating KuasaTurbo into your applications today.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              size="lg"
              onClick={handleGetStartedClick}
            >
              <Link href="/api-access">Get Started</Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleApiDocsClick}
            >
              View API Docs
            </Button>
          </div>
          
          <p className="text-sm text-orange-200 mt-6">
            Developer support: developers@kuasaturbo.com
          </p>
        </div>
      </section>
    </div>
  );
}