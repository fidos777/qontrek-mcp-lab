"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { trackConversionClick } from '@/lib/track';

export default function CreditsPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'credits' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handleBuyClick = () => {
    trackConversionClick('credits_page', 'pricing');
  };

  const handlePlaygroundClick = () => {
    trackConversionClick('credits_page', 'playground');
  };

  // Mock data - in real app this would come from API
  const mockUsage = [
    { date: '2024-12-13', widget: 'Invoice Generator', credits: 3, status: 'success' },
    { date: '2024-12-12', widget: 'Social Caption', credits: 2, status: 'success' },
    { date: '2024-12-12', widget: 'Lead Qualifier', credits: 3, status: 'success' },
    { date: '2024-12-11', widget: 'Attendance Tracker', credits: 1, status: 'success' },
    { date: '2024-12-10', widget: 'Proposal Generator', credits: 5, status: 'success' },
  ];

  const totalUsed = mockUsage.reduce((sum, item) => sum + item.credits, 0);
  const currentBalance = 150 - totalUsed;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Credit <span className="text-yellow-300">Management</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Track your usage, manage your balance, dan optimize your AI spending
          </p>
        </div>
      </section>

      <div className="container section-padding">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Current Balance */}
            <Card variant="elevated" className="bg-gradient-to-r from-blue-50 to-purple-50">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Current Balance</h2>
                  <div className="text-4xl font-bold text-primary">{currentBalance} credits</div>
                  <p className="text-gray-600 mt-2">Ready untuk your next AI generations</p>
                </div>
                <div className="text-6xl opacity-20">💳</div>
              </div>
            </Card>

            {/* Usage Statistics */}
            <Card variant="bordered">
              <div className="space-y-6">
                <h3 className="text-xl font-semibold">Usage This Month</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">{totalUsed}</div>
                    <div className="text-sm text-gray-600">Credits Used</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">{mockUsage.length}</div>
                    <div className="text-sm text-gray-600">Generations</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600">
                      {Math.round(totalUsed / mockUsage.length * 10) / 10}
                    </div>
                    <div className="text-sm text-gray-600">Avg per Task</div>
                  </div>
                </div>
              </div>
            </Card>

            {/* Recent Usage */}
            <Card variant="bordered">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold">Recent Usage</h3>
                  <Badge variant="default" size="sm">Last 7 days</Badge>
                </div>
                
                <div className="space-y-3">
                  {mockUsage.map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <div>
                          <div className="font-medium text-gray-900">{item.widget}</div>
                          <div className="text-sm text-gray-500">{item.date}</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="success" size="sm">{item.status}</Badge>
                        <div className="font-medium text-gray-900">{item.credits} credits</div>
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="text-center">
                  <Button variant="outline" size="sm">
                    View Full History
                  </Button>
                </div>
              </div>
            </Card>

            {/* Usage Insights */}
            <Card variant="bordered" className="bg-blue-50 border-blue-200">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-blue-900">💡 Usage Insights</h3>
                
                <div className="space-y-3 text-sm text-blue-800">
                  <div className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>You're using an average of {Math.round(totalUsed / 7)} credits per day</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>Most used widget: Invoice Generator (3 credits each)</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>At current usage, your credits will last ~{Math.round(currentBalance / (totalUsed / 7))} days</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card variant="bordered">
              <div className="space-y-4">
                <h3 className="font-semibold">Quick Actions</h3>
                
                <div className="space-y-3">
                  <Button
                    variant="primary"
                    className="w-full"
                    onClick={handleBuyClick}
                  >
                    <Link href="/pricing">Buy More Credits</Link>
                  </Button>
                  
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={handlePlaygroundClick}
                  >
                    <Link href="/playground">Use Playground</Link>
                  </Button>
                  
                  <Button variant="ghost" className="w-full">
                    Download Usage Report
                  </Button>
                </div>
              </div>
            </Card>

            {/* Credit Recommendations */}
            <Card variant="bordered" className="bg-green-50 border-green-200">
              <div className="space-y-4">
                <h3 className="font-semibold text-green-900">💰 Smart Recommendations</h3>
                
                <div className="space-y-3 text-sm text-green-800">
                  <div>
                    <strong>Based on your usage:</strong>
                  </div>
                  <div className="bg-green-100 p-3 rounded">
                    <div className="font-medium">Professional Pack (500 credits)</div>
                    <div className="text-xs text-green-700 mt-1">
                      Will last ~{Math.round(500 / (totalUsed / 7))} days at current usage
                    </div>
                  </div>
                  <div className="text-xs">
                    Save RM{((150/500) * 99 - (totalUsed * 0.29)).toFixed(2)} compared to buying smaller packs
                  </div>
                </div>
              </div>
            </Card>

            {/* Support */}
            <Card variant="bordered">
              <div className="space-y-4">
                <h3 className="font-semibold">Need Help?</h3>
                
                <div className="space-y-2 text-sm text-gray-600">
                  <div>
                    <Link href="/docs" className="text-primary hover:underline">
                      📚 View Documentation
                    </Link>
                  </div>
                  <div>
                    <Link href="/api-access" className="text-primary hover:underline">
                      💬 Contact Support
                    </Link>
                  </div>
                  <div>
                    <Link href="/pricing" className="text-primary hover:underline">
                      ❓ Pricing FAQ
                    </Link>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}