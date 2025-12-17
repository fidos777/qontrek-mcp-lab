// KuasaTurbo Signal Engine Widget Definitions

import type { Widget } from './types';

export const WIDGETS: Widget[] = [
  // Operations Widgets (4)
  {
    id: 'ops.attendance_tracker',
    name: 'Attendance Tracker',
    namespace: 'ops.attendance_tracker',
    description: 'Track daily attendance dengan automated reporting',
    category: 'ops',
    estimatedCredits: 2,
    fields: [
      {
        id: 'employee_name',
        label: 'Employee Name',
        type: 'text',
        required: true,
        placeholder: 'Ahmad bin Ali',
      },
      {
        id: 'date',
        label: 'Date',
        type: 'text',
        required: true,
        placeholder: '2024-12-13',
      },
      {
        id: 'check_in',
        label: 'Check In Time',
        type: 'text',
        required: true,
        placeholder: '09:00',
      },
      {
        id: 'check_out',
        label: 'Check Out Time',
        type: 'text',
        required: false,
        placeholder: '17:30',
      },
      {
        id: 'notes',
        label: 'Notes',
        type: 'textarea',
        required: false,
        placeholder: 'Any additional notes...',
      },
    ],
  },
  {
    id: 'ops.invoice_generator',
    name: 'Invoice Generator',
    namespace: 'ops.invoice_generator',
    description: 'Generate professional invoices dengan auto calculations',
    category: 'ops',
    estimatedCredits: 3,
    fields: [
      {
        id: 'client_name',
        label: 'Client Name',
        type: 'text',
        required: true,
        placeholder: 'ABC Sdn Bhd',
      },
      {
        id: 'invoice_number',
        label: 'Invoice Number',
        type: 'text',
        required: true,
        placeholder: 'INV-2024-001',
      },
      {
        id: 'items',
        label: 'Items/Services',
        type: 'textarea',
        required: true,
        placeholder: 'Item 1: RM100\nItem 2: RM200',
      },
      {
        id: 'due_date',
        label: 'Due Date',
        type: 'text',
        required: true,
        placeholder: '2024-12-31',
      },
      {
        id: 'payment_terms',
        label: 'Payment Terms',
        type: 'select',
        required: true,
        options: ['Net 30', 'Net 15', 'Due on Receipt', 'Net 60'],
      },
    ],
  },
  {
    id: 'ops.expense_categorizer',
    name: 'Expense Categorizer',
    namespace: 'ops.expense_categorizer',
    description: 'Automatically categorize expenses untuk accounting',
    category: 'ops',
    estimatedCredits: 1,
    fields: [
      {
        id: 'expense_description',
        label: 'Expense Description',
        type: 'text',
        required: true,
        placeholder: 'Petrol for company car',
      },
      {
        id: 'amount',
        label: 'Amount (RM)',
        type: 'number',
        required: true,
        placeholder: '50.00',
      },
      {
        id: 'receipt_image',
        label: 'Receipt Image',
        type: 'file',
        required: false,
      },
      {
        id: 'date',
        label: 'Date',
        type: 'text',
        required: true,
        placeholder: '2024-12-13',
      },
    ],
  },
  {
    id: 'ops.task_scheduler',
    name: 'Task Scheduler',
    namespace: 'ops.task_scheduler',
    description: 'Schedule and organize team tasks dengan priorities',
    category: 'ops',
    estimatedCredits: 2,
    fields: [
      {
        id: 'task_title',
        label: 'Task Title',
        type: 'text',
        required: true,
        placeholder: 'Update website content',
      },
      {
        id: 'assignee',
        label: 'Assigned To',
        type: 'text',
        required: true,
        placeholder: 'John Doe',
      },
      {
        id: 'priority',
        label: 'Priority',
        type: 'select',
        required: true,
        options: ['High', 'Medium', 'Low'],
      },
      {
        id: 'due_date',
        label: 'Due Date',
        type: 'text',
        required: true,
        placeholder: '2024-12-20',
      },
      {
        id: 'description',
        label: 'Task Description',
        type: 'textarea',
        required: false,
        placeholder: 'Detailed task description...',
      },
    ],
  },

  // Sales Widgets (3)
  {
    id: 'sales.lead_qualifier',
    name: 'Lead Qualifier',
    namespace: 'sales.lead_qualifier',
    description: 'Qualify leads dengan scoring system',
    category: 'sales',
    estimatedCredits: 3,
    fields: [
      {
        id: 'lead_name',
        label: 'Lead Name',
        type: 'text',
        required: true,
        placeholder: 'Siti Abdullah',
      },
      {
        id: 'company',
        label: 'Company',
        type: 'text',
        required: false,
        placeholder: 'XYZ Sdn Bhd',
      },
      {
        id: 'budget_range',
        label: 'Budget Range',
        type: 'select',
        required: true,
        options: ['< RM10k', 'RM10k-50k', 'RM50k-100k', '> RM100k'],
      },
      {
        id: 'timeline',
        label: 'Decision Timeline',
        type: 'select',
        required: true,
        options: ['Immediate', '1-3 months', '3-6 months', '6+ months'],
      },
      {
        id: 'pain_points',
        label: 'Pain Points',
        type: 'textarea',
        required: true,
        placeholder: 'What challenges are they facing?',
      },
    ],
  },
  {
    id: 'sales.proposal_generator',
    name: 'Proposal Generator',
    namespace: 'sales.proposal_generator',
    description: 'Generate sales proposals dengan pricing',
    category: 'sales',
    estimatedCredits: 5,
    fields: [
      {
        id: 'client_name',
        label: 'Client Name',
        type: 'text',
        required: true,
        placeholder: 'ABC Corporation',
      },
      {
        id: 'project_scope',
        label: 'Project Scope',
        type: 'textarea',
        required: true,
        placeholder: 'Describe the project requirements...',
      },
      {
        id: 'budget',
        label: 'Proposed Budget (RM)',
        type: 'number',
        required: true,
        placeholder: '25000',
      },
      {
        id: 'timeline',
        label: 'Project Timeline',
        type: 'text',
        required: true,
        placeholder: '3 months',
      },
      {
        id: 'deliverables',
        label: 'Key Deliverables',
        type: 'textarea',
        required: true,
        placeholder: 'List main deliverables...',
      },
    ],
  },
  {
    id: 'sales.followup_scheduler',
    name: 'Follow-up Scheduler',
    namespace: 'sales.followup_scheduler',
    description: 'Schedule follow-ups dengan automated reminders',
    category: 'sales',
    estimatedCredits: 2,
    fields: [
      {
        id: 'prospect_name',
        label: 'Prospect Name',
        type: 'text',
        required: true,
        placeholder: 'Maria Santos',
      },
      {
        id: 'last_contact',
        label: 'Last Contact Date',
        type: 'text',
        required: true,
        placeholder: '2024-12-10',
      },
      {
        id: 'contact_method',
        label: 'Preferred Contact Method',
        type: 'select',
        required: true,
        options: ['WhatsApp', 'Email', 'Phone Call', 'In-Person'],
      },
      {
        id: 'follow_up_reason',
        label: 'Follow-up Reason',
        type: 'select',
        required: true,
        options: ['Quote Follow-up', 'Check-in', 'New Offer', 'Meeting Reminder'],
      },
      {
        id: 'notes',
        label: 'Notes',
        type: 'textarea',
        required: false,
        placeholder: 'Additional context...',
      },
    ],
  },

  // Creative Widget (1)
  {
    id: 'creative.social_caption',
    name: 'Social Media Caption',
    namespace: 'creative.social_caption',
    description: 'Generate engaging social media captions',
    category: 'creative',
    estimatedCredits: 2,
    fields: [
      {
        id: 'platform',
        label: 'Platform',
        type: 'select',
        required: true,
        options: ['Instagram', 'Facebook', 'LinkedIn', 'TikTok', 'Twitter'],
      },
      {
        id: 'content_type',
        label: 'Content Type',
        type: 'select',
        required: true,
        options: ['Product Launch', 'Behind the Scenes', 'Educational', 'Promotional', 'Inspirational'],
      },
      {
        id: 'tone',
        label: 'Tone',
        type: 'select',
        required: true,
        options: ['Professional', 'Casual', 'Funny', 'Inspirational', 'Urgent'],
      },
      {
        id: 'key_message',
        label: 'Key Message',
        type: 'textarea',
        required: true,
        placeholder: 'What do you want to communicate?',
      },
      {
        id: 'hashtags',
        label: 'Include Hashtags',
        type: 'checkbox',
        required: false,
      },
    ],
  },

  // Meta Widget (1)
  {
    id: 'meta.request_new_task',
    name: 'Request New Task',
    namespace: 'meta.request_new_task',
    description: 'Request new widget atau feature untuk platform',
    category: 'meta',
    estimatedCredits: 0,
    fields: [
      {
        id: 'task_name',
        label: 'Task/Widget Name',
        type: 'text',
        required: true,
        placeholder: 'Customer Survey Generator',
      },
      {
        id: 'category',
        label: 'Category',
        type: 'select',
        required: true,
        options: ['Operations', 'Sales', 'Creative', 'Analytics', 'Other'],
      },
      {
        id: 'description',
        label: 'Description',
        type: 'textarea',
        required: true,
        placeholder: 'Describe what this task should do...',
      },
      {
        id: 'use_case',
        label: 'Use Case',
        type: 'textarea',
        required: true,
        placeholder: 'How would you use this in your business?',
      },
      {
        id: 'priority',
        label: 'Priority',
        type: 'select',
        required: true,
        options: ['Low', 'Medium', 'High'],
      },
      {
        id: 'contact_email',
        label: 'Contact Email',
        type: 'text',
        required: false,
        placeholder: 'your@email.com',
      },
    ],
  },
];

export function getWidgetsByCategory(category: 'ops' | 'sales' | 'creative' | 'meta'): Widget[] {
  return WIDGETS.filter(widget => widget.category === category);
}

export function getWidgetById(id: string): Widget | undefined {
  return WIDGETS.find(widget => widget.id === id);
}