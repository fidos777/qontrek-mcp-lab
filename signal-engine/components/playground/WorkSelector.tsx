"use client";

import Card from '@/components/shared/Card';
import Badge from '@/components/shared/Badge';
import { getWidgetsByCategory } from '@/lib/widgets';
import { WORK_CATEGORIES } from '@/lib/constants';
import type { PlaygroundTab, Widget } from '@/lib/types';
import { trackWorkStart } from '@/lib/track';

interface WorkSelectorProps {
  activeTab: PlaygroundTab;
  selectedWidget: string | null;
  onWidgetSelect: (widget: Widget) => void;
}

export default function WorkSelector({ activeTab, selectedWidget, onWidgetSelect }: WorkSelectorProps) {
  const widgets = getWidgetsByCategory(activeTab);

  const handleWidgetClick = (widget: Widget) => {
    onWidgetSelect(widget);
    trackWorkStart(widget.id);
  };

  if (widgets.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">🚧</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {WORK_CATEGORIES[activeTab]} widgets coming soon
        </h3>
        <p className="text-gray-500">
          We're working on adding more widgets untuk this category
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">
          Choose your {WORK_CATEGORIES[activeTab].toLowerCase()} task
        </h3>
        <Badge variant="default" size="sm">
          {widgets.length} available
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {widgets.map((widget) => (
          <Card
            key={widget.id}
            variant="bordered"
            className={`cursor-pointer transition-all hover:shadow-md ${
              selectedWidget === widget.id
                ? 'border-primary bg-primary/5'
                : 'hover:border-gray-300'
            }`}
            onClick={() => handleWidgetClick(widget)}
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <h4 className="font-medium text-gray-900">{widget.name}</h4>
                <div className="text-sm text-gray-500">
                  {widget.estimatedCredits} credits
                </div>
              </div>
              
              <p className="text-sm text-gray-600">{widget.description}</p>
              
              <div className="flex items-center justify-between">
                <Badge variant="primary" size="sm">
                  {widget.namespace}
                </Badge>
                <div className="text-xs text-gray-400">
                  {widget.fields.length} fields
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}