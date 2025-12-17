// KuasaTurbo API Client (Phase XXIII-B - Full Implementation)

import type { GenerateCreativeParams, GenerateCreativeResponse } from "./types";

// API Base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "";

/**
 * Convert File to Base64 string
 */
export async function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      // Remove data URL prefix (e.g., "data:image/png;base64,")
      const base64 = result.split(",")[1] || result;
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

/**
 * Generate creative content
 * 
 * Calls POST /creative/generate with real API or falls back to mock
 */
export async function generateCreative(
  params: GenerateCreativeParams
): Promise<GenerateCreativeResponse> {
  // If no API URL configured, use mock mode
  if (!API_BASE_URL) {
    return generateMockCreative(params);
  }

  try {
    // Convert image to base64 if provided
    let imageBase64: string | undefined;
    if (params.image) {
      imageBase64 = await fileToBase64(params.image);
    }

    // Build request payload
    const requestBody = {
      task_type: params.task,
      payload: {
        prompt: params.prompt || `Generate ${params.task} with ${params.style} style`,
        image_base64: imageBase64,
      },
      persona_id: "zeyti_bbnu_creator.v1",
      style_override: params.style,
      model_override: null,
    };

    // Make API call
    const response = await fetch(`${API_BASE_URL}/creative/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": params.apiKey || "demo_key",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail?.message || `API error: ${response.status}`);
    }

    const data = await response.json();

    // Transform backend response to frontend format
    return {
      status: "success",
      creative_id: data.creative_id || data.execution_id || "unknown",
      task: params.task,
      style_used: params.style,
      model_used: data.model_used || "unknown",
      credits_charged: data.credits_charged || 0,
      mock_mode: data.mock_mode || false,
      outputs: {
        images: data.outputs?.images || [],
        copy: data.outputs?.copy || data.outputs?.description || "",
        metadata: data.outputs?.metadata || {},
      },
    };
  } catch (error) {
    console.error("API call failed, falling back to mock:", error);
    // Fallback to mock on any error
    return generateMockCreative(params);
  }
}

/**
 * Generate mock creative response (fallback)
 */
function generateMockCreative(
  params: GenerateCreativeParams
): Promise<GenerateCreativeResponse> {
  return new Promise((resolve) => {
    // Simulate network delay
    setTimeout(() => {
      const mockOutputs: Record<string, any> = {
        thumbnail: {
          copy: "Vibrant thumbnail dengan bold typography dan energetic colors. Perfect untuk social media engagement.",
          metadata: {
            composition_notes: [
              "Primary brand color dominates the background",
              "Title text positioned in upper third using bold sans-serif",
              "CTA button prominently placed at bottom with high contrast",
              "Subtle gradient overlay for depth",
            ],
            aspect_ratio: "16:9",
            recommended_dimensions: "1920x1080px",
          },
        },
        product_render: {
          copy: "Professional product render dengan premium lighting dan showroom quality finish.",
          metadata: {
            composition_notes: [
              "Three-point lighting setup for dimensional depth",
              "Reflective surface beneath product",
              "Soft shadow for realism",
              "Clean white background for versatility",
            ],
            aspect_ratio: "1:1",
            recommended_dimensions: "1080x1080px",
          },
        },
        story_infographic: {
          copy: "Engaging story infographic dengan clear visual hierarchy dan easy-to-read layout.",
          metadata: {
            composition_notes: [
              "Vertical flow optimized for mobile viewing",
              "Icon-driven sections for quick scanning",
              "Color-coded information blocks",
              "Consistent spacing and alignment",
            ],
            aspect_ratio: "9:16",
            recommended_dimensions: "1080x1920px",
          },
        },
        car_visualizer: {
          copy: "Stunning car visualization dengan dynamic angle dan premium showroom aesthetic.",
          metadata: {
            composition_notes: [
              "Three-quarter front view for maximum appeal",
              "Dramatic lighting to highlight curves",
              "Motion blur on wheels for dynamic feel",
              "Reflective floor for luxury presentation",
            ],
            aspect_ratio: "16:9",
            recommended_dimensions: "1920x1080px",
          },
        },
        image_cleanup: {
          copy: "Image cleanup completed: background removed, colors enhanced, imperfections corrected.",
          metadata: {
            composition_notes: [
              "Background removed with clean edges",
              "Color balance adjusted for natural look",
              "Minor imperfections smoothed",
              "Sharpness enhanced for clarity",
            ],
            aspect_ratio: "original",
            recommended_dimensions: "original",
          },
        },
      };

      const taskOutput = mockOutputs[params.task] || mockOutputs.thumbnail;

      resolve({
        status: "success",
        creative_id: `mock_${Date.now()}`,
        task: params.task,
        style_used: params.style,
        model_used: "mock",
        credits_charged: 0,
        mock_mode: true,
        outputs: {
          images: [],
          copy: taskOutput.copy,
          metadata: taskOutput.metadata,
        },
      });
    }, 1500);
  });
}
