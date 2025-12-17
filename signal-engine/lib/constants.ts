// KuasaTurbo Signal Engine Constants

import type { CreditPack, Vertical } from './types';

export const BRAND_COLORS = {
  primary: '#FE4800',
  secondary: '#262A3B',
  accent: '#FF6B35',
  neutral: '#F8F9FA',
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
} as const;

export const CREDIT_PACKS: CreditPack[] = [
  {
    id: 'starter',
    name: 'Starter Pack',
    credits: 100,
    price: 29,
    description: 'Perfect untuk try out basic features',
  },
  {
    id: 'professional',
    name: 'Professional',
    credits: 500,
    price: 99,
    popular: true,
    description: 'Most popular untuk SME operations',
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    credits: 2000,
    price: 299,
    description: 'High volume untuk large organizations',
  },
];

export const VERTICALS: Vertical[] = [
  {
    slug: 'automotive',
    name: 'Automotive',
    status: 'available',
    description: 'Trade-in evaluation, loan checks, lead management',
    icon: '🚗',
  },
  {
    slug: 'fnb',
    name: 'F&B',
    status: 'pilot',
    description: 'Menu updates, promo generation, inventory tracking',
    icon: '🍽️',
  },
  {
    slug: 'solar',
    name: 'Solar',
    status: 'coming_soon',
    description: 'ROI calculations, proposal generation',
    icon: '☀️',
  },
  {
    slug: 'property',
    name: 'Property',
    status: 'coming_soon',
    description: 'Mortgage calculations, property valuations',
    icon: '🏠',
  },
  {
    slug: 'takaful',
    name: 'Takaful',
    status: 'coming_soon',
    description: 'Coverage calculations, policy comparisons',
    icon: '🛡️',
  },
];

export const ALLOWED_EVENTS = [
  'tab_view',
  'work_start',
  'work_run',
  'work_save_draft',
  'work_save_proof',
  'estimator_used',
  'conversion_click',
  'feature_request_submit',
  'witness_modal_open',
  'request_modal_open',
] as const;

export const PLAYGROUND_TABS = [
  { id: 'ops', label: 'Operations', icon: '⚙️' },
  { id: 'sales', label: 'Sales', icon: '💼' },
  { id: 'creative', label: 'Creative', icon: '🎨' },
] as const;

export const WORK_CATEGORIES = {
  ops: 'Operations & Admin',
  sales: 'Sales & CRM',
  creative: 'Creative & Marketing',
  meta: 'Platform Features',
} as const;