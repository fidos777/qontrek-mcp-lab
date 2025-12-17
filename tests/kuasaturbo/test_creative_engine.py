#!/usr/bin/env python3
"""
Test Suite: KuasaTurbo Creative Engine

Tests all creative tasks, engine orchestration, and integration.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.creative import engine
from kuasaturbo.creative.tasks import thumbnail, product_render, story_infographic, car_visualizer, image_cleanup


def test_load_style_profile():
    """Test loading style profiles"""
    print("\n[TEST] Loading style profiles...")
    
    # Test valid styles
    styles = ['energetic', 'premium', 'simple_clean', 'modern', 'vibrant']
    for style_id in styles:
        style = engine.load_style_profile(style_id)
        assert 'name' in style, f"Style {style_id} missing 'name'"
        assert 'colors' in style, f"Style {style_id} missing 'colors'"
        assert isinstance(style['colors'], list), f"Style {style_id} colors must be list"
        print(f"  ✓ Style '{style_id}' loaded: {len(style['colors'])} colors")
    
    # Test invalid style
    try:
        engine.load_style_profile('nonexistent')
        assert False, "Should raise ValueError for invalid style"
    except ValueError:
        print("  ✓ Invalid style raises ValueError")
    
    print("✓ Style profile loading works")


def test_load_template():
    """Test loading task templates"""
    print("\n[TEST] Loading task templates...")
    
    # Test valid templates
    tasks = ['thumbnail', 'product_render', 'story_infographic', 'car_visualizer', 'image_cleanup']
    for task_type in tasks:
        template = engine.load_template(task_type)
        assert 'default_style' in template, f"Template {task_type} missing 'default_style'"
        print(f"  ✓ Template '{task_type}' loaded: style={template['default_style']}")
    
    # Test invalid template
    try:
        engine.load_template('nonexistent')
        assert False, "Should raise ValueError for invalid template"
    except ValueError:
        print("  ✓ Invalid template raises ValueError")
    
    print("✓ Template loading works")


def test_load_prompt_preset():
    """Test loading prompt presets"""
    print("\n[TEST] Loading prompt presets...")
    
    tasks = ['thumbnail', 'product_render', 'infographic', 'car_visualizer', 'image_cleanup']
    for task_type in tasks:
        prompt = engine.load_prompt_preset(task_type)
        assert isinstance(prompt, str), f"Prompt for {task_type} must be string"
        assert len(prompt) > 0, f"Prompt for {task_type} is empty"
        print(f"  ✓ Prompt '{task_type}' loaded: {len(prompt)} chars")
    
    print("✓ Prompt preset loading works")


def test_resolve_creative_task():
    """Test resolving task configuration"""
    print("\n[TEST] Resolving creative tasks...")
    
    tasks = ['thumbnail', 'product_render', 'story_infographic', 'car_visualizer', 'image_cleanup']
    for task_type in tasks:
        config = engine.resolve_creative_task(task_type)
        assert 'task_type' in config, f"Config for {task_type} missing 'task_type'"
        assert 'module' in config, f"Config for {task_type} missing 'module'"
        assert 'function' in config, f"Config for {task_type} missing 'function'"
        assert 'preferred_model' in config, f"Config for {task_type} missing 'preferred_model'"
        print(f"  ✓ Task '{task_type}' resolved: model={config['preferred_model']}")
    
    print("✓ Task resolution works")


def test_route_to_model():
    """Test model routing logic"""
    print("\n[TEST] Testing model routing...")
    
    task_config = {
        'preferred_model': 'gemini-3.0'
    }
    
    # Test with override
    model = engine.route_to_model(task_config, model_override='chatgpt-5.1')
    assert model == 'chatgpt-5.1', "Override should take priority"
    print("  ✓ Model override works")
    
    # Test without override
    model = engine.route_to_model(task_config)
    assert model == 'gemini-3.0', "Should use task preferred model"
    print("  ✓ Task preferred model works")
    
    # Test with no preferred model
    model = engine.route_to_model({})
    assert model == 'mock', "Should default to mock"
    print("  ✓ Default model fallback works")
    
    print("✓ Model routing works")


def test_build_creative_prompt():
    """Test prompt building"""
    print("\n[TEST] Building creative prompts...")
    
    payload = {
        'title': 'Test Video',
        'mood': 'energetic',
        'platform': 'youtube'
    }
    
    style_profile = {
        'name': 'energetic',
        'colors': ['#FE4800', '#262A3B']
    }
    
    prompt = engine.build_creative_prompt('thumbnail', payload, style_profile)
    assert isinstance(prompt, str), "Prompt must be string"
    assert len(prompt) > 0, "Prompt must not be empty"
    assert 'energetic' in prompt.lower(), "Prompt should contain style name"
    print(f"  ✓ Prompt built: {len(prompt)} chars")
    
    print("✓ Prompt building works")


def test_thumbnail_task():
    """Test thumbnail generation task"""
    print("\n[TEST] Testing thumbnail task...")
    
    payload = {
        'title': 'Amazing AI Tutorial',
        'mood': 'energetic',
        'platform': 'youtube',
        'variation_count': 3
    }
    
    persona = {'persona_name': 'Zeyti'}
    style_profile = engine.load_style_profile('energetic')
    
    result = thumbnail.run(payload, persona, None, style_profile, 'gemini-3.0', mock_mode=True)
    
    assert 'images' in result, "Result must contain 'images'"
    assert len(result['images']) == 3, "Should generate 3 variations"
    assert 'debug' in result, "Result must contain 'debug'"
    
    for img in result['images']:
        assert 'variation_id' in img
        assert 'headline_text' in img
        assert 'dominant_colors' in img
        print(f"  ✓ Thumbnail variation: {img['variation_id']}")
    
    print("✓ Thumbnail task works")


def test_product_render_task():
    """Test product render task"""
    print("\n[TEST] Testing product render task...")
    
    payload = {
        'image': 'fake://product_01',
        'angles': ['front', 'side', 'three_quarter'],
        'background': 'showroom'
    }
    
    persona = {'persona_name': 'Jordan'}
    style_profile = engine.load_style_profile('premium')
    
    result = product_render.run(payload, persona, None, style_profile, 'gemini-3.0', mock_mode=True)
    
    assert 'images' in result, "Result must contain 'images'"
    assert len(result['images']) == 3, "Should generate 3 angles"
    
    for img in result['images']:
        assert 'angle' in img
        assert 'background_style' in img
        print(f"  ✓ Product shot: {img['angle']}")
    
    print("✓ Product render task works")


def test_story_infographic_task():
    """Test story infographic task"""
    print("\n[TEST] Testing story infographic task...")
    
    payload = {
        'story_points': [
            'AI saves time',
            'Automate tasks',
            'Focus on growth'
        ],
        'title': 'AI Benefits'
    }
    
    persona = {'persona_name': 'Raya'}
    style_profile = engine.load_style_profile('simple_clean')
    
    result = story_infographic.run(payload, persona, None, style_profile, 'chatgpt-5.1', mock_mode=True)
    
    assert 'image' in result, "Result must contain 'image'"
    assert 'sections' in result['image']
    assert len(result['image']['sections']) == 3, "Should have 3 sections"
    
    print(f"  ✓ Infographic: {result['image']['title']}")
    print("✓ Story infographic task works")


def test_car_visualizer_task():
    """Test car visualizer task"""
    print("\n[TEST] Testing car visualizer task...")
    
    payload = {
        'car_model': 'Proton X70',
        'scenario': 'premium-night',
        'effects': ['deep_shadow', 'bokeh_lights']
    }
    
    persona = {'persona_name': 'Tawfiq'}
    style_profile = engine.load_style_profile('premium')
    
    result = car_visualizer.run(payload, persona, None, style_profile, 'gemini-3.0', mock_mode=True)
    
    assert 'image' in result, "Result must contain 'image'"
    assert 'scenario' in result['image']
    assert result['image']['scenario'] == 'premium-night'
    
    print(f"  ✓ Car visualization: {result['image']['car_model']}")
    print("✓ Car visualizer task works")


def test_image_cleanup_task():
    """Test image cleanup task"""
    print("\n[TEST] Testing image cleanup task...")
    
    payload = {
        'image': 'fake://messy_image_01',
        'mode': 'full-clean',
        'output_format': 'png'
    }
    
    persona = {'persona_name': 'Izzara'}
    style_profile = engine.load_style_profile('simple_clean')
    
    result = image_cleanup.run(payload, persona, None, style_profile, 'chatgpt-5.1', mock_mode=True)
    
    assert 'image' in result, "Result must contain 'image'"
    assert result['image']['cleanup_mode'] == 'full-clean'
    assert result['image']['background'] == 'transparent'
    assert len(result['image']['artifacts_fixed']) > 0
    
    print(f"  ✓ Image cleanup: {result['image']['cleanup_mode']}")
    print("✓ Image cleanup task works")


def test_execute_generation():
    """Test full generation execution"""
    print("\n[TEST] Testing full generation execution...")
    
    # Test thumbnail generation
    payload = {
        'title': 'Test Video',
        'mood': 'energetic',
        'platform': 'youtube',
        'variation_count': 2
    }
    
    persona = {
        'persona_name': 'Zeyti',
        'role': 'BBNU Creator'
    }
    
    result = engine.execute_generation(
        task_type='thumbnail',
        payload=payload,
        persona=persona,
        mock_mode=True
    )
    
    assert 'images' in result, "Result must contain 'images'"
    assert 'metadata' in result, "Result must contain 'metadata'"
    assert result['metadata']['task_type'] == 'thumbnail'
    assert result['metadata']['mock_mode'] is True
    
    print(f"  ✓ Generated {len(result['images'])} thumbnails")
    print("✓ Full generation execution works")


def test_get_available_tasks():
    """Test getting available tasks"""
    print("\n[TEST] Getting available tasks...")
    
    tasks = engine.get_available_tasks()
    assert isinstance(tasks, list), "Tasks must be a list"
    assert len(tasks) == 5, "Should have 5 tasks"
    assert 'thumbnail' in tasks
    assert 'product_render' in tasks
    assert 'story_infographic' in tasks
    assert 'car_visualizer' in tasks
    assert 'image_cleanup' in tasks
    
    print(f"  ✓ Found {len(tasks)} tasks: {', '.join(tasks)}")
    print("✓ Available tasks retrieval works")


def test_get_available_styles():
    """Test getting available styles"""
    print("\n[TEST] Getting available styles...")
    
    styles = engine.get_available_styles()
    assert isinstance(styles, list), "Styles must be a list"
    assert len(styles) == 5, "Should have 5 styles"
    assert 'energetic' in styles
    assert 'premium' in styles
    assert 'simple_clean' in styles
    
    print(f"  ✓ Found {len(styles)} styles: {', '.join(styles)}")
    print("✓ Available styles retrieval works")


def run_all_tests():
    """Run all creative engine tests"""
    print("=" * 60)
    print("KUASATURBO CREATIVE ENGINE TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_load_style_profile,
        test_load_template,
        test_load_prompt_preset,
        test_resolve_creative_task,
        test_route_to_model,
        test_build_creative_prompt,
        test_thumbnail_task,
        test_product_render_task,
        test_story_infographic_task,
        test_car_visualizer_task,
        test_image_cleanup_task,
        test_execute_generation,
        test_get_available_tasks,
        test_get_available_styles
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
