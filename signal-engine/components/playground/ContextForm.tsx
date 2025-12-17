"use client";

import { useState } from 'react';
import Input from '@/components/shared/Input';
import Textarea from '@/components/shared/Textarea';
import Select from '@/components/shared/Select';
import type { Widget, WidgetField } from '@/lib/types';

interface ContextFormProps {
  widget: Widget;
  formData: Record<string, any>;
  onFormChange: (data: Record<string, any>) => void;
}

export default function ContextForm({ widget, formData, onFormChange }: ContextFormProps) {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleFieldChange = (fieldId: string, value: any) => {
    const newData = { ...formData, [fieldId]: value };
    onFormChange(newData);
    
    // Clear error when user starts typing
    if (errors[fieldId]) {
      setErrors(prev => ({ ...prev, [fieldId]: '' }));
    }
  };

  const validateField = (field: WidgetField, value: any): string => {
    if (field.required && (!value || value.toString().trim() === '')) {
      return `${field.label} is required`;
    }
    
    if (field.validation) {
      if (field.type === 'number') {
        const numValue = parseFloat(value);
        if (field.validation.min !== undefined && numValue < field.validation.min) {
          return `${field.label} must be at least ${field.validation.min}`;
        }
        if (field.validation.max !== undefined && numValue > field.validation.max) {
          return `${field.label} must be at most ${field.validation.max}`;
        }
      }
      
      if (field.validation.pattern && value) {
        const regex = new RegExp(field.validation.pattern);
        if (!regex.test(value)) {
          return `${field.label} format is invalid`;
        }
      }
    }
    
    return '';
  };

  const renderField = (field: WidgetField) => {
    const value = formData[field.id] || '';
    const error = errors[field.id];

    switch (field.type) {
      case 'text':
        return (
          <Input
            key={field.id}
            label={field.label}
            placeholder={field.placeholder}
            required={field.required}
            value={value}
            onChange={(e) => handleFieldChange(field.id, e.target.value)}
            error={error}
          />
        );
        
      case 'textarea':
        return (
          <Textarea
            key={field.id}
            label={field.label}
            placeholder={field.placeholder}
            required={field.required}
            value={value}
            onChange={(e) => handleFieldChange(field.id, e.target.value)}
            error={error}
            rows={4}
          />
        );
        
      case 'select':
        return (
          <Select
            key={field.id}
            label={field.label}
            required={field.required}
            value={value}
            onChange={(e) => handleFieldChange(field.id, e.target.value)}
            error={error}
            options={field.options?.map(opt => ({ value: opt, label: opt })) || []}
          />
        );
        
      case 'number':
        return (
          <Input
            key={field.id}
            type="number"
            label={field.label}
            placeholder={field.placeholder}
            required={field.required}
            value={value}
            onChange={(e) => handleFieldChange(field.id, e.target.value)}
            error={error}
            min={field.validation?.min}
            max={field.validation?.max}
          />
        );
        
      case 'checkbox':
        return (
          <div key={field.id} className="flex items-center space-x-2">
            <input
              type="checkbox"
              id={field.id}
              checked={value || false}
              onChange={(e) => handleFieldChange(field.id, e.target.checked)}
              className="rounded border-gray-300 text-primary focus:ring-primary"
            />
            <label htmlFor={field.id} className="text-sm font-medium text-gray-700">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
          </div>
        );
        
      case 'file':
        return (
          <div key={field.id} className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <input
              type="file"
              onChange={(e) => handleFieldChange(field.id, e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-primary file:text-white hover:file:bg-primary/90"
            />
            {error && <p className="text-sm text-red-600">{error}</p>}
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h3 className="text-lg font-medium text-gray-900">{widget.name}</h3>
        <p className="text-sm text-gray-600 mt-1">{widget.description}</p>
        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
          <span>Estimated: {widget.estimatedCredits} credits</span>
          <span>•</span>
          <span>{widget.fields.length} fields</span>
          <span>•</span>
          <span>Draft mode</span>
        </div>
      </div>

      <div className="space-y-4">
        {widget.fields.map(renderField)}
      </div>
    </div>
  );
}