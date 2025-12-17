"use client";

import Badge from '@/components/shared/Badge';

interface ProofStripProps {
  executionId?: string;
  isVisible?: boolean;
}

export default function ProofStrip({ executionId, isVisible = false }: ProofStripProps) {
  if (!isVisible || !executionId) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <span className="text-purple-600">🔗</span>
            <span className="font-medium text-purple-900 text-sm">Blockchain Proof</span>
          </div>
          <Badge variant="default" size="sm" className="bg-purple-100 text-purple-800">
            Coming Soon
          </Badge>
        </div>
        
        <div className="flex items-center space-x-2 text-xs text-purple-700">
          <span>Hash:</span>
          <code className="bg-purple-100 px-2 py-1 rounded font-mono">
            0x{executionId.slice(-8)}...
          </code>
        </div>
      </div>
      
      <div className="mt-2 text-xs text-purple-600">
        This execution will be eligible for blockchain witness once the feature is available
      </div>
    </div>
  );
}