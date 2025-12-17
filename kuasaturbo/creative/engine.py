"""
KuasaTurbo Creative Engine

Orchestrates creative task execution with style profiles, templates, and model routing.
All operations run in MOCK MODE (no external API calls, no file writes).
"""

import yaml
import os
import importlib
from typing import Dict, Any, Optional
from pathlib import Path


# Get project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_style_profile(style_id: str) -> Dict[str, Any]:
    """
    Load visual style profile
    
    Args:
        style_id: Style identifier (e.g., "energetic", "premium")
    
    Returns:
        Style configuration dict
    """
    styles_path = PROJECT_ROOT / "kuasaturbo" / "creative" / "presets" / "styles.yaml"
    
    if not styles_path.exists():
        raise FileNotFoundError(f"Styles file not found: {styles_path}")
    
    with open(styles_path, 'r') as f:
        styles = yaml.safe_load(f)
    
    if style_id not in styles:
        raise ValueError(f"Style '{style_id}' not found in styles.yaml")
    
    return styles[style_id]


def load_template(task_type: str) -> Dict[str, Any]:
    """
    Load task template configuration
    
    Args:
        task_type: Task type (e.g., "thumbnail", "product_render")
    
    Returns:
        Template configuration dict
    """
    templates_path = PROJECT_ROOT / "kuasaturbo" / "creative" / "presets" / "templates.yaml"
    
    if not templates_path.exists():
        raise FileNotFoundError(f"Templates file not found: {templates_path}")
    
    with open(templates_path, 'r') as f:
        templates = yaml.safe_load(f)
    
    if task_type not in templates:
        raise ValueError(f"Template for task '{task_type}' not found")
    
    return templates[task_type]


def load_prompt_preset(task_type: str) -> str:
    """
    Load prompt template for task type
    
    Args:
        task_type: Task type (e.g., "thumbnail", "product_render")
    
    Returns:
        Prompt template string
    """
    prompt_path = PROJECT_ROOT / "kuasaturbo" / "creative" / "presets" / "prompts" / f"{task_type}.txt"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r') as f:
        return f.read()


def resolve_creative_task(task_type: str) -> Dict[str, Any]:
    """
    Resolve task configuration from creative_tasks.yaml
    
    Args:
        task_type: Task type identifier
    
    Returns:
        Task configuration dict
    """
    config_path = PROJECT_ROOT / "config" / "creative_tasks.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Creative tasks config not found: {config_path}")
    
    with open(config_path, 'r') as f:
        tasks = yaml.safe_load(f)
    
    if task_type not in tasks:
        raise ValueError(f"Task type '{task_type}' not found in creative_tasks.yaml")
    
    return tasks[task_type]


def route_to_model(task_config: Dict[str, Any], model_override: Optional[str] = None) -> str:
    """
    Determine which model to use for creative task
    
    Args:
        task_config: Task configuration from creative_tasks.yaml
        model_override: Optional explicit model override
    
    Returns:
        Model identifier
    """
    # Priority 1: Explicit override
    if model_override:
        return model_override
    
    # Priority 2: Task preferred model
    if 'preferred_model' in task_config:
        return task_config['preferred_model']
    
    # Priority 3: Default to mock
    return "mock"


def build_creative_prompt(
    task_type: str,
    payload: dict,
    style_profile: dict,
    brand_profile: Optional[dict] = None
) -> str:
    """
    Build creative prompt from template and inputs
    
    Args:
        task_type: Task type identifier
        payload: Input data
        style_profile: Visual style configuration
        brand_profile: Optional brand profile
    
    Returns:
        Formatted prompt string
    """
    # Load prompt template
    prompt_template = load_prompt_preset(task_type)
    
    # Prepare substitution values
    values = {
        'style_name': style_profile.get('name', 'default'),
        **payload
    }
    
    # Add brand info if available
    if brand_profile:
        values['brand_name'] = brand_profile.get('name', 'Unknown Brand')
        values['brand_colors'] = ', '.join(brand_profile.get('colors', []))
    
    # Format prompt
    try:
        formatted_prompt = prompt_template.format(**values)
    except KeyError as e:
        # Missing key in template, return template with available values
        formatted_prompt = prompt_template
        for key, value in values.items():
            formatted_prompt = formatted_prompt.replace(f'{{{key}}}', str(value))
    
    return formatted_prompt


def execute_generation(
    task_type: str,
    payload: dict,
    persona: dict,
    brand_profile: Optional[dict] = None,
    style_override: Optional[str] = None,
    model_override: Optional[str] = None,
    mock_mode: bool = True
) -> Dict[str, Any]:
    """
    Execute creative generation task (MOCK MODE)
    
    Args:
        task_type: Task type (thumbnail, product_render, etc.)
        payload: Input data for the task
        persona: Persona definition
        brand_profile: Optional brand profile
        style_override: Optional style override
        model_override: Optional model override
        mock_mode: Always True for Phase XIII
    
    Returns:
        Generated creative output (mock)
    """
    print(f"[CreativeEngine] Executing task: {task_type}")
    
    # Resolve task configuration
    task_config = resolve_creative_task(task_type)
    
    # Load template
    template = load_template(task_type)
    
    # Determine style
    style_id = style_override or task_config.get('default_style', 'simple_clean')
    style_profile = load_style_profile(style_id)
    
    # Route to model
    model = route_to_model(task_config, model_override)
    
    # Build prompt (for reference, not used in mock mode)
    prompt = build_creative_prompt(task_type, payload, style_profile, brand_profile)
    
    print(f"[CreativeEngine] Style: {style_id}, Model: {model}")
    
    # Load and execute task module
    module_path = task_config['module']
    function_name = task_config['function']
    
    try:
        # Import task module dynamically
        module = importlib.import_module(module_path)
        task_function = getattr(module, function_name)
        
        # Execute task
        result = task_function(
            payload=payload,
            persona=persona,
            brand_profile=brand_profile,
            style_profile=style_profile,
            model=model,
            mock_mode=mock_mode
        )
        
        # Add metadata
        result['metadata'] = {
            'task_type': task_type,
            'style': style_id,
            'model': model,
            'mock_mode': mock_mode,
            'persona': persona.get('persona_name', 'unknown')
        }
        
        return result
        
    except Exception as e:
        print(f"[CreativeEngine] Error executing task: {str(e)}")
        return {
            'error': str(e),
            'task_type': task_type,
            'status': 'failed'
        }


def get_available_tasks() -> list:
    """
    Get list of available creative tasks
    
    Returns:
        List of task type identifiers
    """
    config_path = PROJECT_ROOT / "config" / "creative_tasks.yaml"
    
    if not config_path.exists():
        return []
    
    with open(config_path, 'r') as f:
        tasks = yaml.safe_load(f)
    
    return list(tasks.keys())


def get_available_styles() -> list:
    """
    Get list of available visual styles
    
    Returns:
        List of style identifiers
    """
    styles_path = PROJECT_ROOT / "kuasaturbo" / "creative" / "presets" / "styles.yaml"
    
    if not styles_path.exists():
        return []
    
    with open(styles_path, 'r') as f:
        styles = yaml.safe_load(f)
    
    return list(styles.keys())
