// Deep Link Utilities for Signal Engine

import type { PlaygroundTab } from './types';
import { getWidgetById } from './widgets';

export interface DeepLinkParams {
  tab?: PlaygroundTab;
  work?: string;
  [key: string]: string | undefined;
}

/**
 * Parse URL search params into deep link parameters
 */
export function parseDeepLinks(searchParams: URLSearchParams): DeepLinkParams {
  const params: DeepLinkParams = {};
  
  // Parse tab parameter
  const tab = searchParams.get('tab');
  if (tab && ['ops', 'sales', 'creative'].includes(tab)) {
    params.tab = tab as PlaygroundTab;
  }
  
  // Parse work parameter (widget ID)
  const work = searchParams.get('work');
  if (work) {
    const widget = getWidgetById(work);
    if (widget) {
      params.work = work;
      // Auto-set tab based on widget category if not explicitly set
      if (!params.tab) {
        params.tab = widget.category as PlaygroundTab;
      }
    }
  }
  
  // Parse other parameters as form defaults
  for (const [key, value] of searchParams.entries()) {
    if (key !== 'tab' && key !== 'work' && value) {
      params[key] = value;
    }
  }
  
  return params;
}

/**
 * Generate deep link URL for playground
 */
export function generateDeepLink(params: DeepLinkParams): string {
  const searchParams = new URLSearchParams();
  
  if (params.tab) {
    searchParams.set('tab', params.tab);
  }
  
  if (params.work) {
    searchParams.set('work', params.work);
  }
  
  // Add other parameters
  Object.entries(params).forEach(([key, value]) => {
    if (key !== 'tab' && key !== 'work' && value) {
      searchParams.set(key, value);
    }
  });
  
  const queryString = searchParams.toString();
  return `/playground${queryString ? `?${queryString}` : ''}`;
}

/**
 * Extract form defaults from deep link parameters
 */
export function extractFormDefaults(params: DeepLinkParams, widgetId: string): Record<string, any> {
  const widget = getWidgetById(widgetId);
  if (!widget) return {};
  
  const defaults: Record<string, any> = {};
  
  // Map URL parameters to widget fields
  widget.fields.forEach(field => {
    const value = params[field.id];
    if (value) {
      // Type conversion based on field type
      switch (field.type) {
        case 'number':
          const numValue = parseFloat(value);
          if (!isNaN(numValue)) {
            defaults[field.id] = numValue;
          }
          break;
        case 'checkbox':
          defaults[field.id] = value === 'true' || value === '1';
          break;
        default:
          defaults[field.id] = decodeURIComponent(value);
      }
    }
  });
  
  return defaults;
}

/**
 * Validate deep link parameters
 */
export function validateDeepLinks(params: DeepLinkParams): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  // Validate tab
  if (params.tab && !['ops', 'sales', 'creative'].includes(params.tab)) {
    errors.push(`Invalid tab: ${params.tab}`);
  }
  
  // Validate work (widget ID)
  if (params.work) {
    const widget = getWidgetById(params.work);
    if (!widget) {
      errors.push(`Invalid widget ID: ${params.work}`);
    } else if (params.tab && widget.category !== params.tab) {
      errors.push(`Widget ${params.work} does not belong to tab ${params.tab}`);
    }
  }
  
  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Example deep links for testing
 */
export const EXAMPLE_DEEP_LINKS = {
  // Tab selection
  opsTab: '/playground?tab=ops',
  salesTab: '/playground?tab=sales',
  creativeTab: '/playground?tab=creative',
  
  // Widget selection
  invoiceGenerator: '/playground?work=ops.invoice_generator',
  leadQualifier: '/playground?work=sales.lead_qualifier',
  socialCaption: '/playground?work=creative.social_caption',
  
  // Pre-filled forms
  invoiceWithData: '/playground?work=ops.invoice_generator&client_name=ABC%20Sdn%20Bhd&invoice_number=INV-2024-001',
  leadWithBudget: '/playground?work=sales.lead_qualifier&lead_name=John%20Doe&budget_range=%3C%20RM10k',
  captionForInstagram: '/playground?work=creative.social_caption&platform=Instagram&tone=Casual',
};