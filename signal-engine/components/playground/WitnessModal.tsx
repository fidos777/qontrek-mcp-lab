"use client";

import Modal from '@/components/shared/Modal';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';

interface WitnessModalProps {
  isOpen: boolean;
  onClose: () => void;
  executionId?: string;
}

export default function WitnessModal({ isOpen, onClose, executionId }: WitnessModalProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Witness & Proof (Coming Soon)"
      size="lg"
    >
      <div className="space-y-6">
        {/* Status */}
        <div className="text-center">
          <div className="text-6xl mb-4">🚧</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Blockchain Witness Feature
          </h3>
          <p className="text-gray-600">
            This feature is under development dan will be available soon
          </p>
        </div>

        {/* What it will do */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-3">What Witness Will Provide:</h4>
          <ul className="space-y-2 text-sm text-blue-800">
            <li className="flex items-start space-x-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span>Cryptographic proof of your AI-generated content</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span>Immutable timestamp dan authorship verification</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span>Blockchain-based audit trail untuk compliance</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span>Integration with legal frameworks</span>
            </li>
          </ul>
        </div>

        {/* Current execution info */}
        {executionId && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 className="font-semibold text-gray-900 mb-2">Current Execution</h4>
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Execution ID:</span>
                <Badge variant="default" size="sm" className="font-mono text-xs">
                  {executionId}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Status:</span>
                <Badge variant="warning" size="sm">Draft Only</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Witness Ready:</span>
                <Badge variant="error" size="sm">Not Available</Badge>
              </div>
            </div>
          </div>
        )}

        {/* Timeline */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-3">Development Timeline:</h4>
          <div className="space-y-2 text-sm text-green-800">
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✓</span>
              <span>Draft mode implementation (Current)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-yellow-600">⏳</span>
              <span>Witness infrastructure setup (Q1 2025)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-gray-400">○</span>
              <span>Beta testing with selected partners (Q2 2025)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-gray-400">○</span>
              <span>Public release (Q3 2025)</span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3">
          <Button variant="outline" className="flex-1" onClick={onClose}>
            Close
          </Button>
          <Button variant="primary" className="flex-1" disabled>
            Join Beta Waitlist (Soon)
          </Button>
        </div>
      </div>
    </Modal>
  );
}