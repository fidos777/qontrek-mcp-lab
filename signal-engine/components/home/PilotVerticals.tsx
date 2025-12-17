"use client";

import Link from 'next/link';
import Card from '@/components/shared/Card';
import Badge from '@/components/shared/Badge';
import { VERTICALS } from '@/lib/constants';

export default function PilotVerticals() {
  return (
    <section className="section-padding bg-gray-50">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Industry <span className="text-gradient">Verticals</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Specialized widgets untuk different industries, dengan more coming soon
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {VERTICALS.map((vertical) => (
            <Card key={vertical.slug} variant="bordered" className="hover:shadow-lg transition-shadow">
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="text-3xl">{vertical.icon}</div>
                  <Badge 
                    variant={
                      vertical.status === 'available' ? 'success' :
                      vertical.status === 'pilot' ? 'warning' : 'default'
                    }
                    size="sm"
                  >
                    {vertical.status === 'available' ? 'Available' :
                     vertical.status === 'pilot' ? 'Pilot' : 'Coming Soon'}
                  </Badge>
                </div>
                
                <div>
                  <h3 className="font-semibold text-lg mb-2">{vertical.name}</h3>
                  <p className="text-gray-600 text-sm">{vertical.description}</p>
                </div>
                
                {vertical.status === 'available' && (
                  <div className="pt-2">
                    <Link 
                      href={`/verticals/${vertical.slug}`}
                      className="text-primary hover:text-primary/80 text-sm font-medium"
                    >
                      Explore widgets →
                    </Link>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12">
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 max-w-2xl mx-auto">
            <h3 className="font-semibold text-green-900 mb-2">🌱 Growing Ecosystem</h3>
            <p className="text-green-800 text-sm">
              We're constantly adding new verticals based on user feedback. 
              <Link href="/api-access" className="font-medium underline ml-1">
                Request your industry
              </Link>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}