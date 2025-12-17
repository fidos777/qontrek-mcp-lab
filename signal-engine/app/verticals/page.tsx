"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { VERTICALS } from '@/lib/constants';
import { trackConversionClick } from '@/lib/track';

export default function VerticalsPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'verticals' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handlePlaygroundClick = () => {
    trackConversionClick('verticals_page', 'playground');
  };

  const handleRequestClick = () => {
    trackConversionClick('verticals_page', 'request_vertical');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Industry <span className="text-yellow-300">Verticals</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Specialized AI workers untuk different industries, dengan more verticals coming soon
          </p>
        </div>
      </section>

      {/* Available Verticals */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">
              Available <span className="text-gradient">Now</span>
            </h2>
            <p className="text-xl text-gray-600">
              Ready-to-use widgets untuk these industries
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {VERTICALS.filter(v => v.status === 'available').map((vertical) => (
              <Card key={vertical.slug} variant="elevated" className="hover:shadow-xl transition-shadow">
                <div className="space-y-6">
                  <div className="flex items-start justify-between">
                    <div className="text-5xl">{vertical.icon}</div>
                    <Badge variant="success" size="sm">Available</Badge>
                  </div>
                  
                  <div>
                    <h3 className="font-bold text-2xl mb-3">{vertical.name}</h3>
                    <p className="text-gray-600 mb-4">{vertical.description}</p>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="text-sm font-medium text-gray-700">Available Widgets:</div>
                    <div className="space-y-2 text-sm text-gray-600">
                      {vertical.slug === 'automotive' && (
                        <>
                          <div className="flex items-center space-x-2">
                            <span className="text-green-500">✓</span>
                            <span>Lead qualification dan intake</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-green-500">✓</span>
                            <span>Follow-up scheduling</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-green-500">✓</span>
                            <span>Proposal generation</span>
                          </div>
                        </>
                      )}
                      {vertical.slug === 'fnb' && (
                        <>
                          <div className="flex items-center space-x-2">
                            <span className="text-green-500">✓</span>
                            <span>Invoice generation</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-green-500">✓</span>
                            <span>Social media captions</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-green-500">✓</span>
                            <span>Attendance tracking</span>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                  
                  <Button variant="primary" className="w-full">
                    <Link href={`/playground?tab=ops`}>Try {vertical.name} Widgets</Link>
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pilot Verticals */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">
              Pilot <span className="text-gradient">Program</span>
            </h2>
            <p className="text-xl text-gray-600">
              Early access untuk selected partners
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {VERTICALS.filter(v => v.status === 'pilot').map((vertical) => (
              <Card key={vertical.slug} variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">{vertical.icon}</div>
                  <Badge variant="warning" size="sm">Pilot Program</Badge>
                  <h3 className="font-semibold text-lg">{vertical.name}</h3>
                  <p className="text-gray-600 text-sm">{vertical.description}</p>
                  <Button variant="outline" size="sm" className="w-full">
                    Join Pilot Program
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Coming Soon */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">
              Coming <span className="text-gradient">Soon</span>
            </h2>
            <p className="text-xl text-gray-600">
              In development based on user feedback
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {VERTICALS.filter(v => v.status === 'coming_soon').map((vertical) => (
              <Card key={vertical.slug} variant="bordered" className="text-center opacity-75">
                <div className="space-y-4">
                  <div className="text-4xl">{vertical.icon}</div>
                  <Badge variant="default" size="sm">Coming Soon</Badge>
                  <h3 className="font-semibold text-lg">{vertical.name}</h3>
                  <p className="text-gray-600 text-sm">{vertical.description}</p>
                  <div className="text-xs text-gray-500">
                    Expected: Q2 2025
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Request New Vertical */}
      <section className="section-padding bg-secondary text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">
            Don't See Your <span className="text-yellow-300">Industry</span>?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            We're constantly expanding based on user needs. Request your industry dan we'll prioritize it.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="text-3xl mb-2">🎯</div>
              <h3 className="font-semibold mb-1">Custom Widgets</h3>
              <p className="text-sm text-gray-300">Tailored untuk your industry needs</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">⚡</div>
              <h3 className="font-semibold mb-1">Fast Development</h3>
              <p className="text-sm text-gray-300">Priority development untuk requested verticals</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">🤝</div>
              <h3 className="font-semibold mb-1">Partnership</h3>
              <p className="text-sm text-gray-300">Collaborate on widget design</p>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              size="lg"
              onClick={handleRequestClick}
            >
              <Link href="/api-access">Request New Vertical</Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-white hover:text-secondary"
              onClick={handlePlaygroundClick}
            >
              <Link href="/playground">Try Existing Widgets</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">
              Success <span className="text-gradient">Stories</span>
            </h2>
            <p className="text-xl text-gray-600">
              How businesses are using KuasaTurbo across industries
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Card variant="bordered" className="bg-blue-50 border-blue-200">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">🚗</div>
                  <div>
                    <h3 className="font-semibold">Automotive Dealer</h3>
                    <div className="text-sm text-gray-600">Kuala Lumpur</div>
                  </div>
                </div>
                <p className="text-gray-700 text-sm">
                  "KuasaTurbo's lead qualification widget helped us process 40% more inquiries 
                  dengan the same team. Follow-up scheduling is now automated."
                </p>
                <div className="text-xs text-blue-600 font-medium">
                  Saved 15 hours/week on admin tasks
                </div>
              </div>
            </Card>

            <Card variant="bordered" className="bg-green-50 border-green-200">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">🍽️</div>
                  <div>
                    <h3 className="font-semibold">Restaurant Chain</h3>
                    <div className="text-sm text-gray-600">Selangor</div>
                  </div>
                </div>
                <p className="text-gray-700 text-sm">
                  "Invoice generation dan social media captions are now automated. 
                  Our staff can focus on customer service instead of paperwork."
                </p>
                <div className="text-xs text-green-600 font-medium">
                  Reduced admin costs by 60%
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
}