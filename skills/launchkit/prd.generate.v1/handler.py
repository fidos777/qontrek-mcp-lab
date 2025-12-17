#!/usr/bin/env python3
"""
LaunchKit PRD Generator - Production Version
Generates Product Requirements Document from brand context.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from lib.logger import log
from lib.llm_client import generate


def prepare_context(params: dict) -> dict:
    """Prepare context for LLM generation."""
    icp = params.get("icp", {})
    
    return {
        "brand_name": params.get("brand_name", ""),
        "mission": params.get("mission", ""),
        "positioning": params.get("positioning", ""),
        "value_proposition": params.get("value_proposition", ""),
        "icp_demographics": icp.get("demographics", ""),
        "icp_pain_points": ", ".join(icp.get("pain_points", [])),
        "icp_goals": ", ".join(icp.get("goals", [])),
        "brand_themes": ", ".join(params.get("brand_themes", [])),
        "product_type": params.get("product_type", "SaaS platform"),
        "platform": params.get("platform", "web"),
        "constraints": ", ".join(params.get("constraints", []))
    }


def generate_problem_statement(context: dict) -> str:
    """Generate problem statement using LLM."""
    prompt = f"""Generate a clear problem statement for {context['brand_name']}.

Target Users: {context['icp_demographics']}
Pain Points: {context['icp_pain_points']}
Goals: {context['icp_goals']}

Create a problem statement that:
- Identifies the core problem
- Quantifies impact where possible
- Explains why existing solutions fail
- Sets up the need for this product
"""
    
    return generate(prompt, context, max_tokens=400)


def generate_solution_overview(context: dict) -> str:
    """Generate solution overview using LLM."""
    prompt = f"""Generate a solution overview for {context['brand_name']}.

Value Proposition: {context['value_proposition']}
Product Type: {context['product_type']}
Platform: {context['platform']}

Describe how the product solves the problem:
- Core approach and methodology
- Key differentiators
- Technical approach (high-level)
- Expected outcomes
"""
    
    return generate(prompt, context, max_tokens=400)


def generate_user_personas(context: dict) -> list:
    """Generate user personas from ICP."""
    icp_demo = context.get("icp_demographics", "")
    pain_points = context.get("icp_pain_points", "").split(", ")
    goals = context.get("icp_goals", "").split(", ")
    
    personas = []
    
    # Primary persona
    personas.append({
        "name": "Primary User",
        "role": icp_demo.split(",")[0] if "," in icp_demo else icp_demo,
        "pain_points": pain_points[:3],
        "goals": goals[:3],
        "tech_savviness": "Medium to High",
        "usage_frequency": "Daily"
    })
    
    # Secondary persona (if applicable)
    if len(pain_points) > 3:
        personas.append({
            "name": "Secondary User",
            "role": "Team Member",
            "pain_points": pain_points[3:5] if len(pain_points) > 3 else pain_points[:2],
            "goals": goals[3:5] if len(goals) > 3 else goals[:2],
            "tech_savviness": "Medium",
            "usage_frequency": "Weekly"
        })
    
    return personas


def generate_key_user_flows(context: dict) -> list:
    """Generate key user flows using LLM."""
    prompt = f"""Generate 5 key user flows for {context['brand_name']}.

Product Type: {context['product_type']}
User Goals: {context['icp_goals']}

For each flow, provide:
- Flow name
- Steps (3-5 steps)
- Expected outcome

Format as numbered list.
"""
    
    flows_text = generate(prompt, context, max_tokens=600)
    
    # Parse flows
    flows = []
    current_flow = None
    
    for line in flows_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # New flow (starts with number)
        if line[0].isdigit() and "." in line[:3]:
            if current_flow:
                flows.append(current_flow)
            
            flow_name = line.split(".", 1)[1].strip().rstrip(":")
            current_flow = {
                "name": flow_name,
                "steps": [],
                "outcome": ""
            }
        elif current_flow and line.startswith("-"):
            current_flow["steps"].append(line.lstrip("- "))
    
    if current_flow:
        flows.append(current_flow)
    
    # Add outcomes
    for flow in flows:
        flow["outcome"] = f"User successfully completes {flow['name'].lower()}"
    
    return flows[:5]


def generate_feature_list(context: dict) -> dict:
    """Generate feature list categorized by priority."""
    prompt = f"""Generate feature list for {context['brand_name']}.

Value Proposition: {context['value_proposition']}
Themes: {context['brand_themes']}
Product Type: {context['product_type']}

Categorize features into:
- MVP (must-have for launch)
- Phase 2 (important but not critical)
- Future (nice-to-have)

List 5-7 features per category.
Format: Category name, then bullet points.
"""
    
    features_text = generate(prompt, context, max_tokens=800)
    
    # Parse features
    features = {
        "mvp": [],
        "phase_2": [],
        "future": []
    }
    
    current_category = None
    
    for line in features_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        line_lower = line.lower()
        if "mvp" in line_lower or "must-have" in line_lower:
            current_category = "mvp"
        elif "phase 2" in line_lower or "phase two" in line_lower:
            current_category = "phase_2"
        elif "future" in line_lower or "nice-to-have" in line_lower:
            current_category = "future"
        elif line.startswith("-") and current_category:
            feature = line.lstrip("- ").strip()
            if feature:
                features[current_category].append(feature)
    
    return features


def generate_nfr(context: dict) -> dict:
    """Generate non-functional requirements."""
    product_type = context.get("product_type", "SaaS")
    platform = context.get("platform", "web")
    
    nfr = {
        "performance": {
            "page_load": "< 2 seconds",
            "api_response": "< 500ms",
            "concurrent_users": "1000+"
        },
        "security": {
            "authentication": "OAuth 2.0 / JWT",
            "data_encryption": "AES-256 at rest, TLS 1.3 in transit",
            "compliance": "GDPR, SOC 2 Type II"
        },
        "scalability": {
            "architecture": "Microservices / serverless",
            "database": "Horizontally scalable",
            "cdn": "Global edge network"
        },
        "reliability": {
            "uptime": "99.9% SLA",
            "backup": "Daily automated backups",
            "disaster_recovery": "< 4 hour RTO"
        },
        "usability": {
            "accessibility": "WCAG 2.1 AA compliant",
            "mobile_responsive": "Yes" if platform in ["web", "mobile"] else "N/A",
            "browser_support": "Modern browsers (last 2 versions)"
        }
    }
    
    return nfr


def generate_acceptance_criteria(context: dict) -> list:
    """Generate high-level acceptance criteria."""
    criteria = [
        {
            "category": "Functionality",
            "criteria": [
                "All MVP features are implemented and functional",
                "User flows complete without errors",
                "Data persists correctly across sessions"
            ]
        },
        {
            "category": "Performance",
            "criteria": [
                "Page load times meet NFR targets",
                "System handles expected concurrent users",
                "API responses within acceptable latency"
            ]
        },
        {
            "category": "Security",
            "criteria": [
                "Authentication and authorization working",
                "Data encryption implemented",
                "Security audit passed"
            ]
        },
        {
            "category": "User Experience",
            "criteria": [
                "UI matches design specifications",
                "Accessibility standards met",
                "Mobile responsiveness verified"
            ]
        },
        {
            "category": "Quality",
            "criteria": [
                "Unit test coverage > 80%",
                "Integration tests passing",
                "No critical or high-severity bugs"
            ]
        }
    ]
    
    return criteria


def run(params: dict) -> dict:
    """
    Main handler entrypoint.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        {status, output, errors} envelope
    """
    log("info", "prd_generate_start", params_keys=list(params.keys()))
    
    errors = []
    
    # Validate required fields
    required = ["brand_name", "mission", "value_proposition", "icp"]
    for field in required:
        if not params.get(field):
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "prd_generate_validation_failed", errors=errors)
        return {"status": "error", "output": {}, "errors": errors}
    
    # Prepare context
    context = prepare_context(params)
    
    log("info", "prd_generate_processing", brand_name=context["brand_name"])
    
    try:
        # Generate PRD components
        problem_statement = generate_problem_statement(context)
        solution_overview = generate_solution_overview(context)
        user_personas = generate_user_personas(context)
        key_user_flows = generate_key_user_flows(context)
        feature_list = generate_feature_list(context)
        nfr = generate_nfr(context)
        acceptance_criteria = generate_acceptance_criteria(context)
        
        # Construct output
        output = {
            "brand_name": params.get("brand_name"),
            "product_type": params.get("product_type", "SaaS platform"),
            "problem_statement": problem_statement,
            "solution_overview": solution_overview,
            "user_personas": user_personas,
            "key_user_flows": key_user_flows,
            "feature_list": feature_list,
            "non_functional_requirements": nfr,
            "acceptance_criteria": acceptance_criteria,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0",
                "llm_powered": True,
                "components": 7
            }
        }
        
        log("info", "prd_generate_done",
            brand_name=params.get("brand_name"),
            features_count=len(feature_list.get("mvp", [])))
        
        return {
            "status": "success",
            "output": output,
            "errors": []
        }
        
    except Exception as e:
        log("error", "prd_generate_error", error=str(e))
        return {
            "status": "error",
            "output": {},
            "errors": [f"Generation error: {str(e)}"]
        }


def main():
    """CLI entrypoint for testing."""
    try:
        input_data = json.loads(sys.stdin.read())
        result = run(input_data)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        error_result = {
            "status": "error",
            "output": {},
            "errors": [f"Invalid JSON input: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)
    except Exception as e:
        error_result = {
            "status": "error",
            "output": {},
            "errors": [f"Handler error: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
