# SKILL: videogen.storyboard.v1

## Overview
Generates detailed video storyboards with scene-by-scene breakdowns, shot specifications, motion concepts, and production notes. Optimized for marketing videos, explainers, product demos, and brand content.

## Input Schema
```json
{
  "video_title": "string (required)",
  "video_type": "enum: explainer|product_demo|brand_story|testimonial|social_ad (required)",
  "duration": "number (required, in seconds)",
  "message": "string (required)",
  "target_audience": "string (required)",
  "tone": "enum: professional|energetic|emotional|playful|cinematic (required)",
  "brand_identity": {
    "colors": "array<string> (optional)",
    "style": "string (optional)",
    "logo_url": "string (optional)"
  },
  "key_points": "array<string> (required)",
  "call_to_action": "string (optional)",
  "music_style": "string (optional)",
  "voiceover": "boolean (optional, default: true)",
  "platform": "enum: youtube|instagram|tiktok|linkedin|website (optional)"
}
```

## Output Schema
```json
{
  "storyboard": {
    "title": "string",
    "total_duration": "number",
    "total_scenes": "number",
    "scenes": [
      {
        "scene_number": "number",
        "duration": "number",
        "timecode": "string",
        "shot_type": "string",
        "visual_description": "string",
        "motion": {
          "camera_movement": "string",
          "subject_movement": "string",
          "transitions": "string"
        },
        "audio": {
          "voiceover": "string (optional)",
          "music": "string",
          "sound_effects": "array<string> (optional)"
        },
        "text_overlays": "array<object> (optional)",
        "color_grading": "string",
        "key_frame_notes": "string"
      }
    ],
    "opening": {
      "hook": "string",
      "duration": "number"
    },
    "closing": {
      "cta": "string",
      "duration": "number"
    }
  },
  "production_notes": {
    "equipment": "array<string>",
    "locations": "array<string>",
    "talent": "array<string>",
    "props": "array<string>",
    "estimated_shoot_time": "string"
  },
  "technical_specs": {
    "aspect_ratio": "string",
    "resolution": "string",
    "frame_rate": "string",
    "format": "string"
  },
  "metadata": {
    "generated_at": "timestamp",
    "version": "string"
  }
}
```

## Logic Breakdown

### Step 1: Video Structure Planning
- Analyze video_type and duration to determine pacing
- Calculate optimal scene count (3-5 second average per scene)
- Define narrative arc: hook → build → climax → resolution → CTA
- Allocate time per section based on message priority

### Step 2: Scene Breakdown
- Create opening hook (3-5 seconds) to capture attention
- Distribute key_points across middle scenes
- Build emotional or logical progression
- Design closing with strong CTA (5-8 seconds)

### Step 3: Visual Concept Development
- Define shot types (wide, medium, close-up, detail)
- Conceptualize camera movements (pan, tilt, zoom, dolly, static)
- Design transitions (cut, fade, wipe, morph)
- Apply brand visual style and color grading

### Step 4: Motion Choreography
- Plan camera movements for dynamic energy
- Coordinate subject movements with message beats
- Time transitions to music or voiceover rhythm
- Create visual variety while maintaining coherence

### Step 5: Audio Design
- Write voiceover script with natural pacing
- Recommend music style and tempo
- Suggest sound effects for emphasis
- Sync audio beats with visual transitions

### Step 6: Text & Graphics
- Design text overlays for key messages
- Specify animation styles (fade, slide, scale)
- Ensure readability (font size, contrast, duration)
- Integrate brand elements (logo, colors)

### Step 7: Production Planning
- List required equipment and locations
- Identify talent and props needed
- Estimate shoot time and complexity
- Provide technical specifications

## Constraints
- Scene duration: 2-10 seconds each
- Total scenes: 5-30 depending on video length
- Text overlay duration: minimum 2 seconds for readability
- Voiceover pace: 150-160 words per minute
- Opening hook: must capture attention in first 3 seconds
- CTA: must be clear and visible for minimum 3 seconds
- Aspect ratio: platform-specific (16:9, 9:16, 1:1, 4:5)
- File format: MP4 or MOV
- Resolution: minimum 1080p

## Performance Criteria
- Generation time: < 10 seconds
- Narrative flow score: > 8/10
- Visual variety score: > 7/10
- Message clarity: > 9/10
- Production feasibility: > 7/10

## Dependencies
- Shot type library
- Camera movement database
- Transition effects catalog
- Music style taxonomy
- Platform specification database
- Voiceover pacing calculator

## Version
1.0.0

## Status
LAB - Ready for testing and validation
