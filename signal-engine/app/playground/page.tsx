"use client";

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Card from '@/components/shared/Card';
import TabSelector from '@/components/playground/TabSelector';
import WorkSelector from '@/components/playground/WorkSelector';
import ContextForm from '@/components/playground/ContextForm';
import GenerateButton from '@/components/playground/GenerateButton';
import DraftOutput from '@/components/playground/DraftOutput';
import ActionButtons from '@/components/playground/ActionButtons';
import CreditInfo from '@/components/playground/CreditInfo';
import SafetyNotes from '@/components/playground/SafetyNotes';
import WitnessModal from '@/components/playground/WitnessModal';
import ProofStrip from '@/components/playground/ProofStrip';
import GateBadge from '@/components/playground/GateBadge';
import RequestModal from '@/components/forms/RequestModal';
import { executeWidget } from '@/lib/api';
import { getWidgetById } from '@/lib/widgets';
import { parseDeepLinks, extractFormDefaults, validateDeepLinks } from '@/lib/deeplinks';
import { trackWorkRun } from '@/lib/track';
import type { PlaygroundTab, PlaygroundState, Widget, ExecuteWidgetResponse } from '@/lib/types';

export default function PlaygroundPage() {
  const searchParams = useSearchParams();
  
  // Parse deep links on mount
  const deepLinks = parseDeepLinks(searchParams);
  const deepLinkValidation = validateDeepLinks(deepLinks);
  
  // State management
  const [activeTab, setActiveTab] = useState<PlaygroundTab>(deepLinks.tab || 'ops');
  const [selectedWidget, setSelectedWidget] = useState<Widget | null>(
    deepLinks.work ? getWidgetById(deepLinks.work) || null : null
  );
  const [formData, setFormData] = useState<Record<string, any>>(
    deepLinks.work ? extractFormDefaults(deepLinks, deepLinks.work) : {}
  );
  const [isExecuting, setIsExecuting] = useState(false);
  const [result, setResult] = useState<ExecuteWidgetResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showWitnessModal, setShowWitnessModal] = useState(false);
  const [showRequestModal, setShowRequestModal] = useState(false);

  // Mock credit balance
  const [currentCredits] = useState(150);

  // Handle tab change
  const handleTabChange = (tab: PlaygroundTab) => {
    setActiveTab(tab);
    setSelectedWidget(null);
    setFormData({});
    setResult(null);
    setError(null);
  };

  // Handle widget selection
  const handleWidgetSelect = (widget: Widget) => {
    setSelectedWidget(widget);
    setFormData(extractFormDefaults(deepLinks, widget.id));
    setResult(null);
    setError(null);
  };

  // Handle form data change
  const handleFormChange = (data: Record<string, any>) => {
    setFormData(data);
  };

  // Handle generation
  const handleGenerate = async () => {
    if (!selectedWidget) return;

    setIsExecuting(true);
    setError(null);

    try {
      const response = await executeWidget({
        widget_id: selectedWidget.id,
        payload: formData,
        context: {
          session_id: `session_${Date.now()}`,
        },
      });

      setResult(response);
      trackWorkRun(selectedWidget.id, response.credits_charged);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Generation failed');
    } finally {
      setIsExecuting(false);
    }
  };

  // Handle generate another
  const handleGenerateAnother = () => {
    setResult(null);
    setError(null);
  };

  // Handle witness modal
  const handleWitnessClick = () => {
    setShowWitnessModal(true);
  };

  // Handle feature request
  const handleRequestFeature = () => {
    setShowRequestModal(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container section-padding">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-4">
            KuasaTurbo <span className="text-gradient">Playground</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Try our AI workers untuk operations, sales, dan creative tasks. All outputs are drafts yang boleh di-edit.
          </p>
        </div>

        {/* Deep Link Validation Errors */}
        {!deepLinkValidation.valid && (
          <div className="mb-6">
            <Card variant="bordered" className="bg-yellow-50 border-yellow-200">
              <div className="space-y-2">
                <h3 className="font-medium text-yellow-900">Deep Link Issues:</h3>
                <ul className="text-sm text-yellow-800 space-y-1">
                  {deepLinkValidation.errors.map((error, index) => (
                    <li key={index}>• {error}</li>
                  ))}
                </ul>
              </div>
            </Card>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Tab Selector */}
            <Card variant="bordered">
              <TabSelector activeTab={activeTab} onTabChange={handleTabChange} />
            </Card>

            {/* Work Selector */}
            {!selectedWidget ? (
              <Card variant="bordered">
                <WorkSelector
                  activeTab={activeTab}
                  selectedWidget={selectedWidget?.id || null}
                  onWidgetSelect={handleWidgetSelect}
                />
              </Card>
            ) : (
              <Card variant="bordered">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <h3 className="font-medium text-gray-900">{selectedWidget.name}</h3>
                    <GateBadge gateType="draft" status="active" />
                  </div>
                  <button
                    onClick={() => setSelectedWidget(null)}
                    className="text-sm text-gray-500 hover:text-gray-700"
                  >
                    ← Choose Different Task
                  </button>
                </div>
                
                <ContextForm
                  widget={selectedWidget}
                  formData={formData}
                  onFormChange={handleFormChange}
                />
              </Card>
            )}

            {/* Generate Button */}
            {selectedWidget && (
              <GenerateButton
                widget={selectedWidget}
                formData={formData}
                isExecuting={isExecuting}
                onGenerate={handleGenerate}
              />
            )}

            {/* Error Display */}
            {error && (
              <Card variant="bordered" className="bg-red-50 border-red-200">
                <div className="flex items-start space-x-2">
                  <span className="text-red-600 mt-0.5">❌</span>
                  <div>
                    <h4 className="font-medium text-red-900">Generation Failed</h4>
                    <p className="text-sm text-red-800 mt-1">{error}</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Result Display */}
            {result && (
              <div className="space-y-4">
                <ProofStrip executionId={result.execution_id} isVisible={true} />
                <Card variant="bordered">
                  <DraftOutput result={result} onGenerateAnother={handleGenerateAnother} />
                </Card>
              </div>
            )}

            {/* Safety Notes */}
            <SafetyNotes />
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Credit Info */}
            <CreditInfo
              currentCredits={currentCredits}
              estimatedCost={selectedWidget?.estimatedCredits || 0}
            />

            {/* Action Buttons */}
            <ActionButtons
              executionId={result?.execution_id}
              onWitnessClick={handleWitnessClick}
              onRequestFeature={handleRequestFeature}
            />

            {/* Quick Stats */}
            <Card variant="bordered" className="bg-blue-50 border-blue-200">
              <div className="space-y-3">
                <h4 className="font-medium text-blue-900">Session Stats</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-blue-600 font-medium">Active Tab</div>
                    <div className="text-blue-800 capitalize">{activeTab}</div>
                  </div>
                  <div>
                    <div className="text-blue-600 font-medium">Selected</div>
                    <div className="text-blue-800">{selectedWidget ? '✓' : '○'}</div>
                  </div>
                  <div>
                    <div className="text-blue-600 font-medium">Generated</div>
                    <div className="text-blue-800">{result ? '✓' : '○'}</div>
                  </div>
                  <div>
                    <div className="text-blue-600 font-medium">Credits Used</div>
                    <div className="text-blue-800">{result?.credits_charged || 0}</div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Modals */}
        <WitnessModal
          isOpen={showWitnessModal}
          onClose={() => setShowWitnessModal(false)}
          executionId={result?.execution_id}
        />
        
        <RequestModal
          isOpen={showRequestModal}
          onClose={() => setShowRequestModal(false)}
        />
      </div>
    </div>
  );
}