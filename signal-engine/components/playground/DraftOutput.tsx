"use client";

import { useState } from 'react';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import Badge from '@/components/shared/Badge';
import type { ExecuteWidgetResponse } from '@/lib/types';
import { trackWorkSaveDraft } from '@/lib/track';

interface DraftOutputProps {
  result: ExecuteWidgetResponse;
  onGenerateAnother: () => void;
}

export default function DraftOutput({ result, onGenerateAnother }: DraftOutputProps) {
  const [editedContent, setEditedContent] = useState(result.outputs.content);
  const [showMetadata, setShowMetadata] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);

  const handleSaveDraft = async () => {
    setIsSaving(true);
    try {
      // Simulate save operation
      await new Promise(resolve => setTimeout(resolve, 1000));
      trackWorkSaveDraft(result.widget_id, result.execution_id);
      alert('Draft saved successfully!');
    } catch (error) {
      alert('Failed to save draft');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(editedContent);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (error) {
      alert('Failed to copy to clipboard');
    }
  };

  return (
    <div className="space-y-6 animate-fadeInUp">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Generated Output</h3>
          <p className="text-sm text-gray-600">Review dan edit as needed</p>
        </div>
        <div className="flex items-center space-x-2">
          {result.draft_mode && (
            <Badge variant="warning" size="sm">Draft Mode</Badge>
          )}
          <Badge variant="success" size="sm">
            {result.credits_charged} credits used
          </Badge>
        </div>
      </div>

      {/* Main Content */}
      <Card variant="bordered">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Generated Content (Editable)
            </label>
            <textarea
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              className="w-full h-64 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary resize-vertical transition-all duration-200 hover:border-gray-400"
              placeholder="Generated content will appear here..."
            />
          </div>

          {/* Metadata Toggle */}
          <div>
            <button
              onClick={() => setShowMetadata(!showMetadata)}
              className="text-sm text-primary hover:text-primary/80 font-medium"
            >
              {showMetadata ? 'Hide' : 'Show'} Metadata & Details
            </button>
            
            {showMetadata && (
              <div className="mt-3 p-4 bg-gray-50 rounded-lg">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Execution ID:</span>
                    <div className="text-gray-600 font-mono text-xs">{result.execution_id}</div>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Widget:</span>
                    <div className="text-gray-600">{result.widget_id}</div>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Credits Charged:</span>
                    <div className="text-gray-600">{result.credits_charged}</div>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Status:</span>
                    <div className="text-gray-600">{result.status}</div>
                  </div>
                </div>
                
                {result.outputs.metadata && Object.keys(result.outputs.metadata).length > 0 && (
                  <div className="mt-4">
                    <span className="font-medium text-gray-700">Additional Metadata:</span>
                    <pre className="mt-2 p-3 bg-white border rounded text-xs overflow-x-auto">
                      {JSON.stringify(result.outputs.metadata, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </Card>

      {/* Next Steps */}
      {result.next_steps && result.next_steps.length > 0 && (
        <Card variant="bordered" className="bg-blue-50 border-blue-200">
          <div>
            <h4 className="font-medium text-blue-900 mb-2">Suggested Next Steps</h4>
            <ul className="space-y-1 text-sm text-blue-800">
              {result.next_steps.map((step, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-blue-600 mt-0.5">•</span>
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </div>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <Button
          variant="primary"
          onClick={handleSaveDraft}
          loading={isSaving}
          className="flex-1"
        >
          Save Draft
        </Button>
        <Button
          variant="outline"
          onClick={handleCopyToClipboard}
          className="flex-1"
        >
          {copySuccess ? (
            <span className="flex items-center space-x-1">
              <span>✓</span>
              <span>Copied!</span>
            </span>
          ) : (
            'Copy to Clipboard'
          )}
        </Button>
        <Button
          variant="secondary"
          onClick={onGenerateAnother}
          className="flex-1"
        >
          Generate Another
        </Button>
      </div>

      {/* Draft Mode Notice */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <span className="text-yellow-600 mt-0.5">⚠️</span>
          <div className="text-sm text-yellow-800">
            <strong>Draft Mode Active:</strong> This output is not committed to any ledger atau proof system. 
            Use for testing dan development purposes only.
          </div>
        </div>
      </div>
    </div>
  );
}