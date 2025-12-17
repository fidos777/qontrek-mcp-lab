// KuasaTurbo Signal Engine API Client

import type { ExecuteWidgetParams, ExecuteWidgetResponse, TrackEventParams, FeatureRequest } from './types';
import { ALLOWED_EVENTS } from './constants';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

/**
 * Execute a widget with given parameters
 */
export async function executeWidget(params: ExecuteWidgetParams): Promise<ExecuteWidgetResponse> {
  // If no API URL configured, return mock response
  if (!API_BASE_URL) {
    return generateMockResponse(params);
  }

  try {
    const response = await fetch(`${API_BASE_URL}/v1/engine/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'demo_key',
      },
      body: JSON.stringify(params),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Widget execution failed, returning mock:', error);
    return generateMockResponse(params);
  }
}

/**
 * Track user events for analytics
 */
export async function trackEvent(params: TrackEventParams): Promise<void> {
  // Validate event type
  if (!ALLOWED_EVENTS.includes(params.event as any)) {
    console.warn(`Invalid event type: ${params.event}`);
    return;
  }

  try {
    await fetch('/api/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...params,
        timestamp: params.timestamp || new Date().toISOString(),
      }),
    });
  } catch (error) {
    console.error('Event tracking failed:', error);
  }
}

/**
 * Submit feature request
 */
export async function submitFeatureRequest(request: FeatureRequest): Promise<void> {
  try {
    const response = await fetch('/api/request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Request submission failed: ${response.status}`);
    }
  } catch (error) {
    console.error('Feature request submission failed:', error);
    throw error;
  }
}

/**
 * Generate mock response for widget execution
 */
function generateMockResponse(params: ExecuteWidgetParams): Promise<ExecuteWidgetResponse> {
  return new Promise((resolve) => {
    setTimeout(() => {
      const mockOutputs: Record<string, any> = {
        'ops.attendance_tracker': {
          content: `Attendance recorded for ${params.payload.employee_name || 'Employee'}:\n\nDate: ${params.payload.date || 'Today'}\nCheck In: ${params.payload.check_in || '09:00'}\nCheck Out: ${params.payload.check_out || 'Pending'}\n\nStatus: ${params.payload.check_out ? 'Complete' : 'In Progress'}`,
          metadata: {
            hours_worked: params.payload.check_out ? '8.5' : 'TBD',
            status: params.payload.check_out ? 'complete' : 'in_progress',
          },
        },
        'ops.invoice_generator': {
          content: `INVOICE\n\nInvoice #: ${params.payload.invoice_number || 'INV-001'}\nClient: ${params.payload.client_name || 'Client Name'}\nDue Date: ${params.payload.due_date || '30 days'}\n\nItems:\n${params.payload.items || 'Service items'}\n\nPayment Terms: ${params.payload.payment_terms || 'Net 30'}\n\nTotal: RM XXX.XX`,
          metadata: {
            invoice_number: params.payload.invoice_number || 'INV-001',
            client: params.payload.client_name || 'Client Name',
            status: 'draft',
          },
        },
        'ops.expense_categorizer': {
          content: `Expense Analysis:\n\nDescription: ${params.payload.expense_description || 'Expense'}\nAmount: RM ${params.payload.amount || '0.00'}\nDate: ${params.payload.date || 'Today'}\n\nSuggested Category: Transportation\nTax Deductible: Yes\nGST/SST: 6%`,
          metadata: {
            category: 'transportation',
            tax_deductible: true,
            gst_rate: 0.06,
          },
        },
        'ops.task_scheduler': {
          content: `Task Scheduled:\n\nTitle: ${params.payload.task_title || 'Task'}\nAssigned to: ${params.payload.assignee || 'Team Member'}\nPriority: ${params.payload.priority || 'Medium'}\nDue: ${params.payload.due_date || 'TBD'}\n\nDescription:\n${params.payload.description || 'Task details'}\n\nStatus: Pending\nReminders: Set for 1 day before due date`,
          metadata: {
            task_id: `task_${Date.now()}`,
            priority: params.payload.priority || 'medium',
            status: 'pending',
          },
        },
        'sales.lead_qualifier': {
          content: `Lead Qualification Report:\n\nLead: ${params.payload.lead_name || 'Prospect'}\nCompany: ${params.payload.company || 'N/A'}\nBudget: ${params.payload.budget_range || 'Unknown'}\nTimeline: ${params.payload.timeline || 'Unknown'}\n\nPain Points:\n${params.payload.pain_points || 'To be determined'}\n\nLead Score: 75/100\nRecommendation: High priority follow-up\nNext Action: Schedule demo call`,
          metadata: {
            lead_score: 75,
            qualification: 'qualified',
            next_action: 'demo_call',
          },
        },
        'sales.proposal_generator': {
          content: `BUSINESS PROPOSAL\n\nClient: ${params.payload.client_name || 'Client'}\nProject: ${params.payload.project_scope || 'Project Description'}\n\nProposed Investment: RM ${params.payload.budget || '0'}\nTimeline: ${params.payload.timeline || 'TBD'}\n\nKey Deliverables:\n${params.payload.deliverables || 'To be defined'}\n\nNext Steps:\n1. Review and feedback\n2. Contract negotiation\n3. Project kickoff`,
          metadata: {
            proposal_id: `prop_${Date.now()}`,
            budget: params.payload.budget || 0,
            status: 'draft',
          },
        },
        'sales.followup_scheduler': {
          content: `Follow-up Scheduled:\n\nProspect: ${params.payload.prospect_name || 'Prospect'}\nLast Contact: ${params.payload.last_contact || 'Unknown'}\nMethod: ${params.payload.contact_method || 'Email'}\nReason: ${params.payload.follow_up_reason || 'General follow-up'}\n\nNotes:\n${params.payload.notes || 'No additional notes'}\n\nScheduled for: 3 days from now\nReminder set: 1 day before`,
          metadata: {
            follow_up_id: `followup_${Date.now()}`,
            scheduled_date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
            status: 'scheduled',
          },
        },
        'creative.social_caption': {
          content: `Social Media Caption for ${params.payload.platform || 'Platform'}:\n\n"${generateSocialCaption(params.payload)}"\n\n${params.payload.hashtags ? '#business #success #growth #motivation' : ''}\n\nEngagement Tips:\n- Post during peak hours\n- Encourage comments with questions\n- Use relevant hashtags\n- Include call-to-action`,
          metadata: {
            platform: params.payload.platform || 'instagram',
            tone: params.payload.tone || 'professional',
            character_count: 150,
          },
        },
        'meta.request_new_task': {
          content: `Feature Request Submitted:\n\nTask: ${params.payload.task_name || 'New Task'}\nCategory: ${params.payload.category || 'Other'}\nPriority: ${params.payload.priority || 'Medium'}\n\nDescription:\n${params.payload.description || 'No description'}\n\nUse Case:\n${params.payload.use_case || 'No use case provided'}\n\nStatus: Under Review\nEstimated Timeline: 2-4 weeks\nContact: ${params.payload.contact_email || 'Not provided'}`,
          metadata: {
            request_id: `req_${Date.now()}`,
            status: 'under_review',
            priority: params.payload.priority || 'medium',
          },
        },
      };

      const widgetOutput = mockOutputs[params.widget_id] || {
        content: `Mock output for ${params.widget_id}`,
        metadata: { mock: true },
      };

      resolve({
        status: 'success',
        execution_id: `exec_${Date.now()}`,
        widget_id: params.widget_id,
        draft_mode: true,
        credits_charged: Math.floor(Math.random() * 5) + 1,
        outputs: widgetOutput,
        next_steps: [
          'Review the generated output',
          'Make any necessary edits',
          'Save or export the result',
        ],
      });
    }, 1500);
  });
}

function generateSocialCaption(payload: any): string {
  const platform = payload.platform || 'Instagram';
  const tone = payload.tone || 'professional';
  const message = payload.key_message || 'Share your message here';
  
  const toneMap: Record<string, string> = {
    professional: `Excited to share: ${message}. What are your thoughts?`,
    casual: `Hey everyone! ${message} 😊 Let me know what you think!`,
    funny: `Plot twist: ${message} 😂 Who else can relate?`,
    inspirational: `Remember: ${message} ✨ You've got this!`,
    urgent: `Don't miss out! ${message} ⏰ Act now!`,
  };

  return toneMap[tone] || toneMap.professional;
}