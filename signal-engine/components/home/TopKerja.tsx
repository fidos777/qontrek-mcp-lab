"use client";

import Card from '@/components/shared/Card';
import Badge from '@/components/shared/Badge';
import { WIDGETS } from '@/lib/widgets';
import { WORK_CATEGORIES } from '@/lib/constants';

export default function TopKerja() {
  // Get top widgets from each category
  const topWidgets = [
    WIDGETS.find(w => w.id === 'ops.invoice_generator'),
    WIDGETS.find(w => w.id === 'sales.lead_qualifier'),
    WIDGETS.find(w => w.id === 'creative.social_caption'),
    WIDGETS.find(w => w.id === 'ops.attendance_tracker'),
  ].filter(Boolean);

  return (
    <section className="section-padding bg-white">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Top <span className="text-gradient">Kerja</span> untuk SME
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Most popular AI workers yang membantu business operations setiap hari
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {topWidgets.map((widget) => (
            <Card key={widget!.id} variant="bordered" className="hover:shadow-lg transition-shadow">
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg mb-2">{widget!.name}</h3>
                    <p className="text-gray-600 text-sm mb-3">{widget!.description}</p>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <Badge variant="primary" size="sm">
                    {WORK_CATEGORIES[widget!.category]}
                  </Badge>
                  <div className="text-sm text-gray-500">
                    {widget!.estimatedCredits} credits
                  </div>
                </div>
                
                <div className="text-xs text-gray-400">
                  {widget!.fields.length} fields • Draft mode
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center mt-8">
          <p className="text-gray-600 mb-4">
            Want to see all available widgets?
          </p>
          <a 
            href="/playground" 
            className="text-primary hover:text-primary/80 font-medium"
          >
            Explore Playground →
          </a>
        </div>
      </div>
    </section>
  );
}