#!/usr/bin/env python3
"""
Phase E: Vertical Loader Tests
Tests the vertical pack loader functionality.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from l6.vertical_loader import (
    load_vertical,
    validate_vertical,
    list_verticals,
    get_vertical_info
)


def test_list_verticals():
    """Test listing available verticals."""
    print("Test 1: List available verticals")
    verticals = list_verticals()
    
    assert len(verticals) >= 2, f"Expected at least 2 verticals, got {len(verticals)}"
    assert 'automotive' in verticals, "automotive vertical not found"
    assert 'solar' in verticals, "solar vertical not found"
    
    print(f"  ✓ Found {len(verticals)} verticals: {', '.join(verticals)}")


def test_load_automotive():
    """Test loading automotive vertical."""
    print("\nTest 2: Load automotive vertical")
    vertical = load_vertical('automotive')
    
    assert vertical['industry_identity']['industry_code'] == 'automotive'
    assert 'entities' in vertical
    assert 'skills' in vertical
    assert 'workflows' in vertical
    assert 'compliance' in vertical
    assert 'statuses' in vertical
    
    print("  ✓ Automotive vertical loaded successfully")


def test_load_solar():
    """Test loading solar vertical."""
    print("\nTest 3: Load solar vertical")
    vertical = load_vertical('solar')
    
    assert vertical['industry_identity']['industry_code'] == 'solar'
    assert 'entities' in vertical
    assert 'skills' in vertical
    assert 'workflows' in vertical
    assert 'compliance' in vertical
    assert 'statuses' in vertical
    
    print("  ✓ Solar vertical loaded successfully")


def test_validate_structure():
    """Test validation of vertical structure."""
    print("\nTest 4: Validate vertical structure")
    
    # Valid vertical
    valid_vertical = {
        "industry_identity": {
            "industry_name": "Test Industry",
            "industry_code": "test",
            "description": "Test industry description for validation"
        },
        "entities": {
            "test_entity": {
                "required": ["field1"],
                "optional": ["field2"]
            }
        },
        "skills": {
            "test_skill": "test.skill.v1"
        },
        "workflows": {
            "test_workflow": "test.workflow.v1"
        },
        "compliance": {
            "required_documents": ["Doc1"],
            "disclaimers": ["Disclaimer1"],
            "industry_rules": ["Rule1"]
        },
        "statuses": ["new", "active", "closed"]
    }
    
    is_valid, errors = validate_vertical(valid_vertical)
    assert is_valid, f"Valid vertical failed validation: {errors}"
    
    print("  ✓ Valid vertical passes validation")


def test_reject_behavioral_skills():
    """Test rejection of behavioral skills."""
    print("\nTest 5: Reject behavioral skills")
    
    invalid_vertical = {
        "industry_identity": {
            "industry_name": "Test Industry",
            "industry_code": "test",
            "description": "Test industry with behavioral skills"
        },
        "entities": {
            "test_entity": {
                "required": ["field1"],
                "optional": []
            }
        },
        "skills": {
            "persuasion_engine": "test.persuasion.v1",  # FORBIDDEN
            "tone_adjustment": "test.tone.v1"  # FORBIDDEN
        },
        "workflows": {
            "test_workflow": "test.workflow.v1"
        },
        "compliance": {},
        "statuses": ["new"]
    }
    
    is_valid, errors = validate_vertical(invalid_vertical)
    assert not is_valid, "Behavioral skills should be rejected"
    assert any('behavioral' in err.lower() for err in errors), "Should mention behavioral skills"
    
    print("  ✓ Behavioral skills correctly rejected")


def test_get_vertical_info():
    """Test getting vertical info."""
    print("\nTest 6: Get vertical info")
    
    info = get_vertical_info('automotive')
    assert info['industry_code'] == 'automotive'
    assert 'industry_name' in info
    assert 'description' in info
    assert info['entity_count'] > 0
    assert info['skill_count'] > 0
    
    print(f"  ✓ Got info for {info['industry_name']}")


def test_missing_vertical():
    """Test loading non-existent vertical."""
    print("\nTest 7: Handle missing vertical")
    
    try:
        load_vertical('nonexistent')
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        assert 'nonexistent' in str(e)
        print("  ✓ Missing vertical handled correctly")


def main():
    """Run all tests."""
    print("=== Testing Vertical Loader ===\n")
    
    tests = [
        test_list_verticals,
        test_load_automotive,
        test_load_solar,
        test_validate_structure,
        test_reject_behavioral_skills,
        test_get_vertical_info,
        test_missing_vertical
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
