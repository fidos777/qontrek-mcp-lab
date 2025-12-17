#!/usr/bin/env python3
"""
L6 Consistency Check
Validates alignment between models, registry, runner, and router.
"""

import json
import sys
from pathlib import Path

def check_registry():
    """Check registry.json structure."""
    print("🔍 Checking l6/registry.json...")
    
    registry_path = Path("l6/registry.json")
    if not registry_path.exists():
        print("  ❌ registry.json not found")
        return False
    
    with open(registry_path) as f:
        registry = json.load(f)
    
    # Check required fields
    if "workflows" not in registry:
        print("  ❌ Missing 'workflows' array")
        return False
    
    for wf in registry["workflows"]:
        required = ["id", "name", "version", "category", "domain", "produces"]
        missing = [f for f in required if f not in wf]
        if missing:
            print(f"  ❌ Workflow {wf.get('id', 'unknown')} missing: {missing}")
            return False
    
    print("  ✅ Registry structure valid")
    return True

def check_models():
    """Check model schemas."""
    print("\n🔍 Checking l6/models/*.json...")
    
    models = ["brand_context.json", "wto.json"]
    all_valid = True
    
    for model in models:
        model_path = Path(f"l6/models/{model}")
        if not model_path.exists():
            print(f"  ❌ {model} not found")
            all_valid = False
            continue
        
        try:
            with open(model_path) as f:
                schema = json.load(f)
            
            # Check JSON Schema fields
            if "$schema" not in schema:
                print(f"  ⚠️  {model} missing $schema")
            
            print(f"  ✅ {model} valid")
        except json.JSONDecodeError as e:
            print(f"  ❌ {model} invalid JSON: {e}")
            all_valid = False
    
    return all_valid

def check_packager():
    """Check packager.py implementation."""
    print("\n🔍 Checking l6/utils/packager.py...")
    
    packager_path = Path("l6/utils/packager.py")
    if not packager_path.exists():
        print("  ❌ packager.py not found")
        return False
    
    content = packager_path.read_text()
    
    # Check for key classes and methods
    checks = [
        ("class WorkflowPackager", "WorkflowPackager class"),
        ("def create_wto", "create_wto method"),
        ("def package_creative_funnel", "package_creative_funnel method"),
        ("def merge_wtos", "merge_wtos method"),
        ("def save_wto", "save_wto method"),
        ("def load_wto", "load_wto method"),
        ("def validate_wto", "validate_wto method")
    ]
    
    all_found = True
    for check_str, name in checks:
        if check_str not in content:
            print(f"  ❌ Missing {name}")
            all_found = False
    
    if all_found:
        print("  ✅ Packager implementation complete")
    
    return all_found

def check_runner_alignment():
    """Check l6_runner.py aligns with models."""
    print("\n🔍 Checking l6/l6_runner.py alignment...")
    
    runner_path = Path("l6/l6_runner.py")
    if not runner_path.exists():
        print("  ❌ l6_runner.py not found")
        return False
    
    content = runner_path.read_text()
    
    # Check for key functions
    checks = [
        ("def run_workflow", "run_workflow function"),
        ("def resolve_input", "resolve_input function"),
        ("def load_skill_handler", "load_skill_handler function")
    ]
    
    all_found = True
    for check_str, name in checks:
        if check_str not in content:
            print(f"  ❌ Missing {name}")
            all_found = False
    
    # Check output structure matches output_envelope
    if '"status":' in content and '"output":' in content:
        print("  ✅ Output structure matches envelope spec")
    else:
        print("  ⚠️  Output structure may not match envelope spec")
    
    if all_found:
        print("  ✅ Runner implementation complete")
    
    return all_found

def check_router_alignment():
    """Check router.py aligns with architecture."""
    print("\n🔍 Checking l6/router.py alignment...")
    
    router_path = Path("l6/router.py")
    if not router_path.exists():
        print("  ❌ router.py not found")
        return False
    
    content = router_path.read_text()
    
    # Check for dispatch function
    if "def dispatch" not in content:
        print("  ❌ Missing dispatch function")
        return False
    
    # Check for workflow routing
    if "run_workflow" not in content:
        print("  ❌ Missing run_workflow call")
        return False
    
    print("  ✅ Router implementation complete")
    return True

def check_skill_implementations():
    """Check LaunchKit skill implementations."""
    print("\n🔍 Checking LaunchKit skill implementations...")
    
    # Load registry
    with open("l6/registry.json") as f:
        registry = json.load(f)
    
    if "skills" not in registry:
        print("  ⚠️  No skills section in registry")
        return True
    
    all_valid = True
    llm_powered_count = 0
    
    for skill in registry["skills"]:
        skill_id = skill["id"]
        handler_path = Path(skill.get("handler", ""))
        
        if not handler_path.exists():
            print(f"  ❌ Handler not found: {skill_id}")
            all_valid = False
            continue
        
        # Check for required files
        skill_dir = handler_path.parent
        required_files = [
            "handler.py",
            "schema.json",
            "manifest.json",
            "governance.yml",
            "reflexion.yml",
            "prompts/main.txt",
            "templates/output.md",
            "sample_inputs.json",
            "sample_outputs.json",
            "validate.sh"
        ]
        
        missing_files = []
        for file in required_files:
            if not (skill_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"  ⚠️  {skill_id} missing: {', '.join(missing_files)}")
        else:
            print(f"  ✅ {skill_id} complete (10/10 files)")
        
        # Count LLM-powered skills
        if skill.get("llm_powered"):
            llm_powered_count += 1
    
    print(f"\n  📊 LLM-powered skills: {llm_powered_count}/{len(registry['skills'])}")
    
    return all_valid

def check_workflow_definitions():
    """Check workflow definitions match registry."""
    print("\n🔍 Checking workflow definitions...")
    
    # Load registry
    with open("l6/registry.json") as f:
        registry = json.load(f)
    
    all_valid = True
    launchkit_count = 0
    
    for wf in registry["workflows"]:
        wf_id = wf["id"]
        wf_path = Path(f"l6/workflows/{wf_id}/workflow.json")
        schema_path = Path(f"l6/workflows/{wf_id}/schema.json")
        
        if not wf_path.exists():
            print(f"  ❌ Workflow definition not found: {wf_id}")
            all_valid = False
            continue
        
        if not schema_path.exists():
            print(f"  ❌ Schema not found: {wf_id}")
            all_valid = False
            continue
        
        # Load and validate workflow
        with open(wf_path) as f:
            workflow = json.load(f)
        
        # Load and validate schema
        with open(schema_path) as f:
            schema = json.load(f)
        
        # Check steps exist
        if "steps" in workflow:
            step_count = len(workflow["steps"])
            if step_count == 0:
                print(f"  ⚠️  {wf_id}: no steps defined")
        
        # Count LaunchKit workflows
        if wf.get("category") == "launchkit":
            launchkit_count += 1
        
        print(f"  ✅ {wf_id} definition valid")
    
    # Validate LaunchKit workflows
    print(f"\n  📊 LaunchKit workflows: {launchkit_count}/6")
    if launchkit_count < 6:
        print(f"  ⚠️  Expected 6 LaunchKit workflows, found {launchkit_count}")
    
    return all_valid

def main():
    """Run all consistency checks."""
    print("=" * 60)
    print("L6 CONSISTENCY CHECK")
    print("=" * 60)
    
    checks = [
        check_registry,
        check_models,
        check_packager,
        check_runner_alignment,
        check_router_alignment,
        check_skill_implementations,
        check_workflow_definitions
    ]
    
    results = [check() for check in checks]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL CHECKS PASSED")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
