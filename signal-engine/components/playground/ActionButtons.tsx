"use client";

import Button from '@/components/shared/Button';
import { trackWitnessModalOpen, trackRequestModalOpen } from '@/lib/track';

interface ActionButtonsProps {
  executionId?: string;
  onWitnessClick: () => void;
  onRequestFeature: () => void;
}

export default function ActionButtons({ executionId, onWitnessClick, onRequestFeature }: ActionButtonsProps) {
  const handleWitnessClick = () => {
    if (executionId) {
      trackWitnessModalOpen(executionId);
    }
    onWitnessClick();
  };

  const handleRequestClick = () => {
    trackRequestModalOpen('playground');
    onRequestFeature();
  };

  return (
    <div className="space-y-4">
      {/* Witness Section (Placeholder) */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-medium text-gray-900">Witness & Proof</h4>
            <p className="text-sm text-gray-600">
              Verify dan commit your work to blockchain ledger
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            disabled={!executionId}
            onClick={handleWitnessClick}
          >
            🔗 Witness (Coming Soon)
          </Button>
        </div>
        {!executionId && (
          <p className="text-xs text-gray-500 mt-2">
            Generate content first to enable witness functionality
          </p>
        )}
      </div>

      {/* Feature Request */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-medium text-green-900">Need a New Widget?</h4>
            <p className="text-sm text-green-700">
              Request custom widgets untuk your specific use case
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            className="border-green-300 text-green-700 hover:bg-green-100"
            onClick={handleRequestClick}
          >
            💡 Request Feature
          </Button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-col sm:flex-row gap-2">
        <Button variant="ghost" size="sm" className="flex-1 text-left justify-start">
          📚 View Documentation
        </Button>
        <Button variant="ghost" size="sm" className="flex-1 text-left justify-start">
          💬 Get Support
        </Button>
        <Button variant="ghost" size="sm" className="flex-1 text-left justify-start">
          🔗 API Access
        </Button>
      </div>
    </div>
  );
}