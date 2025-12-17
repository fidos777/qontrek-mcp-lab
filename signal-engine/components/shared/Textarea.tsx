"use client";

import { TextareaHTMLAttributes, forwardRef } from 'react';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className = '', label, error, helperText, ...props }, ref) => {
    const baseClasses = 'block w-full rounded-lg border px-3 py-2 text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed resize-vertical transition-all duration-200 ease-out';
    const normalClasses = 'border-gray-300 focus:border-primary focus:ring-primary hover:border-gray-400';
    const errorClasses = 'border-red-300 focus:border-red-500 focus:ring-red-500 animate-shake';
    
    const textareaClasses = `${baseClasses} ${error ? errorClasses : normalClasses} ${className}`;
    
    return (
      <div className="space-y-1">
        {label && (
          <label className="block text-sm font-medium text-gray-700">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <textarea 
          ref={ref} 
          className={textareaClasses} 
          rows={props.rows || 3}
          {...props} 
        />
        {error && (
          <p className="text-sm text-red-600">{error}</p>
        )}
        {helperText && !error && (
          <p className="text-sm text-gray-500">{helperText}</p>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';

export default Textarea;