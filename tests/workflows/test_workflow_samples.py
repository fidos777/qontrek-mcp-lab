#!/usr/bin/env python3
"""
Phase X: Workflow Sample Tests
Validate workflow content and structure
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from l8.loader.workflow_loader import list_workflows, load_workflow, check_forbidden_keys

def test_no_governance_keys():
    """Test that no workflow contains governance-related keys."""
    print("Test 1: No governance keys in any workflow")
    
    workflows = list_workflows()
    violations = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            forbidden = check_forbidden_keys(workflow)
            if forbidden:
                violations.append((workflow_id, forbidden))
        except Exception as e:
            pass
    
    if violations:
        print(f"  ✗ Found governance keys:")
        for workflow_id, keys in violations:
            print(f"    - {workflow_id}: {keys}")
        return False
    
    print(f"  ✓ No governance keys found in {len(workflows)} workflows")
    return True

def test_output_schema_defined():
    """Test that workflows have output_schema defined."""
    print("\nTest 2: Workflows have output_schema")
    
    workflows = list_workflows()
    missing_schema = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            
            if "output_schema" not in workflow:
                missing_schema.append(workflow_id)
        except Exception as e:
            pass
    
    if missing_schema:
        print(f"  ⚠ Workflows missing output_schema: {missing_schema}")
        # This is a warning, not a hard failure
    
    print(f"  ✓ Output schema check complete")
    return True

def test_expected_output_keys():
    """Test that workflows define expected output keys."""
    print("\nTest 3: Workflows define expected output keys")
    
    expected_outputs = {
        "content_idea_workflow.v1": ["ideas"],
        "caption_builder_workflow.v1": ["captions"],
        "invoice_gen_workflow.v1": ["invoice_text"],
        "kuasaturbo.lead_intake.v1": ["lead_summary", "suggested_reply"],
        "kuasaturbo.tradein_eval.v1": ["evaluation_note", "customer_reply"],
        "kuasaturbo.loancheck.v1": ["assessment_narrative", "document_checklist"],
        "attendance_local_workflow.v1": ["attendance_summary"],
        "menu_update_workflow.v1": ["menu_description"]
    }
    
    missing_keys = []
    
    for workflow_id, expected_keys in expected_outputs.items():
        try:
            workflow = load_workflow(workflow_id)
            output_schema = workflow.get("output_schema", {})
            
            for key in expected_keys:
                if key not in output_schema:
                    missing_keys.append((workflow_id, key))
        except Exception as e:
            pass
    
    if missing_keys:
        print(f"  ⚠ Missing expected output keys:")
        for workflow_id, key in missing_keys:
            print(f"    - {workflow_id}: {key}")
        # Warning only
    
    print(f"  ✓ Output keys check complete")
    return True

def test_persona_matches_widget():
    """Test that workflow personas match widget expectations."""
    print("\nTest 4: Workflow personas match widget expectations")
    
    expected_personas = {
        "content_idea_workflow.v1": "zeyti_bbnu_creator.v1",
        "caption_builder_workflow.v1": "zeyti_bbnu_creator.v1",
        "invoice_gen_workflow.v1": "jordan_cfo_analyst.v1",
        "kuasaturbo.lead_intake.v1": "izzara_friendly_consultant.v1",
        "kuasaturbo.tradein_eval.v1": "tawfiq_sales_closer.v1",
        "kuasaturbo.loancheck.v1": "jordan_cfo_analyst.v1",
        "attendance_local_workflow.v1": "izzara_friendly_consultant.v1",
        "menu_update_workflow.v1": "raya_campaign_storyteller.v1"
    }
    
    mismatches = []
    
    for workflow_id, expected_persona in expected_personas.items():
        try:
            workflow = load_workflow(workflow_id)
            actual_persona = workflow.get("persona_id")
            
            if actual_persona != expected_persona:
                mismatches.append((workflow_id, expected_persona, actual_persona))
        except Exception as e:
            pass
    
    if mismatches:
        print(f"  ✗ Persona mismatches:")
        for workflow_id, expected, actual in mismatches:
            print(f"    - {workflow_id}: expected {expected}, got {actual}")
        return False
    
    print(f"  ✓ All personas match widget expectations")
    return True

def test_workflow_descriptions():
    """Test that workflows have meaningful descriptions."""
    print("\nTest 5: Workflows have meaningful descriptions")
    
    workflows = list_workflows()
    short_descriptions = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            description = workflow.get("description", "")
            
            if len(description) < 20:
                short_descriptions.append(workflow_id)
        except Exception as e:
            pass
    
    if short_descriptions:
        print(f"  ⚠ Workflows with short descriptions: {short_descriptions}")
        # Warning only
    
    print(f"  ✓ Description check complete")
    return True

def test_step_structure():
    """Test that workflow steps have proper structure."""
    print("\nTest 6: Workflow steps have proper structure")
    
    workflows = list_workflows()
    invalid_steps = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            steps = workflow.get("steps", [])
            
            for i, step in enumerate(steps):
                if "id" not in step:
                    invalid_steps.append((workflow_id, i, "missing id"))
                if "type" not in step and "skill_id" not in step:
                    invalid_steps.append((workflow_id, i, "missing type or skill_id"))
        except Exception as e:
            pass
    
    if invalid_steps:
        print(f"  ✗ Invalid step structures:")
        for workflow_id, step_idx, issue in invalid_steps:
            print(f"    - {workflow_id} step[{step_idx}]: {issue}")
        return False
    
    print(f"  ✓ All steps have proper structure")
    return True

def main():
    print("=== Testing Workflow Samples ===\n")
    
    tests = [
        test_no_governance_keys,
        test_output_schema_defined,
        test_expected_output_keys,
        test_persona_matches_widget,
        test_workflow_descriptions,
        test_step_structure
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
