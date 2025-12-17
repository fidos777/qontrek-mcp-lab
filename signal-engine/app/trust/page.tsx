"use client";

import { useEffect } from 'react';
import Card from '@/components/shared/Card';
import Badge from '@/components/shared/Badge';

export default function TrustPage() {
  useEffect(() => {
    // Track page view
    const event = new CustomEvent('track', {
      detail: { event: 'tab_view', properties: { page: 'trust' } }
    });
    window.dispatchEvent(event);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white section-padding">
        <div className="container text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Trust & <span className="text-yellow-300">Security</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-orange-100 max-w-3xl mx-auto">
            Your data security dan privacy are our top priorities. Learn how we protect your business.
          </p>
          <Badge variant="secondary" size="md" className="bg-yellow-400 text-yellow-900">
            SOC 2 Compliant
          </Badge>
        </div>
      </section>

      {/* Security Overview */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Enterprise-Grade <span className="text-gradient">Security</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🔒</div>
                  <h3 className="font-semibold text-lg">Data Encryption</h3>
                  <p className="text-gray-600 text-sm">
                    End-to-end encryption for all data in transit dan at rest using AES-256
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🛡️</div>
                  <h3 className="font-semibold text-lg">Access Control</h3>
                  <p className="text-gray-600 text-sm">
                    Multi-factor authentication dan role-based access controls
                  </p>
                </div>
              </Card>
              
              <Card variant="bordered" className="text-center">
                <div className="space-y-4">
                  <div className="text-4xl">🏢</div>
                  <h3 className="font-semibold text-lg">Compliance</h3>
                  <p className="text-gray-600 text-sm">
                    SOC 2 Type II, GDPR, dan PDPA compliant infrastructure
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Data Protection */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Data <span className="text-gradient">Protection</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🔐 Data Security</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>AES-256 encryption for all stored data</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>TLS 1.3 for all data transmission</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Regular security audits dan penetration testing</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>Zero-knowledge architecture where possible</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">🌍 Data Residency</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Data stored in Malaysia dan Singapore only</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>No data transfer to third countries</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>PDPA compliant data handling</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>Right to data portability dan deletion</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Privacy Commitments */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Privacy <span className="text-gradient">Commitments</span>
            </h2>
            
            <div className="space-y-6">
              <Card variant="bordered" className="bg-blue-50 border-blue-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-blue-900">🚫 What We DON'T Do</h3>
                  <ul className="space-y-2 text-sm text-blue-800">
                    <li>• We don't sell your data to third parties</li>
                    <li>• We don't use your data to train AI models for other customers</li>
                    <li>• We don't share your business information with competitors</li>
                    <li>• We don't store unnecessary personal information</li>
                    <li>• We don't track you outside our platform</li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-green-50 border-green-200">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-green-900">✅ What We DO</h3>
                  <ul className="space-y-2 text-sm text-green-800">
                    <li>• We use your data only to provide our services</li>
                    <li>• We give you full control over your data</li>
                    <li>• We provide transparent privacy policies</li>
                    <li>• We respond to data requests within 30 days</li>
                    <li>• We notify you of any security incidents immediately</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="section-padding bg-secondary text-white">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6">
              Security <span className="text-yellow-300">Certifications</span>
            </h2>
            <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
              We maintain the highest security standards through regular audits dan certifications.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <div className="text-4xl">🏆</div>
                  <h3 className="font-semibold">SOC 2 Type II</h3>
                  <p className="text-sm text-gray-600">
                    Audited security controls for availability, confidentiality, dan privacy
                  </p>
                  <Badge variant="outline" size="sm" className="border-green-300 text-green-700">Certified</Badge>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <div className="text-4xl">🌍</div>
                  <h3 className="font-semibold">GDPR Compliant</h3>
                  <p className="text-sm text-gray-600">
                    Full compliance with European data protection regulations
                  </p>
                  <Badge variant="outline" size="sm" className="border-blue-300 text-blue-700">Compliant</Badge>
                </div>
              </Card>
              
              <Card variant="bordered" className="bg-white text-gray-900">
                <div className="text-center space-y-4">
                  <div className="text-4xl">🇲🇾</div>
                  <h3 className="font-semibold">PDPA Compliant</h3>
                  <p className="text-sm text-gray-600">
                    Adherence to Malaysia's Personal Data Protection Act
                  </p>
                  <Badge variant="outline" size="sm" className="border-purple-300 text-purple-700">Compliant</Badge>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Infrastructure */}
      <section className="section-padding bg-gray-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Secure <span className="text-gradient">Infrastructure</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-purple-900">☁️ Cloud Security</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-purple-500 mt-0.5">•</span>
                      <span>AWS dan Google Cloud infrastructure</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-purple-500 mt-0.5">•</span>
                      <span>Multi-region backup dan disaster recovery</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-purple-500 mt-0.5">•</span>
                      <span>99.9% uptime SLA with monitoring</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-purple-500 mt-0.5">•</span>
                      <span>Automated security patching</span>
                    </li>
                  </ul>
                </div>
              </Card>
              
              <Card variant="bordered">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg text-orange-900">🔍 Monitoring</h3>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start space-x-2">
                      <span className="text-orange-500 mt-0.5">•</span>
                      <span>24/7 security monitoring dan alerting</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-orange-500 mt-0.5">•</span>
                      <span>Intrusion detection dan prevention</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-orange-500 mt-0.5">•</span>
                      <span>Comprehensive audit logging</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-orange-500 mt-0.5">•</span>
                      <span>Real-time threat intelligence</span>
                    </li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Incident Response */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Incident <span className="text-gradient">Response</span>
            </h2>
            
            <Card variant="bordered" className="bg-red-50 border-red-200">
              <div className="space-y-6">
                <h3 className="font-semibold text-lg text-red-900 text-center">
                  🚨 Security Incident Protocol
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="w-12 h-12 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-2">
                      1
                    </div>
                    <h4 className="font-medium text-red-900 mb-1">Detection</h4>
                    <p className="text-xs text-red-800">Automated systems detect potential threats</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-2">
                      2
                    </div>
                    <h4 className="font-medium text-red-900 mb-1">Response</h4>
                    <p className="text-xs text-red-800">Security team responds within 15 minutes</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-2">
                      3
                    </div>
                    <h4 className="font-medium text-red-900 mb-1">Containment</h4>
                    <p className="text-xs text-red-800">Isolate dan contain the incident</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-2">
                      4
                    </div>
                    <h4 className="font-medium text-red-900 mb-1">Notification</h4>
                    <p className="text-xs text-red-800">Notify affected customers within 24 hours</p>
                  </div>
                </div>
                
                <div className="bg-red-100 border border-red-300 rounded-lg p-4">
                  <p className="text-sm text-red-800 text-center">
                    <strong>Emergency Contact:</strong> security@kuasaturbo.com | +60-3-XXXX-XXXX
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Contact Security Team */}
      <section className="section-padding bg-primary text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">
            Security <span className="text-yellow-300">Questions</span>?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Our security team is available to answer any questions about our data protection practices.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="text-2xl mb-2">📧</div>
              <h3 className="font-semibold mb-1">Email</h3>
              <p className="text-sm text-orange-200">security@kuasaturbo.com</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">📋</div>
              <h3 className="font-semibold mb-1">Security Questionnaire</h3>
              <p className="text-sm text-orange-200">Available upon request</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">🔍</div>
              <h3 className="font-semibold mb-1">Penetration Testing</h3>
              <p className="text-sm text-orange-200">Reports available for enterprise clients</p>
            </div>
          </div>
          
          <p className="text-sm text-orange-200">
            Last updated: December 2024 | Next audit: March 2025
          </p>
        </div>
      </section>
    </div>
  );
}