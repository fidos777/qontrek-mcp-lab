// KuasaTurbo Signal Engine Event Tracking

import { trackEvent } from './api';
import type { TrackEventParams } from './types';

/**
 * Track playground tab view
 */
export function trackTabView(tab: string) {
  trackEvent({
    event: 'tab_view',
    properties: { tab },
  });
}

/**
 * Track work start (widget selection)
 */
export function trackWorkStart(widgetId: string) {
  trackEvent({
    event: 'work_start',
    properties: { widget_id: widgetId },
  });
}

/**
 * Track work execution
 */
export function trackWorkRun(widgetId: string, creditsCharged: number) {
  trackEvent({
    event: 'work_run',
    properties: { 
      widget_id: widgetId,
      credits_charged: creditsCharged,
    },
  });
}

/**
 * Track draft save
 */
export function trackWorkSaveDraft(widgetId: string, executionId: string) {
  trackEvent({
    event: 'work_save_draft',
    properties: { 
      widget_id: widgetId,
      execution_id: executionId,
    },
  });
}

/**
 * Track proof save (placeholder)
 */
export function trackWorkSaveProof(widgetId: string, executionId: string) {
  trackEvent({
    event: 'work_save_proof',
    properties: { 
      widget_id: widgetId,
      execution_id: executionId,
    },
  });
}

/**
 * Track credit estimator usage
 */
export function trackEstimatorUsed(widgetId: string, estimatedCredits: number) {
  trackEvent({
    event: 'estimator_used',
    properties: { 
      widget_id: widgetId,
      estimated_credits: estimatedCredits,
    },
  });
}

/**
 * Track conversion clicks (pricing, etc.)
 */
export function trackConversionClick(source: string, target: string) {
  trackEvent({
    event: 'conversion_click',
    properties: { 
      source,
      target,
    },
  });
}

/**
 * Track feature request submission
 */
export function trackFeatureRequestSubmit(category: string, priority: string) {
  trackEvent({
    event: 'feature_request_submit',
    properties: { 
      category,
      priority,
    },
  });
}

/**
 * Track witness modal open (placeholder)
 */
export function trackWitnessModalOpen(executionId: string) {
  trackEvent({
    event: 'witness_modal_open',
    properties: { 
      execution_id: executionId,
    },
  });
}

/**
 * Track request modal open
 */
export function trackRequestModalOpen(source: string) {
  trackEvent({
    event: 'request_modal_open',
    properties: { 
      source,
    },
  });
}