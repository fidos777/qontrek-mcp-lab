#!/usr/bin/env python3
"""
Phase W: Widget Loader Tests
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from l3.loader.widget_loader import list_widgets, load_widget, validate_widget

def test_list_widgets():
    """Test that list_widgets returns at least 8 widgets."""
    print("Test 1: List available widgets")
    widgets = list_widgets()
    
    if len(widgets) >= 8:
        print(f"  ✓ Found {len(widgets)} widgets (expected >= 8)")
        return True
    else:
        print(f"  ✗ Found only {len(widgets)} widgets (expected >= 8)")
        return False

def test_load_all_widgets():
    """Test that all sample widgets can be loaded."""
    print("\nTest 2: Load all sample widgets")
    widgets = list_widgets()
    
    success_count = 0
    fail_count = 0
    
    for widget_id in widgets:
        try:
            widget = load_widget(widget_id)
            success_count += 1
        except Exception as e:
            print(f"  ✗ Failed to load {widget_id}: {e}")
            fail_count += 1
    
    if fail_count == 0:
        print(f"  ✓ All {success_count} widgets loaded successfully")
        return True
    else:
        print(f"  ✗ {fail_count} widgets failed to load")
        return False

def test_validate_invalid_widget():
    """Test that validate_widget rejects invalid widgets."""
    print("\nTest 3: Reject widget with missing workflow")
    
    invalid_widget = {
        "widget_id": "test_widget.v1",
        "widget_name": "Test Widget",
        "vertical": "content",
        "description": "Test",
        "fields": [
            {
                "id": "test_field",
                "label": "Test",
                "type": "text",
                "required": True
            }
        ]
        # Missing workflow - should fail
    }
    
    is_valid, errors = validate_widget(invalid_widget)
    
    if not is_valid and len(errors) > 0:
        print(f"  ✓ Invalid widget correctly rejected: {errors[0]}")
        return True
    else:
        print(f"  ✗ Invalid widget was not rejected")
        return False

def test_reject_governance_widget():
    """Test that widgets with governance keys are rejected."""
    print("\nTest 4: Reject widget with governance_gate")
    
    governance_widget = {
        "widget_id": "bad_widget.v1",
        "widget_name": "Bad Widget",
        "vertical": "content",
        "description": "Test",
        "fields": [
            {
                "id": "test_field",
                "label": "Test",
                "type": "text",
                "required": True
            }
        ],
        "workflow": {
            "trigger": "test_workflow.v1",
            "persona": "test_persona.v1"
        },
        "governance_gate": "G13"  # FORBIDDEN
    }
    
    is_valid, errors = validate_widget(governance_widget)
    
    if not is_valid and any("governance" in str(e).lower() for e in errors):
        print(f"  ✓ Governance widget correctly rejected")
        return True
    else:
        print(f"  ✗ Governance widget was not rejected")
        return False

def test_widget_structure():
    """Test that loaded widgets have correct structure."""
    print("\nTest 5: Validate widget structure")
    
    widgets = list_widgets()
    if not widgets:
        print("  ✗ No widgets found")
        return False
    
    widget = load_widget(widgets[0])
    
    # Check required fields
    required = ["widget_id", "widget_name", "vertical", "description", "fields", "workflow"]
    missing = [f for f in required if f not in widget]
    
    if missing:
        print(f"  ✗ Missing required fields: {missing}")
        return False
    
    # Check workflow structure
    if "trigger" not in widget["workflow"] or "persona" not in widget["workflow"]:
        print(f"  ✗ Workflow missing trigger or persona")
        return False
    
    # Check fields structure
    if not isinstance(widget["fields"], list) or len(widget["fields"]) == 0:
        print(f"  ✗ Fields must be non-empty array")
        return False
    
    first_field = widget["fields"][0]
    field_required = ["id", "label", "type", "required"]
    field_missing = [f for f in field_required if f not in first_field]
    
    if field_missing:
        print(f"  ✗ Field missing required properties: {field_missing}")
        return False
    
    print(f"  ✓ Widget structure is valid")
    return True

def test_specific_widgets():
    """Test specific widget examples."""
    print("\nTest 6: Test specific widget examples")
    
    test_cases = [
        ("content_idea_widget.v1", "content", "zeyti_bbnu_creator.v1"),
        ("invoice_gen_widget.v1", "accounting", "jordan_cfo_analyst.v1"),
        ("lead_intake_widget.v1", "crm", "izzara_friendly_consultant.v1")
    ]
    
    all_passed = True
    
    for widget_id, expected_vertical, expected_persona in test_cases:
        try:
            widget = load_widget(widget_id)
            
            if widget["vertical"] != expected_vertical:
                print(f"  ✗ {widget_id}: wrong vertical (expected {expected_vertical}, got {widget['vertical']})")
                all_passed = False
                continue
            
            if widget["workflow"]["persona"] != expected_persona:
                print(f"  ✗ {widget_id}: wrong persona (expected {expected_persona}, got {widget['workflow']['persona']})")
                all_passed = False
                continue
            
        except Exception as e:
            print(f"  ✗ {widget_id}: {e}")
            all_passed = False
    
    if all_passed:
        print(f"  ✓ All specific widgets validated")
    
    return all_passed

def main():
    print("=== Testing Widget Loader ===\n")
    
    tests = [
        test_list_widgets,
        test_load_all_widgets,
        test_validate_invalid_widget,
        test_reject_governance_widget,
        test_widget_structure,
        test_specific_widgets
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Test failed with exception: {e}")
            failed += 1
    
    print("\n=== Loader Tests Complete ===\n")
    
    if failed == 0:
        print(f"✅ PASS: All {passed} tests passed\n")
        return 0
    else:
        print(f"❌ FAIL: {passed} passed, {failed} failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
