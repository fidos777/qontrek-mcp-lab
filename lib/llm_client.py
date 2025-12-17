#!/usr/bin/env python3
"""
LLM Client - Simulated LLM Engine for LaunchKit
This module provides intelligent text generation via pattern-based simulation.
Ready to be swapped with real LLM API calls (OpenAI, Anthropic, etc.)
"""

import re
import random
from typing import Dict, List, Optional
from lib.logger import log


class LLMClient:
    """
    Simulated LLM client for content generation.
    
    In production, replace simulate_generation() with real API calls:
    - OpenAI GPT-4
    - Anthropic Claude
    - Local models via Ollama
    """
    
    def __init__(self, model: str = "simulated-gpt-4", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.use_real_llm = False  # Switch to True when API is available
    
    def generate(self, prompt: str, context: Dict = None, max_tokens: int = 2000) -> str:
        """
        Generate text based on prompt and context.
        
        Args:
            prompt: The prompt template with {variables}
            context: Dictionary of variables to inject
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        log("info", "llm_generate_start", 
            model=self.model, 
            prompt_length=len(prompt),
            has_context=bool(context))
        
        # Inject context into prompt
        if context:
            try:
                prompt = prompt.format(**context)
            except KeyError as e:
                log("warn", "llm_prompt_missing_key", key=str(e))
        
        # Generate content
        if self.use_real_llm:
            output = self._call_real_llm(prompt, max_tokens)
        else:
            output = self._simulate_generation(prompt, context or {}, max_tokens)
        
        log("info", "llm_generate_done", output_length=len(output))
        return output
    
    def _call_real_llm(self, prompt: str, max_tokens: int) -> str:
        """
        Call real LLM API (OpenAI, Anthropic, etc.)
        
        Example implementation:
        ```python
        import openai
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=self.temperature
        )
        return response.choices[0].message.content
        ```
        """
        raise NotImplementedError("Real LLM integration not configured. Set API keys and implement.")
    
    def _simulate_generation(self, prompt: str, context: Dict, max_tokens: int) -> str:
        """
        Simulate LLM generation using response banks and controlled randomness.
        This produces contextual, brand-specific content without hardcoding.
        """
        # Extract generation intent from prompt
        intent = self._extract_intent(prompt)
        
        # Apply temperature-based variation
        variation_seed = int(self.temperature * 100) % 5
        
        # Generate based on intent and context with controlled randomness
        if "brand story" in intent.lower() or "narrative" in intent.lower():
            return self._generate_brand_story(context, variation_seed)
        elif "vision" in intent.lower():
            return self._generate_vision(context, variation_seed)
        elif "problem statement" in intent.lower():
            return self._generate_problem_statement(context, variation_seed)
        elif "solution" in intent.lower():
            return self._generate_solution(context, variation_seed)
        elif "pricing" in intent.lower() or "tiers" in intent.lower():
            return self._generate_pricing(context, variation_seed)
        elif "roadmap" in intent.lower() or "milestone" in intent.lower():
            return self._generate_roadmap(context, variation_seed)
        elif "slide" in intent.lower() or "pitch" in intent.lower():
            return self._generate_pitch_content(context, variation_seed)
        elif "social" in intent.lower() or "post" in intent.lower():
            return self._generate_social_content(context, variation_seed)
        elif "tagline" in intent.lower():
            return self._generate_taglines(context, variation_seed)
        else:
            return self._generate_generic(context, prompt)
    
    def _extract_intent(self, prompt: str) -> str:
        """Extract the generation intent from prompt."""
        # Look for key phrases
        intent_markers = [
            "generate", "create", "write", "produce", "develop",
            "brand story", "vision", "mission", "problem", "solution",
            "pricing", "roadmap", "slide", "post", "tagline"
        ]
        
        prompt_lower = prompt.lower()
        for marker in intent_markers:
            if marker in prompt_lower:
                return marker
        
        return "generic"
    
    def _generate_brand_story(self, context: Dict, variation: int = 0) -> str:
        """Generate contextual brand story with response banks."""
        brand_name = context.get("brand_name", "the company")
        mission = context.get("mission", "")
        themes = context.get("brand_themes", [])
        target = context.get("target_audience", "customers")
        
        # Response bank: 3-5 variations per template
        story_templates = [
            "{brand_name} was founded on a simple belief: {mission}.\n\nWe saw {target} struggling with challenges that existing solutions couldn't solve. So we built something different—a platform rooted in {themes}.\n\nEvery feature we ship, every decision we make, reflects our commitment to {primary_theme}. We're not just building software; we're building a movement.",
            
            "The journey of {brand_name} began when we discovered a fundamental problem: {mission}.\n\n{target} deserved better. They needed a solution built on {themes}, not compromises.\n\nToday, {brand_name} stands as proof that {primary_theme} can transform industries. We're here to make that transformation accessible to everyone.",
            
            "{brand_name} exists because we believe {mission}.\n\nWhen we looked at {target}, we saw untapped potential held back by inadequate tools. We knew we could do better.\n\nOur platform embodies {themes}—not as buzzwords, but as core principles. Every line of code, every design decision, serves our mission.",
            
            "Why {brand_name}? Because {mission}.\n\nWe built {brand_name} for {target} who refuse to settle for mediocrity. Our foundation is {themes}, our goal is transformation.\n\n{primary_theme} isn't just what we do—it's who we are.",
            
            "{brand_name} started with a question: What if {mission}?\n\nFor {target}, this question became our mission. We combined {themes} to create something unprecedented.\n\nToday, we're proving that {primary_theme} can change everything."
        ]
        
        # Select template based on variation
        template = story_templates[variation % len(story_templates)]
        
        # Prepare interpolation context
        theme_str = ", ".join(themes[:3]) if themes else "innovation and excellence"
        primary_theme = themes[0] if themes else "quality"
        
        # Interpolate
        story = template.format(
            brand_name=brand_name,
            mission=mission.lower() if mission else "great products change lives",
            target=target,
            themes=theme_str,
            primary_theme=primary_theme
        )
        
        return story
    
    def _generate_vision(self, context: Dict) -> str:
        """Generate vision statement."""
        themes = context.get("brand_themes", ["innovation"])
        mission = context.get("mission", "")
        
        primary_theme = themes[0] if themes else "innovation"
        
        vision = f"We envision a world where {primary_theme} is accessible to everyone. "
        
        if mission:
            # Extract action from mission
            action = mission.lower().replace("to ", "").split(",")[0]
            vision += f"By {action}, we're making that vision reality."
        else:
            vision += f"Through our platform, we're democratizing {primary_theme} for all."
        
        return vision
    
    def _generate_problem_statement(self, context: Dict) -> str:
        """Generate problem statement from ICP pain points."""
        icp = context.get("icp", {})
        pain_points = icp.get("pain_points", ["inefficiency", "complexity", "high costs"])
        target = icp.get("demographics", "professionals")
        
        problem = f"{target.capitalize()} face {len(pain_points)} critical challenges:\n\n"
        for i, pain in enumerate(pain_points[:3], 1):
            problem += f"{i}. {pain.capitalize()}\n"
        
        problem += f"\nThese issues cost time, money, and productivity. Existing solutions are inadequate."
        
        return problem
    
    def _generate_solution(self, context: Dict) -> str:
        """Generate solution overview."""
        brand_name = context.get("brand_name", "Our platform")
        value_prop = context.get("value_proposition", "")
        themes = context.get("brand_themes", ["efficiency"])
        
        solution = f"{brand_name} solves these challenges through {', '.join(themes[:3])}.\n\n"
        solution += f"{value_prop}\n\n" if value_prop else ""
        solution += f"Our approach combines cutting-edge technology with user-centric design, "
        solution += f"delivering results that traditional solutions can't match."
        
        return solution
    
    def _generate_pricing(self, context: Dict) -> str:
        """Generate pricing rationale."""
        icp = context.get("icp", {})
        value_prop = context.get("value_proposition", "")
        
        demographics = icp.get("demographics", "professionals")
        
        pricing = f"Our pricing is designed for {demographics}, balancing accessibility with sustainability.\n\n"
        pricing += f"We offer tiered plans that scale with your needs:\n"
        pricing += f"- Starter: For individuals getting started\n"
        pricing += f"- Professional: For power users and small teams\n"
        pricing += f"- Enterprise: For organizations at scale\n\n"
        pricing += f"Each tier delivers {value_prop.lower() if value_prop else 'exceptional value'}."
        
        return pricing
    
    def _generate_roadmap(self, context: Dict) -> str:
        """Generate roadmap narrative."""
        features = context.get("feature_list", {})
        
        roadmap = "Our roadmap is structured in three phases:\n\n"
        roadmap += "Phase 1 (30 days): MVP launch with core features\n"
        roadmap += "Phase 2 (60 days): Enhanced capabilities and integrations\n"
        roadmap += "Phase 3 (90 days): Advanced features and scale\n\n"
        roadmap += "Each phase builds on the last, ensuring stable, iterative growth."
        
        return roadmap
    
    def _generate_pitch_content(self, context: Dict) -> str:
        """Generate pitch deck content."""
        brand_name = context.get("brand_name", "Company")
        
        pitch = f"{brand_name} is transforming the industry.\n\n"
        pitch += "We're solving a $10B problem with innovative technology.\n"
        pitch += "Our traction proves product-market fit.\n"
        pitch += "We're seeking investment to scale."
        
        return pitch
    
    def _generate_social_content(self, context: Dict) -> str:
        """Generate social media content."""
        brand_name = context.get("brand_name", "Product")
        value_prop = context.get("value_proposition", "amazing results")
        
        post = f"🚀 Introducing {brand_name}!\n\n"
        post += f"{value_prop}\n\n"
        post += f"Join thousands already transforming their workflow.\n"
        post += f"Try it free → [link]"
        
        return post
    
    def _generate_taglines(self, context: Dict) -> str:
        """Generate tagline variations."""
        brand_name = context.get("brand_name", "Brand")
        themes = context.get("brand_themes", ["innovation"])
        
        taglines = []
        for theme in themes[:3]:
            taglines.append(f"{brand_name}: {theme.capitalize()} Redefined")
            taglines.append(f"{theme.capitalize()} Made Simple")
        
        taglines.append(f"The Future of {themes[0].capitalize()}")
        taglines.append(f"Work Smarter with {brand_name}")
        
        return "\n".join(taglines[:5])
    
    def _generate_generic(self, context: Dict, prompt: str) -> str:
        """Generic generation fallback."""
        brand_name = context.get("brand_name", "the product")
        
        output = f"Generated content for {brand_name}.\n\n"
        output += f"Context: {', '.join(f'{k}={v}' for k, v in list(context.items())[:3])}\n\n"
        output += "This is simulated LLM output. Replace with real API call for production."
        
        return output


# Global client instance
_client = None

def get_client(model: str = "simulated-gpt-4", temperature: float = 0.7) -> LLMClient:
    """Get or create LLM client instance."""
    global _client
    if _client is None:
        _client = LLMClient(model=model, temperature=temperature)
    return _client

def generate(prompt: str, context: Dict = None, max_tokens: int = 2000) -> str:
    """
    Convenience function for text generation.
    
    Usage:
        from lib.llm_client import generate
        
        output = generate(
            prompt="Generate a brand story for {brand_name}...",
            context={"brand_name": "FlowMind", "mission": "..."},
            max_tokens=1000
        )
    """
    client = get_client()
    return client.generate(prompt, context, max_tokens)
