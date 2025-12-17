"use client";

import { useState } from 'react';
import Modal from '@/components/shared/Modal';
import Button from '@/components/shared/Button';
import Input from '@/components/shared/Input';
import Textarea from '@/components/shared/Textarea';
import Select from '@/components/shared/Select';
import { submitFeatureRequest } from '@/lib/api';
import { trackFeatureRequestSubmit } from '@/lib/track';
import type { FeatureRequest } from '@/lib/types';

interface RequestModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function RequestModal({ isOpen, onClose }: RequestModalProps) {
  const [formData, setFormData] = useState<FeatureRequest>({
    title: '',
    description: '',
    category: '',
    priority: 'medium',
    contact_email: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const categoryOptions = [
    { value: 'Operations', label: 'Operations & Admin' },
    { value: 'Sales', label: 'Sales & CRM' },
    { value: 'Creative', label: 'Creative & Marketing' },
    { value: 'Analytics', label: 'Analytics & Reporting' },
    { value: 'Integration', label: 'Integration & API' },
    { value: 'Other', label: 'Other' },
  ];

  const priorityOptions = [
    { value: 'low', label: 'Low - Nice to have' },
    { value: 'medium', label: 'Medium - Would be helpful' },
    { value: 'high', label: 'High - Critical for my business' },
  ];

  const handleInputChange = (field: keyof FeatureRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title.trim() || !formData.description.trim() || !formData.category) {
      setError('Please fill in all required fields');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await submitFeatureRequest(formData);
      trackFeatureRequestSubmit(formData.category, formData.priority);
      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit request');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    if (!isSubmitting) {
      setFormData({
        title: '',
        description: '',
        category: '',
        priority: 'medium',
        contact_email: '',
      });
      setSubmitted(false);
      setError(null);
      onClose();
    }
  };

  if (submitted) {
    return (
      <Modal isOpen={isOpen} onClose={handleClose} title="Request Submitted!" size="md">
        <div className="text-center space-y-4">
          <div className="text-6xl">✅</div>
          <h3 className="text-xl font-semibold text-green-900">
            Thank you for your feedback!
          </h3>
          <p className="text-green-700">
            We've received your feature request dan will review it soon. 
            {formData.contact_email && ' We\'ll contact you if we need more details.'}
          </p>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-medium text-green-900 mb-2">What happens next?</h4>
            <ul className="text-sm text-green-800 space-y-1 text-left">
              <li>• Our team will review your request within 2-3 business days</li>
              <li>• High priority requests get faster attention</li>
              <li>• We'll add popular requests to our development roadmap</li>
              <li>• You'll be notified when the feature is available</li>
            </ul>
          </div>
          <Button variant="primary" onClick={handleClose}>
            Close
          </Button>
        </div>
      </Modal>
    );
  }

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Request New Feature" size="lg">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-4">
          <Input
            label="Feature Title"
            placeholder="e.g., Customer Survey Generator"
            value={formData.title}
            onChange={(e) => handleInputChange('title', e.target.value)}
            required
          />

          <Select
            label="Category"
            options={categoryOptions}
            value={formData.category}
            onChange={(e) => handleInputChange('category', e.target.value)}
            required
          />

          <Textarea
            label="Description"
            placeholder="Describe what this feature should do and how it would help your business..."
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            rows={4}
            required
          />

          <Select
            label="Priority"
            options={priorityOptions}
            value={formData.priority}
            onChange={(e) => handleInputChange('priority', e.target.value as 'low' | 'medium' | 'high')}
            required
          />

          <Input
            label="Contact Email (Optional)"
            type="email"
            placeholder="your@email.com"
            value={formData.contact_email}
            onChange={(e) => handleInputChange('contact_email', e.target.value)}
            helperText="We'll only use this to follow up on your request"
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">💡 Tips for better requests:</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Be specific about what the feature should do</li>
            <li>• Explain how it would help your business</li>
            <li>• Include examples if possible</li>
            <li>• Mention if you'd be willing to beta test</li>
          </ul>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={handleClose}
            disabled={isSubmitting}
            className="flex-1"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            className="flex-1"
          >
            Submit Request
          </Button>
        </div>
      </form>
    </Modal>
  );
}