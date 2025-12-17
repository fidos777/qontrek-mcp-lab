#!/usr/bin/env python3
"""
Phase F: Persona Loader Tests
Tests the persona pack loader functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from l5.persona_loader import load_persona, validate_persona, list_personas, get_persona_metadata


def test_list_personas():
    """Test listing available personas."""
    print("Test 1: List available personas")
    personas = list_personas()
    
    assert len(personas) >= 5, f"Expected at least 5 personas, got {len(personas)}"
    expected = [
        'izzara_friendly_consultant.v1',
        'zeyti_bbnu_creator.v1',
        'tawfiq_sales_closer.v1',
        'jordan_cfo_analyst.v1',
        'raya_campaign_storyteller.v1'
    ]
    for p in expected:
        assert p in personas, f"{p} not found"
    
    print(f"  ✓ Found {len(personas)} personas")


def test_load_izzara():
    """Test loading Izzara persona."""
    print("\nTest 2: Load Izzara persona")
    persona = load_persona('izzara_friendly_consultant.v1')
    
    assert persona['identity']['persona_name'] == 'Izzara'
    assert persona['identity']['role'] == 'Friendly Consultant'
    assert 'language_profile' in persona
    assert 'rubric_targets' in persona
    
    print("  ✓ Izzara persona loaded successfully")


def test_rubric_targets():
    """Test rubric targets are valid."""
    print("\nTest 3: Validate rubric targets")
    persona = load_persona('jordan_cfo_analyst.v1')
    
    rubric = persona['rubric_targets']
    required_metrics = ['clarity', 'tone_consistency', 'persuasion_control', 
                       'personalization', 'structure', 'compliance']
    
    for metric in required_metrics:
        assert metric in rubric, f"Missing rubric metric: {metric}"
        score = rubric[metric]
        assert 1 <= score <= 5, f"Invalid score for {metric}: {score}"
    
    print("  ✓ Rubric targets valid")


def test_reject_vertical_logic():
    """Test rejection of vertical/business logic."""
    print("\nTest 4: Reject vertical logic")
    
    invalid_persona = {
        "identity": {
            "persona_id": "test.v1",
            "persona_name": "Test",
            "role": "Test",
            "description": "Test persona with vertical logic"
        },
        "language_profile": {
            "primary_language": "english",
            "english_ratio": 100,
            "bbnu_ratio": 0,
            "code_switching_rules": ["test"]
        },
        "tone": {
            "primary_tone": "professional",
            "emotional_range": ["neutral"],
            "formality_level": 3
        },
        "structure": {
            "message_length": "moderate",
            "paragraph_style": "medium",
            "use_bullets": True
        },
        "persuasion": {
            "persuasion_level": 3,
            "tactics_allowed": ["data_driven"]
        },
        "rhetoric_rules": ["test"],
        "channels": {},
        "rubric_targets": {
            "clarity": 5,
            "tone_consistency": 5,
            "persuasion_control": 5,
            "personalization": 5,
            "structure": 5,
            "compliance": 5
        },
        "constraints": {
            "forbidden_topics": [],
            "required_disclaimers": []
        },
        "workflows": {"test": "test.workflow.v1"}  # FORBIDDEN
    }
    
    is_valid, errors = validate_persona(invalid_persona)
    assert not is_valid, "Should reject persona with vertical logic"
    assert len(errors) > 0, "Should have validation errors"
    
    print("  ✓ Vertical logic correctly rejected")


def test_get_metadata():
    """Test getting persona metadata."""
    print("\nTest 5: Get persona metadata")
    
    meta = get_persona_metadata('zeyti_bbnu_creator.v1')
    assert meta['identity']['persona_name'] == 'Zeyti'
    assert 'language_profile' in meta
    assert 'tone' in meta
    assert 'rubric_targets' in meta
    
    print("  ✓ Metadata retrieved successfully")


def test_missing_persona():
    """Test loading non-existent persona."""
    print("\nTest 6: Handle missing persona")
    
    try:
        load_persona('nonexistent.v1')
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        assert 'nonexistent' in str(e)
        print("  ✓ Missing persona handled correctly")


def main():
    """Run all tests."""
    print("=== Testing Persona Loader ===\n")
    
    tests = [
        test_list_personas,
        test_load_izzara,
        test_rubric_targets,
        test_reject_vertical_logic,
        test_get_metadata,
        test_missing_persona
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print("\n=== Loader Tests Complete ===\n")
    if failed == 0:
        print(f"✅ PASS: All {passed} tests passed")
        return 0
    else:
        print(f"❌ FAIL: {passed} passed, {failed} failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
