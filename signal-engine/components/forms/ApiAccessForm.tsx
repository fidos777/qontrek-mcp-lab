"use client";

import { useState } from 'react';
import Button from '@/components/shared/Button';
import Input from '@/components/shared/Input';
import Textarea from '@/components/shared/Textarea';
import Select from '@/components/shared/Select';
import Card from '@/components/shared/Card';
import { submitFeatureRequest } from '@/lib/api';
import { trackConversionClick, trackFeatureRequestSubmit } from '@/lib/track';

interface ApiAccessFormData {
  company_name: string;
  contact_name: string;
  email: string;
  phone: string;
  use_case: string;
  expected_volume: string;
  integration_timeline: string;
  additional_info: string;
}

export default function ApiAccessForm() {
  const [formData, setFormData] = useState<ApiAccessFormData>({
    company_name: '',
    contact_name: '',
    email: '',
    phone: '',
    use_case: '',
    expected_volume: '',
    integration_timeline: '',
    additional_info: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const volumeOptions = [
    { value: '< 1000', label: '< 1,000 requests/month' },
    { value: '1000-10000', label: '1,000 - 10,000 requests/month' },
    { value: '10000-100000', label: '10,000 - 100,000 requests/month' },
    { value: '> 100000', label: '> 100,000 requests/month' },
  ];

  const timelineOptions = [
    { value: 'immediate', label: 'Immediate (< 1 week)' },
    { value: '1-4 weeks', label: '1-4 weeks' },
    { value: '1-3 months', label: '1-3 months' },
    { value: '3+ months', label: '3+ months' },
  ];

  const handleInputChange = (field: keyof ApiAccessFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    const requiredFields = ['company_name', 'contact_name', 'email', 'use_case', 'expected_volume', 'integration_timeline'];
    const missingFields = requiredFields.filter(field => !formData[field as keyof ApiAccessFormData].trim());
    
    if (missingFields.length > 0) {
      setError('Please fill in all required fields');
      return;
    }

    // Email validation
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      setError('Please enter a valid email address');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // Track conversion
      trackConversionClick('api_access_form', 'submit');

      // Submit as feature request
      await submitFeatureRequest({
        title: `API Access Request - ${formData.company_name}`,
        description: `Company: ${formData.company_name}\nContact: ${formData.contact_name}\nEmail: ${formData.email}\nPhone: ${formData.phone}\n\nUse Case:\n${formData.use_case}\n\nExpected Volume: ${formData.expected_volume}\nTimeline: ${formData.integration_timeline}\n\nAdditional Info:\n${formData.additional_info}`,
        category: 'Integration',
        priority: 'high',
        contact_email: formData.email,
      });

      trackFeatureRequestSubmit('Integration', 'high');
      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit request');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <Card variant="elevated" className="max-w-2xl mx-auto">
        <div className="text-center space-y-6">
          <div className="text-6xl">🚀</div>
          <h3 className="text-2xl font-bold text-green-900">
            API Access Request Submitted!
          </h3>
          <p className="text-green-700 text-lg">
            Thank you for your interest in KuasaTurbo API. Our team will review your request dan contact you within 1-2 business days.
          </p>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h4 className="font-semibold text-green-900 mb-4">What happens next?</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-green-800">
              <div className="flex items-start space-x-2">
                <span className="text-green-600 mt-0.5">1.</span>
                <span>Technical review of your use case</span>
              </div>
              <div className="flex items-start space-x-2">
                <span className="text-green-600 mt-0.5">2.</span>
                <span>Custom pricing proposal</span>
              </div>
              <div className="flex items-start space-x-2">
                <span className="text-green-600 mt-0.5">3.</span>
                <span>API key generation</span>
              </div>
              <div className="flex items-start space-x-2">
                <span className="text-green-600 mt-0.5">4.</span>
                <span>Integration support</span>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button variant="primary" className="flex-1">
              <a href="/docs">View Documentation</a>
            </Button>
            <Button variant="outline" className="flex-1">
              <a href="/playground">Try Playground</a>
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card variant="elevated" className="max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            Request API Access
          </h3>
          <p className="text-gray-600">
            Get production access to KuasaTurbo's AI workers untuk your applications
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input
            label="Company Name"
            placeholder="ABC Sdn Bhd"
            value={formData.company_name}
            onChange={(e) => handleInputChange('company_name', e.target.value)}
            required
          />

          <Input
            label="Contact Name"
            placeholder="John Doe"
            value={formData.contact_name}
            onChange={(e) => handleInputChange('contact_name', e.target.value)}
            required
          />

          <Input
            label="Email Address"
            type="email"
            placeholder="john@company.com"
            value={formData.email}
            onChange={(e) => handleInputChange('email', e.target.value)}
            required
          />

          <Input
            label="Phone Number"
            placeholder="+60 12-345 6789"
            value={formData.phone}
            onChange={(e) => handleInputChange('phone', e.target.value)}
          />
        </div>

        <Textarea
          label="Use Case Description"
          placeholder="Describe how you plan to use KuasaTurbo API in your application..."
          value={formData.use_case}
          onChange={(e) => handleInputChange('use_case', e.target.value)}
          rows={4}
          required
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Select
            label="Expected Volume"
            options={volumeOptions}
            value={formData.expected_volume}
            onChange={(e) => handleInputChange('expected_volume', e.target.value)}
            required
          />

          <Select
            label="Integration Timeline"
            options={timelineOptions}
            value={formData.integration_timeline}
            onChange={(e) => handleInputChange('integration_timeline', e.target.value)}
            required
          />
        </div>

        <Textarea
          label="Additional Information"
          placeholder="Any specific requirements, questions, or additional context..."
          value={formData.additional_info}
          onChange={(e) => handleInputChange('additional_info', e.target.value)}
          rows={3}
        />

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">🔒 Enterprise Features</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Dedicated API keys dengan rate limiting</li>
            <li>• Priority support dan SLA guarantees</li>
            <li>• Custom integrations dan white-label options</li>
            <li>• Advanced analytics dan usage reporting</li>
          </ul>
        </div>

        <Button
          type="submit"
          variant="primary"
          size="lg"
          className="w-full"
          loading={isSubmitting}
        >
          Submit API Access Request
        </Button>

        <p className="text-xs text-gray-500 text-center">
          By submitting this form, you agree to our terms of service dan privacy policy. 
          We'll only use your information to process your API access request.
        </p>
      </form>
    </Card>
  );
}