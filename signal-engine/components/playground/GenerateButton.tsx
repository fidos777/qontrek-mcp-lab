"use client";

import Button from '@/components/shared/Button';
import Spinner from '@/components/shared/Spinner';
import type { Widget } from '@/lib/types';
import { trackEstimatorUsed } from '@/lib/track';

interface GenerateButtonProps {
  widget: Widget | null;
  formData: Record<string, any>;
  isExecuting: boolean;
  onGenerate: () => void;
}

export default function GenerateButton({ widget, formData, isExecuting, onGenerate }: GenerateButtonProps) {
  if (!widget) {
    return null;
  }

  // Check if required fields are filled
  const requiredFields = widget.fields.filter(field => field.required);
  const missingFields = requiredFields.filter(field => {
    const value = formData[field.id];
    return !value || (typeof value === 'string' && value.trim() === '');
  });

  const canGenerate = missingFields.length === 0;

  const handleClick = () => {
    if (canGenerate && !isExecuting) {
      trackEstimatorUsed(widget.id, widget.estimatedCredits);
      onGenerate();
    }
  };

  return (
    <div className="space-y-4">
      {/* Credit Estimation */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-medium text-blue-900">Credit Estimation</h4>
            <p className="text-sm text-blue-700">
              This task will consume approximately {widget.estimatedCredits} credits
            </p>
          </div>
          <div className="text-2xl font-bold text-blue-600">
            {widget.estimatedCredits}
          </div>
        </div>
      </div>

      {/* Validation Messages */}
      {missingFields.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 className="font-medium text-yellow-900 mb-2">Required Fields Missing</h4>
          <ul className="text-sm text-yellow-700 space-y-1">
            {missingFields.map(field => (
              <li key={field.id}>• {field.label}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Generate Button */}
      <Button
        variant="primary"
        size="lg"
        className={`w-full ${isExecuting ? 'animate-pulse' : ''}`}
        disabled={!canGenerate || isExecuting}
        onClick={handleClick}
      >
        {isExecuting ? (
          <span className="flex items-center space-x-2">
            <Spinner size="sm" />
            <span>Generating...</span>
          </span>
        ) : (
          `Generate ${widget.name}`
        )}
      </Button>

      {/* Draft Mode Notice */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <span>📝</span>
          <span>
            <strong>Draft Mode:</strong> Output will be editable dan tidak akan di-commit to any ledger
          </span>
        </div>
      </div>
    </div>
  );
}