"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import { trackConversionClick } from '@/lib/track';

export default function ConsultantPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'consultant' } }
    });
    window.dispatchEvent(event);
  }, []);

  const handleApplyClick = () => {
    trackConversionClick('consultant_page', 'apply');
  };

  const handleWhatsAppClick = () => {
    trackConversionClick('consultant_page', 'whatsapp');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Become a KuasaTurbo <span className="text-yellow-300">Consultant</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Help SMEs implement AI workflows dan earn revenue sharing dari successful implementations
          </p>
          <Badge variant="secondary" size="md" className="bg-yellow-400 text-yellow-900">
            Now Accepting Applications
          </Badge>
        </div>
      </section>

      {/* Program Overview */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Why Join Our <span className="text-gradient">Consultant Network</span>?
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">💰</div>
                  <h3 className="font-semibold text-lg">Revenue Sharing</h3>
                  <p className="text-gray-600 text-sm">
                    Earn 20-30% commission on client implementations dan ongoing usage
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🎓</div>
                  <h3 className="font-semibold text-lg">Training Provided</h3>
                  <p className="text-gray-600 text-sm">
                    Comprehensive training on KuasaTurbo platform dan implementation best practices
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🤝</div>
                  <h3 className="font-semibold text-lg">Client Referrals</h3>
                  <p className="text-gray-600 text-sm">
                    Access to our lead pipeline dan marketing qualified prospects
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* What You'll Do */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              What <span className="text-gradient">Consultants</span> Do
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">Client Assessment</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Analyze client business processes</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Identify automation opportunities</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Recommend suitable widgets</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Calculate ROI projections</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">Implementation</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Set up KuasaTurbo workflows</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Train client teams</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Customize widgets for specific needs</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Provide ongoing support</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Requirements */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Consultant <span className="text-gradient">Requirements</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">✅ Must Have</h3>
                  <ul className="space-y-2 text-sm text-green-800">
                    <li>• 2+ years business consulting experience</li>
                    <li>• Understanding of SME operations</li>
                    <li>• Basic technical knowledge</li>
                    <li>• Strong communication skills</li>
                    <li>• Fluent in BM/EN</li>
                    <li>• Based in Malaysia</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">⭐ Nice to Have</h3>
                  <ul className="space-y-2 text-sm text-blue-800">
                    <li>• AI/automation experience</li>
                    <li>• Existing SME client network</li>
                    <li>• Industry specialization</li>
                    <li>• Project management certification</li>
                    <li>• Sales/business development background</li>
                    <li>• Technical implementation experience</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Earning Potential */}
      <section className="section-padding bg-secondary text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">
            Earning <span className="text-yellow-300">Potential</span>
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Our top consultants earn RM5,000-15,000 per month dari implementations dan ongoing commissions
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-300 mb-2">20-30%</div>
              <h3 className="font-semibold mb-1">Commission Rate</h3>
              <p className="text-sm text-gray-300">On all client implementations</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-300 mb-2">RM2-10k</div>
              <h3 className="font-semibold mb-1">Per Implementation</h3>
              <p className="text-sm text-gray-300">Depending on client size</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-300 mb-2">Recurring</div>
              <h3 className="font-semibold mb-1">Ongoing Revenue</h3>
              <p className="text-sm text-gray-300">From client usage</p>
            </div>
          </div>
        </div>
      </section>

      {/* Application Process */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Application <span className="text-gradient">Process</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { step: '1', title: 'Apply', desc: 'Submit application form' },
                { step: '2', title: 'Interview', desc: 'Video call assessment' },
                { step: '3', title: 'Training', desc: '2-week certification program' },
                { step: '4', title: 'Launch', desc: 'Start consulting with support' },
              ].map((item, index) => (
                <Card key={index} variant="bordered" className="text-center">
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
            Ready to Join Our <span className="text-yellow-300">Team</span>?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Applications are reviewed weekly. Early applicants get priority access to training dan client referrals.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              size="lg"
              onClick={handleApplyClick}
            >
              <Link href="/api-access">Apply Now</Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-white hover:text-primary"
              onClick={handleWhatsAppClick}
            >
              <a href="https://wa.me/60123456789" target="_blank" rel="noopener noreferrer">
                WhatsApp Us
              </a>
            </Button>
          </div>
          
          <p className="text-sm text-orange-200 mt-6">
            Questions? Contact our partner team at partners@kuasaturbo.com
          </p>
        </div>
      </section>
    </div>
  );
}