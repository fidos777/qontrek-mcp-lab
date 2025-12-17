"use client";

import Link from 'next/link';
import Card from '@/components/shared/Card';
import Badge from '@/components/shared/Badge';
import Button from '@/components/shared/Button';
import { CREDIT_PACKS } from '@/lib/constants';
import { trackConversionClick } from '@/lib/track';

interface CreditInfoProps {
  currentCredits?: number;
  estimatedCost?: number;
}

export default function CreditInfo({ currentCredits = 0, estimatedCost = 0 }: CreditInfoProps) {
  const canAfford = currentCredits >= estimatedCost;
  const recommendedPack = CREDIT_PACKS.find(pack => pack.credits >= estimatedCost * 10) || CREDIT_PACKS[0];

  const handleBuyCreditsClick = () => {
    trackConversionClick('credit_info', 'pricing');
  };

  return (
    <Card variant="bordered" className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">Credit Balance</h3>
          <Badge variant={canAfford ? 'success' : 'warning'} size="sm">
            {currentCredits} credits
          </Badge>
        </div>

        {estimatedCost > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Estimated cost:</span>
              <span className="font-medium">{estimatedCost} credits</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">After execution:</span>
              <span className={`font-medium ${canAfford ? 'text-green-600' : 'text-red-600'}`}>
                {currentCredits - estimatedCost} credits
              </span>
            </div>
          </div>
        )}

        {!canAfford && estimatedCost > 0 && (
          <div className="bg-yellow-100 border border-yellow-300 rounded-lg p-3">
            <div className="flex items-start space-x-2">
              <span className="text-yellow-600 mt-0.5">⚠️</span>
              <div className="text-sm text-yellow-800">
                <strong>Insufficient Credits:</strong> You need {estimatedCost - currentCredits} more credits to run this task.
              </div>
            </div>
          </div>
        )}

        <div className="space-y-3">
          <div className="text-sm text-gray-600">
            <strong>Quick Top-up:</strong>
          </div>
          <div className="grid grid-cols-3 gap-2">
            {CREDIT_PACKS.slice(0, 3).map((pack) => (
              <div key={pack.id} className="text-center p-2 bg-white rounded border">
                <div className="text-xs font-medium text-gray-900">{pack.credits}</div>
                <div className="text-xs text-gray-500">RM{pack.price}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-2">
          <Button
            variant="primary"
            size="sm"
            className="flex-1"
            onClick={handleBuyCreditsClick}
          >
            <Link href="/pricing">Buy Credits</Link>
          </Button>
          <Button variant="outline" size="sm" className="flex-1">
            <Link href="/credits">View Usage</Link>
          </Button>
        </div>

        <div className="text-xs text-gray-500 text-center">
          💡 Credits never expire dan can be used across all widgets
        </div>
      </div>
    </Card>
  );
}