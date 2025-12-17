// KuasaTurbo Signal Engine Types

export interface Widget {
  id: string;
  name: string;
  namespace: string;
  description: string;
  category: 'ops' | 'sales' | 'creative' | 'meta';
  fields: WidgetField[];
  estimatedCredits: number;
}

export interface WidgetField {
  id: string;
  label: string;
  type: 'text' | 'textarea' | 'select' | 'number' | 'file' | 'checkbox';
  required: boolean;
  placeholder?: string;
  options?: string[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
  };
}

export interface ExecuteWidgetParams {
  widget_id: string;
  payload: Record<string, any>;
  context?: {
    user_id?: string;
    session_id?: string;
  };
}

export interface ExecuteWidgetResponse {
  status: 'success' | 'error';
  execution_id: string;
  widget_id: string;
  draft_mode: boolean;
  credits_charged: number;
  outputs: {
    content: string;
    metadata: Record<string, any>;
    attachments?: string[];
  };
  next_steps?: string[];
  error?: string;
}

export interface TrackEventParams {
  event: string;
  properties?: Record<string, any>;
  timestamp?: string;
}

export interface FeatureRequest {
  title: string;
  description: string;
  category: string;
  priority: 'low' | 'medium' | 'high';
  contact_email?: string;
}

export type PlaygroundTab = 'ops' | 'sales' | 'creative';

export interface PlaygroundState {
  activeTab: PlaygroundTab;
  selectedWidget: string | null;
  formData: Record<string, any>;
  isExecuting: boolean;
  result: ExecuteWidgetResponse | null;
  error: string | null;
}

export interface CreditPack {
  id: string;
  name: string;
  credits: number;
  price: number;
  popular?: boolean;
  description: string;
}

export interface Vertical {
  slug: string;
  name: string;
  status: 'available' | 'coming_soon' | 'pilot';
  description: string;
  icon: string;
}