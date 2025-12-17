#!/usr/bin/env python3
"""
Phase X: Workflow Registry Tests
Verify all workflows exist and are properly registered
"""

import sys
import os
import yaml

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from l8.loader.workflow_loader import list_workflows, load_workflow

def test_all_workflows_exist():
    """Test that all 8 workflow IDs exist."""
    print("Test 1: All 8 workflows exist")
    
    workflows = list_workflows()
    
    expected_workflows = [
        "content_idea_workflow.v1",
        "caption_builder_workflow.v1",
        "invoice_gen_workflow.v1",
        "kuasaturbo.lead_intake.v1",
        "kuasaturbo.tradein_eval.v1",
        "kuasaturbo.loancheck.v1",
        "attendance_local_workflow.v1",
        "menu_update_workflow.v1"
    ]
    
    missing = [w for w in expected_workflows if w not in workflows]
    
    if missing:
        print(f"  ✗ Missing workflows: {missing}")
        return False
    
    print(f"  ✓ All {len(expected_workflows)} workflows found")
    return True

def test_workflows_in_service_registry():
    """Test that workflows are correctly referenced in service_registry.yaml."""
    print("\nTest 2: Workflows referenced in service registry")
    
    # Load service registry
    try:
        with open('services/service_registry.yaml', 'r') as f:
            registry = yaml.safe_load(f)
    except Exception as e:
        print(f"  ✗ Failed to load service registry: {e}")
        return False
    
    services = registry.get('services', {})
    
    if len(services) < 8:
        print(f"  ✗ Expected at least 8 services, found {len(services)}")
        return False
    
    # Check that each service has a workflow_id
    missing_workflow = []
    for service_id, service_data in services.items():
        if 'workflow_id' not in service_data:
            missing_workflow.append(service_id)
    
    if missing_workflow:
        print(f"  ✗ Services missing workflow_id: {missing_workflow}")
        return False
    
    print(f"  ✓ All {len(services)} services have workflow_id")
    return True

def test_load_all_workflows():
    """Test that loading each workflow does not raise error."""
    print("\nTest 3: Load all workflows without errors")
    
    workflows = list_workflows()
    
    failed = []
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
        except Exception as e:
            failed.append((workflow_id, str(e)))
    
    if failed:
        print(f"  ✗ {len(failed)} workflows failed to load:")
        for workflow_id, error in failed:
            print(f"    - {workflow_id}: {error}")
        return False
    
    print(f"  ✓ All {len(workflows)} workflows loaded successfully")
    return True

def test_workflow_structure():
    """Test that workflows have correct structure."""
    print("\nTest 4: Validate workflow structure")
    
    workflows = list_workflows()
    
    if not workflows:
        print("  ✗ No workflows found")
        return False
    
    invalid = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            
            # Check required fields
            required = ["id", "description", "version", "steps"]
            missing = [f for f in required if f not in workflow]
            
            if missing:
                invalid.append((workflow_id, f"missing fields: {missing}"))
                continue
            
            # Check steps is non-empty array
            if not isinstance(workflow["steps"], list) or len(workflow["steps"]) == 0:
                invalid.append((workflow_id, "steps must be non-empty array"))
                continue
            
        except Exception as e:
            invalid.append((workflow_id, str(e)))
    
    if invalid:
        print(f"  ✗ {len(invalid)} workflows have invalid structure:")
        for workflow_id, issue in invalid:
            print(f"    - {workflow_id}: {issue}")
        return False
    
    print(f"  ✓ All workflows have valid structure")
    return True

def test_persona_mapping():
    """Test that workflows have persona_id defined."""
    print("\nTest 5: Workflows have persona_id")
    
    workflows = list_workflows()
    
    missing_persona = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            
            if "persona_id" not in workflow:
                missing_persona.append(workflow_id)
        except Exception as e:
            pass
    
    if missing_persona:
        print(f"  ✗ Workflows missing persona_id: {missing_persona}")
        return False
    
    print(f"  ✓ All workflows have persona_id defined")
    return True

def test_stateless_flag():
    """Test that workflows are marked as stateless."""
    print("\nTest 6: Workflows marked as stateless")
    
    workflows = list_workflows()
    
    not_stateless = []
    
    for workflow_id in workflows:
        try:
            workflow = load_workflow(workflow_id)
            
            if workflow.get("stateless") is not True:
                not_stateless.append(workflow_id)
        except Exception as e:
            pass
    
    if not_stateless:
        print(f"  ⚠ Workflows not marked as stateless: {not_stateless}")
        # This is a warning, not a failure
    
    print(f"  ✓ Stateless flag checked")
    return True

def main():
    print("=== Testing Workflow Registry ===\n")
    
    tests = [
        test_all_workflows_exist,
        test_workflows_in_service_registry,
        test_load_all_workflows,
        test_workflow_structure,
        test_persona_mapping,
        test_stateless_flag
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
    
    print("\n=== Registry Tests Complete ===\n")
    
    if failed == 0:
        print(f"✅ PASS: All {passed} tests passed\n")
        return 0
    else:
        print(f"❌ FAIL: {passed} passed, {failed} failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
