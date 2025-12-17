"use client";

import Badge from '@/components/shared/Badge';
import Tooltip from '@/components/shared/Tooltip';

interface GateBadgeProps {
  gateType?: 'draft' | 'witness' | 'proof';
  status?: 'active' | 'pending' | 'disabled';
}

export default function GateBadge({ gateType = 'draft', status = 'active' }: GateBadgeProps) {
  const gateConfig = {
    draft: {
      icon: '📝',
      label: 'Draft Mode',
      description: 'Output is editable dan tidak committed to ledger',
      variant: 'warning' as const,
    },
    witness: {
      icon: '👁️',
      label: 'Witness Ready',
      description: 'Ready untuk blockchain witness verification',
      variant: 'primary' as const,
    },
    proof: {
      icon: '🔗',
      label: 'Proof Generated',
      description: 'Cryptographic proof available on blockchain',
      variant: 'success' as const,
    },
  };

  const statusConfig = {
    active: 'opacity-100',
    pending: 'opacity-75',
    disabled: 'opacity-50',
  };

  const config = gateConfig[gateType];

  return (
    <Tooltip content={config.description}>
      <div className={`inline-flex items-center ${statusConfig[status]}`}>
        <Badge variant={config.variant} size="sm">
          <span className="flex items-center space-x-1">
            <span>{config.icon}</span>
            <span>{config.label}</span>
            {status === 'pending' && <span className="animate-pulse">⏳</span>}
            {status === 'disabled' && <span>🚫</span>}
          </span>
        </Badge>
      </div>
    </Tooltip>
  );
}