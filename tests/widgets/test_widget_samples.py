#!/usr/bin/env python3
"""
Phase W: Widget Sample Tests
Validate all 8 sample widgets
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from l3.loader.widget_loader import list_widgets, load_widget, check_forbidden_keys

def test_all_widgets_valid():
    """Test that all 8 sample widgets pass schema validation."""
    print("Test 1: All widgets pass schema validation")
    
    widgets = list_widgets()
    
    if len(widgets) < 8:
        print(f"  ✗ Expected at least 8 widgets, found {len(widgets)}")
        return False
    
    failed = []
    for widget_id in widgets:
        try:
            widget = load_widget(widget_id)
        except Exception as e:
            failed.append((widget_id, str(e)))
    
    if failed:
        print(f"  ✗ {len(failed)} widgets failed validation:")
        for widget_id, error in failed:
            print(f"    - {widget_id}: {error}")
        return False
    
    print(f"  ✓ All {len(widgets)} widgets valid")
    return True

def test_all_fields_complete():
    """Test that all fields have id, label, type, required."""
    print("\nTest 2: All fields have required properties")
    
    widgets = list_widgets()
    incomplete = []
    
    for widget_id in widgets:
        try:
            widget = load_widget(widget_id)
            for i, field in enumerate(widget.get("fields", [])):
                required_props = ["id", "label", "type", "required"]
                missing = [p for p in required_props if p not in field]
                if missing:
                    incomplete.append((widget_id, i, missing))
        except Exception as e:
            pass
    
    if incomplete:
        print(f"  ✗ Found incomplete fields:")
        for widget_id, field_idx, missing in incomplete:
            print(f"    - {widget_id} field[{field_idx}] missing: {missing}")
        return False
    
    print(f"  ✓ All fields complete")
    return True

def test_all_workflows_defined():
    """Test that all workflows reference non-empty workflow.trigger and workflow.persona."""
    print("\nTest 3: All workflows properly defined")
    
    widgets = list_widgets()
    invalid = []
    
    for widget_id in widgets:
        try:
            widget = load_widget(widget_id)
            workflow = widget.get("workflow", {})
            
            if not workflow.get("trigger"):
                invalid.append((widget_id, "missing trigger"))
            
            if not workflow.get("persona"):
                invalid.append((widget_id, "missing persona"))
        except Exception as e:
            pass
    
    if invalid:
        print(f"  ✗ Found invalid workflows:")
        for widget_id, issue in invalid:
            print(f"    - {widget_id}: {issue}")
        return False
    
    print(f"  ✓ All workflows properly defined")
    return True

def test_no_governance_keys():
    """Test that no widget contains governance-related keys."""
    print("\nTest 4: No governance keys in any widget")
    
    widgets = list_widgets()
    violations = []
    
    for widget_id in widgets:
        try:
            widget = load_widget(widget_id)
            forbidden = check_forbidden_keys(widget)
            if forbidden:
                violations.append((widget_id, forbidden))
        except Exception as e:
            pass
    
    if violations:
        print(f"  ✗ Found governance keys:")
        for widget_id, keys in violations:
            print(f"    - {widget_id}: {keys}")
        return False
    
    print(f"  ✓ No governance keys found")
    return True

def test_vertical_distribution():
    """Test that widgets cover multiple verticals."""
    print("\nTest 5: Widgets cover multiple verticals")
    
    widgets = list_widgets()
    verticals = set()
    
    for widget_id in widgets:
        try:
            widget = load_widget(widget_id)
            verticals.add(widget.get("vertical"))
        except Exception as e:
            pass
    
    expected_verticals = ["content", "accounting", "crm", "automotive", "hr", "fnb"]
    found_expected = [v for v in expected_verticals if v in verticals]
    
    if len(found_expected) < 5:
        print(f"  ✗ Expected at least 5 verticals, found {len(found_expected)}: {found_expected}")
        return False
    
    print(f"  ✓ Found {len(verticals)} verticals: {sorted(verticals)}")
    return True

def test_specific_widget_content():
    """Test specific widget characteristics."""
    print("\nTest 6: Specific widget characteristics")
    
    test_cases = [
        {
            "widget_id": "content_idea_widget.v1",
            "expected_vertical": "content",
            "expected_persona": "zeyti_bbnu_creator.v1",
            "min_fields": 3
        },
        {
            "widget_id": "invoice_gen_widget.v1",
            "expected_vertical": "accounting",
            "expected_persona": "jordan_cfo_analyst.v1",
            "min_fields": 3
        },
        {
            "widget_id": "trade_in_eval_widget.v1",
            "expected_vertical": "automotive",
            "expected_persona": "tawfiq_sales_closer.v1",
            "min_fields": 4
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        widget_id = test_case["widget_id"]
        try:
            widget = load_widget(widget_id)
            
            if widget["vertical"] != test_case["expected_vertical"]:
                print(f"  ✗ {widget_id}: wrong vertical")
                all_passed = False
                continue
            
            if widget["workflow"]["persona"] != test_case["expected_persona"]:
                print(f"  ✗ {widget_id}: wrong persona")
                all_passed = False
                continue
            
            if len(widget["fields"]) < test_case["min_fields"]:
                print(f"  ✗ {widget_id}: too few fields")
                all_passed = False
                continue
            
        except Exception as e:
            print(f"  ✗ {widget_id}: {e}")
            all_passed = False
    
    if all_passed:
        print(f"  ✓ All specific characteristics validated")
    
    return all_passed

def main():
    print("=== Testing Widget Samples ===\n")
    
    tests = [
        test_all_widgets_valid,
        test_all_fields_complete,
        test_all_workflows_defined,
        test_no_governance_keys,
        test_vertical_distribution,
        test_specific_widget_content
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
    
    print("\n=== Sample Tests Complete ===\n")
    
    if failed == 0:
        print(f"✅ PASS: All {passed} tests passed\n")
        return 0
    else:
        print(f"❌ FAIL: {passed} passed, {failed} failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
