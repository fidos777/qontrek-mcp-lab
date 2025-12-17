// KuasaTurbo Frontend Constants

export const CREATIVE_TASKS = [
  { id: "thumbnail", label: "Thumbnail Generator" },
  { id: "product_render", label: "Product Render" },
  { id: "story_infographic", label: "Story Infographic" },
  { id: "car_visualizer", label: "Car Visualizer" },
  { id: "image_cleanup", label: "Image Cleanup" },
];

export const CREATIVE_STYLES = [
  {
    id: "energetic",
    label: "Energetic",
    description: "Bold, high-contrast, motion-focused",
  },
  {
    id: "premium",
    label: "Premium",
    description: "Elegant, sophisticated, showroom quality",
  },
  {
    id: "simple_clean",
    label: "Simple Clean",
    description: "Minimal, flat, easy to read",
  },
  {
    id: "modern",
    label: "Modern",
    description: "Geometric, gradient, glass morphism",
  },
  {
    id: "vibrant",
    label: "Vibrant",
    description: "High saturation, colorful, eye-catching",
  },
];

export const VERTICALS = [
  {
    slug: "automotive",
    name: "Automotive",
    status: "available" as const,
    description: "Trade-in, loan check, lead intake untuk showroom kereta",
  },
  {
    slug: "solar",
    name: "Solar",
    status: "coming_soon" as const,
    description: "ROI calculator, proposal generator untuk solar installation",
  },
  {
    slug: "takaful",
    name: "Takaful",
    status: "coming_soon" as const,
    description: "Coverage calculator, policy comparison untuk insurance",
  },
  {
    slug: "property",
    name: "Property",
    status: "coming_soon" as const,
    description: "Mortgage calculator, property valuation untuk real estate",
  },
  {
    slug: "fnb",
    name: "F&B",
    status: "available" as const,
    description: "Menu update, promo generator untuk restaurant",
  },
];
