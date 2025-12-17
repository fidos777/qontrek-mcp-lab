"use client";

import Link from 'next/link';
import Button from '@/components/shared/Button';
import { trackConversionClick } from '@/lib/track';

export default function FinalCTA() {
  const handlePlaygroundClick = () => {
    trackConversionClick('final_cta', 'playground');
  };

  const handleAPIClick = () => {
    trackConversionClick('final_cta', 'api_access');
  };

  return (
    <section className="gradient-bg text-white section-padding">
      <div className="container">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Ready to Automate
            <br />
            <span className="text-yellow-300">Your Business?</span>
          </h2>
          <p className="text-xl md:text-2xl mb-8 text-orange-100">
            Start dengan free playground atau get API access untuk production use
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button 
              variant="secondary" 
              size="lg"
              onClick={handlePlaygroundClick}
            >
              <Link href="/playground" className="flex items-center space-x-2">
                <span>🎮</span>
                <span>Start Free in Playground</span>
              </Link>
            </Button>
            <Button 
              variant="outline" 
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleAPIClick}
            >
              <Link href="/api-access" className="flex items-center space-x-2">
                <span>🚀</span>
                <span>Get Production Access</span>
              </Link>
            </Button>
          </div>

          <div className="text-center">
            <p className="text-orange-200 text-sm mb-4">
              Questions? Need help getting started?
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center text-sm">
              <Link href="/docs" className="text-yellow-300 hover:text-yellow-100 transition-colors">
                📚 Documentation
              </Link>
              <Link href="/api-access" className="text-yellow-300 hover:text-yellow-100 transition-colors">
                💬 Contact Support
              </Link>
              <Link href="/partners" className="text-yellow-300 hover:text-yellow-100 transition-colors">
                🤝 Partner with Us
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}