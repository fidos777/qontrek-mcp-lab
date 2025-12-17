#!/usr/bin/env python3
"""
Phase E: Vertical Sample Tests
Tests the actual vertical pack samples (automotive, solar).
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from l6.vertical_loader import load_vertical, validate_vertical


def test_automotive_structure():
    """Test automotive vertical structure."""
    print("Test 1: Automotive vertical structure")
    vertical = load_vertical('automotive')
    
    # Check industry identity
    assert vertical['industry_identity']['industry_name'] == "Automotive Sales"
    assert vertical['industry_identity']['industry_code'] == "automotive"
    assert vertical['industry_identity']['icon'] == "🚗"
    
    # Check entities
    assert 'lead' in vertical['entities']
    assert 'vehicle' in vertical['entities']
    assert 'deal' in vertical['entities']
    
    # Check skills (functional only)
    skills = vertical['skills']
    assert 'branding' in skills
    assert 'prd' in skills
    assert 'pricing' in skills
    
    # Ensure NO behavioral skills
    for skill_name in skills.keys():
        assert 'persuasion' not in skill_name.lower()
        assert 'tone' not in skill_name.lower()
        assert 'personality' not in skill_name.lower()
    
    # Check workflows
    assert 'launchkit' in vertical['workflows']
    assert 'followup_only' in vertical['workflows']
    
    # Check compliance
    compliance = vertical['compliance']
    assert 'required_documents' in compliance
    assert 'disclaimers' in compliance
    assert 'industry_rules' in compliance
    
    # Ensure NO governance in compliance
    assert 'governance' not in compliance
    assert 'policies' not in compliance
    
    # Check statuses
    statuses = vertical['statuses']
    assert 'new' in statuses
    assert 'closed_won' in statuses
    assert 'closed_lost' in statuses
    
    print("  ✓ Automotive structure valid")


def test_solar_structure():
    """Test solar vertical structure."""
    print("\nTest 2: Solar vertical structure")
    vertical = load_vertical('solar')
    
    # Check industry identity
    assert vertical['industry_identity']['industry_name'] == "Solar Energy"
    assert vertical['industry_identity']['industry_code'] == "solar"
    assert vertical['industry_identity']['icon'] == "☀️"
    
    # Check entities
    assert 'lead' in vertical['entities']
    assert 'site_assessment' in vertical['entities']
    assert 'system_design' in vertical['entities']
    assert 'proposal' in vertical['entities']
    
    # Check skills (functional only)
    skills = vertical['skills']
    assert 'branding' in skills
    assert 'prd' in skills
    
    # Ensure NO behavioral skills
    for skill_name in skills.keys():
        assert 'emotional' not in skill_name.lower()
        assert 'behavior' not in skill_name.lower()
    
    # Check workflows
    assert 'launchkit' in vertical['workflows']
    
    # Check compliance
    compliance = vertical['compliance']
    assert len(compliance['required_documents']) > 0
    assert len(compliance['disclaimers']) > 0
    assert len(compliance['industry_rules']) > 0
    
    # Check statuses
    statuses = vertical['statuses']
    assert 'new' in statuses
    assert 'site_assessment_scheduled' in statuses
    assert 'system_activated' in statuses
    
    print("  ✓ Solar structure valid")


def test_automotive_widgets():
    """Test automotive widgets are declarative only."""
    print("\nTest 3: Automotive widgets (declarative only)")
    vertical = load_vertical('automotive')
    
    widgets = vertical.get('widgets', {})
    assert len(widgets) > 0, "Should have widgets defined"
    
    # Check lead_intake widget
    assert 'lead_intake' in widgets
    lead_widget = widgets['lead_intake']
    
    assert lead_widget['type'] == 'form'
    assert 'fields' in lead_widget
    assert len(lead_widget['fields']) > 0
    
    # Ensure NO logic/behavior in widgets
    for widget_name, widget_def in widgets.items():
        assert 'logic' not in widget_def, f"Widget {widget_name} has logic"
        assert 'behavior' not in widget_def, f"Widget {widget_name} has behavior"
        assert 'decision' not in widget_def, f"Widget {widget_name} has decision logic"
        assert 'chain' not in widget_def, f"Widget {widget_name} has chaining"
    
    # Check workflow entrypoint (allowed)
    if 'workflow_entrypoint' in lead_widget:
        assert lead_widget['workflow_entrypoint'].endswith('.v1')
    
    print("  ✓ Automotive widgets are declarative")


def test_solar_widgets():
    """Test solar widgets are declarative only."""
    print("\nTest 4: Solar widgets (declarative only)")
    vertical = load_vertical('solar')
    
    widgets = vertical.get('widgets', {})
    assert len(widgets) > 0, "Should have widgets defined"
    
    # Check widgets have proper structure
    for widget_name, widget_def in widgets.items():
        assert 'type' in widget_def
        assert 'fields' in widget_def
        assert widget_def['type'] in ['form', 'table', 'card', 'list', 'detail']
        
        # Ensure NO logic/behavior
        assert 'logic' not in widget_def
        assert 'behavior' not in widget_def
        assert 'rules' not in widget_def
    
    print("  ✓ Solar widgets are declarative")


def test_no_personality_in_verticals():
    """Test that verticals contain NO personality/tone/behavior."""
    print("\nTest 5: No personality in verticals")
    
    for industry_code in ['automotive', 'solar']:
        vertical = load_vertical(industry_code)
        
        # Check entire vertical for forbidden terms
        vertical_str = str(vertical).lower()
        
        forbidden_terms = [
            'personality', 'persuasive', 'emotional_delivery',
            'sentiment', 'empathy', 'friendly_tone'
        ]
        
        for term in forbidden_terms:
            assert term not in vertical_str, \
                f"{industry_code} vertical contains forbidden term: {term}"
    
    print("  ✓ No personality/behavior in verticals")


def test_compliance_not_governance():
    """Test that compliance is not governance."""
    print("\nTest 6: Compliance vs Governance separation")
    
    for industry_code in ['automotive', 'solar']:
        vertical = load_vertical(industry_code)
        compliance = vertical.get('compliance', {})
        
        # Compliance should have industry rules
        assert 'industry_rules' in compliance or 'required_documents' in compliance
        
        # But NOT governance
        assert 'governance' not in compliance
        assert 'policies' not in compliance
        assert 'approval_gates' not in compliance
        assert 'quality_gates' not in compliance
    
    print("  ✓ Compliance properly separated from governance")


def main():
    """Run all tests."""
    print("=== Testing Vertical Samples ===\n")
    
    tests = [
        test_automotive_structure,
        test_solar_structure,
        test_automotive_widgets,
        test_solar_widgets,
        test_no_personality_in_verticals,
        test_compliance_not_governance
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
    
    print("\n=== Sample Tests Complete ===\n")
    if failed == 0:
        print(f"✅ PASS: All {passed} tests passed")
        return 0
    else:
        print(f"❌ FAIL: {passed} passed, {failed} failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
