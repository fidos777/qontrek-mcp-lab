"use client";

import Link from 'next/link';
import { useState, useEffect } from 'react';
import Button from '@/components/shared/Button';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`bg-white border-b border-gray-200 sticky top-0 z-40 transition-all duration-200 ${
      isScrolled ? 'backdrop-blur-md bg-white/95 shadow-sm' : ''
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KT</span>
            </div>
            <span className="font-bold text-xl text-secondary">KuasaTurbo</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/playground" className="text-gray-700 hover:text-primary transition-colors">
              Playground
            </Link>
            <Link href="/verticals" className="text-gray-700 hover:text-primary transition-colors">
              Verticals
            </Link>
            <Link href="/pricing" className="text-gray-700 hover:text-primary transition-colors">
              Pricing
            </Link>
            <Link href="/docs" className="text-gray-700 hover:text-primary transition-colors">
              Docs
            </Link>
            <Link href="/partners" className="text-gray-700 hover:text-primary transition-colors">
              Partners
            </Link>
            <Button variant="primary" size="sm">
              <Link href="/api-access">Get API Access</Link>
            </Button>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-md text-gray-700 hover:text-primary"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200 animate-fadeInUp">
            <div className="flex flex-col space-y-4">
              <Link href="/playground" className="text-gray-700 hover:text-primary transition-colors">
                Playground
              </Link>
              <Link href="/verticals" className="text-gray-700 hover:text-primary transition-colors">
                Verticals
              </Link>
              <Link href="/pricing" className="text-gray-700 hover:text-primary transition-colors">
                Pricing
              </Link>
              <Link href="/docs" className="text-gray-700 hover:text-primary transition-colors">
                Docs
              </Link>
              <Link href="/partners" className="text-gray-700 hover:text-primary transition-colors">
                Partners
              </Link>
              <Button variant="primary" size="sm" className="w-fit">
                <Link href="/api-access">Get API Access</Link>
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}