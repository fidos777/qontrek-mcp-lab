"use client";

import Link from 'next/link';
import Button from '@/components/shared/Button';
import { trackConversionClick } from '@/lib/track';

export default function HeroChooser() {
  const handlePlaygroundClick = () => {
    trackConversionClick('hero', 'playground');
  };

  const handleAPIClick = () => {
    trackConversionClick('hero', 'api_access');
  };

  return (
    <section className="gradient-bg text-white section-padding relative overflow-hidden">
      <div className="container">
        <div className="max-w-4xl mx-auto text-center animate-fadeInUp">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            AI Workers untuk
            <br />
            <span className="text-yellow-300">SME Operations</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100">
            Generate content, automate tasks, dan scale your business dengan lightweight AI engine yang mudah digunakan.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button 
              variant="secondary" 
              size="lg"
              onClick={handlePlaygroundClick}
            >
              <Link href="/playground" className="flex items-center space-x-2">
                <span>🎮</span>
                <span>Try Playground</span>
              </Link>
            </Button>
            <Button 
              variant="outline" 
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleAPIClick}
            >
              <Link href="/api-access" className="flex items-center space-x-2">
                <span>🔌</span>
                <span>Get API Access</span>
              </Link>
            </Button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-yellow-300">9+</div>
              <div className="text-orange-100">Ready-to-use widgets</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-300">3</div>
              <div className="text-orange-100">Work categories</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-300">Draft</div>
              <div className="text-orange-100">Mode only (for now)</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}