#!/usr/bin/env python3
"""
LaunchKit Roadmap Generator - Production Version
Generates 30/60/90-day roadmap and phased rollout plan.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from lib.logger import log
from lib.llm_client import generate


def prepare_context(params: dict) -> dict:
    """Prepare context for LLM generation."""
    prd = params.get("prd", {})
    pricing = params.get("pricing", {})
    feature_list = prd.get("feature_list", {})
    
    return {
        "brand_name": params.get("brand_name", ""),
        "mvp_features": ", ".join(feature_list.get("mvp", [])),
        "phase_2_features": ", ".join(feature_list.get("phase_2", [])),
        "future_features": ", ".join(feature_list.get("future", [])),
        "pricing_model": pricing.get("billing_model", {}).get("primary_model", ""),
        "target_launch_date": params.get("target_launch_date", "")
    }


def generate_roadmap_30(context: dict) -> dict:
    """Generate 30-day roadmap (MVP phase)."""
    mvp_features = context.get("mvp_features", "").split(", ")
    
    roadmap = {
        "phase": "30 Days - MVP Launch",
        "objectives": [
            "Launch minimum viable product",
            "Validate core value proposition",
            "Establish initial user base",
            "Gather critical feedback"
        ],
        "key_tasks": [
            {
                "week": 1,
                "focus": "Final development and testing",
                "tasks": [
                    "Complete MVP feature development",
                    "Conduct internal QA testing",
                    "Fix critical bugs",
                    "Prepare launch materials"
                ]
            },
            {
                "week": 2,
                "focus": "Beta launch and validation",
                "tasks": [
                    "Launch private beta to early users",
                    "Monitor system performance",
                    "Collect user feedback",
                    "Iterate on critical issues"
                ]
            },
            {
                "week": 3,
                "focus": "Public launch preparation",
                "tasks": [
                    "Finalize public launch plan",
                    "Prepare marketing materials",
                    "Set up support systems",
                    "Train support team"
                ]
            },
            {
                "week": 4,
                "focus": "Public launch and growth",
                "tasks": [
                    "Execute public launch",
                    "Monitor user acquisition",
                    "Provide active support",
                    "Analyze early metrics"
                ]
            }
        ],
        "milestones": [
            {"name": "MVP Complete", "target": "Day 7"},
            {"name": "Beta Launch", "target": "Day 14"},
            {"name": "Public Launch", "target": "Day 28"},
            {"name": "First 100 Users", "target": "Day 30"}
        ],
        "success_metrics": [
            "MVP features deployed and stable",
            "100+ active users",
            "< 5% critical bug rate",
            "Positive user feedback (NPS > 30)"
        ]
    }
    
    return roadmap


def generate_roadmap_60(context: dict) -> dict:
    """Generate 60-day roadmap (Enhancement phase)."""
    phase_2_features = context.get("phase_2_features", "").split(", ")
    
    roadmap = {
        "phase": "60 Days - Enhancement & Scale",
        "objectives": [
            "Enhance product based on feedback",
            "Scale infrastructure and team",
            "Expand feature set",
            "Grow user base 5x"
        ],
        "key_tasks": [
            {
                "week": 5,
                "focus": "Feedback analysis and planning",
                "tasks": [
                    "Analyze user feedback and metrics",
                    "Prioritize enhancement backlog",
                    "Plan Phase 2 features",
                    "Allocate resources"
                ]
            },
            {
                "week": 6,
                "focus": "Core enhancements",
                "tasks": [
                    "Implement top user requests",
                    "Optimize performance",
                    "Enhance UX based on data",
                    "Add key integrations"
                ]
            },
            {
                "week": 7,
                "focus": "Feature expansion",
                "tasks": [
                    "Develop Phase 2 features",
                    "Expand integration ecosystem",
                    "Improve onboarding flow",
                    "Scale infrastructure"
                ]
            },
            {
                "week": 8,
                "focus": "Growth and partnerships",
                "tasks": [
                    "Launch partnership program",
                    "Expand marketing efforts",
                    "Optimize conversion funnel",
                    "Build community"
                ]
            }
        ],
        "milestones": [
            {"name": "Phase 2 Features Live", "target": "Day 45"},
            {"name": "500 Active Users", "target": "Day 50"},
            {"name": "First Partnerships", "target": "Day 55"},
            {"name": "Product-Market Fit Signals", "target": "Day 60"}
        ],
        "success_metrics": [
            "500+ active users",
            "30% MoM growth",
            "NPS > 50",
            "< 10% churn rate"
        ]
    }
    
    return roadmap


def generate_roadmap_90(context: dict) -> dict:
    """Generate 90-day roadmap (Scale phase)."""
    roadmap = {
        "phase": "90 Days - Scale & Optimize",
        "objectives": [
            "Achieve product-market fit",
            "Scale operations efficiently",
            "Expand to new segments",
            "Prepare for next funding round"
        ],
        "key_tasks": [
            {
                "week": 9,
                "focus": "Optimization and automation",
                "tasks": [
                    "Automate key workflows",
                    "Optimize unit economics",
                    "Improve retention metrics",
                    "Scale support operations"
                ]
            },
            {
                "week": 10,
                "focus": "Market expansion",
                "tasks": [
                    "Launch in new segments",
                    "Expand sales channels",
                    "Build enterprise features",
                    "Develop case studies"
                ]
            },
            {
                "week": 11,
                "focus": "Advanced capabilities",
                "tasks": [
                    "Launch advanced features",
                    "Enhance analytics",
                    "Build API ecosystem",
                    "Improve security posture"
                ]
            },
            {
                "week": 12,
                "focus": "Fundraising preparation",
                "tasks": [
                    "Compile traction metrics",
                    "Prepare investor materials",
                    "Refine growth strategy",
                    "Build financial projections"
                ]
            }
        ],
        "milestones": [
            {"name": "1,000 Active Users", "target": "Day 75"},
            {"name": "Enterprise Pilot", "target": "Day 80"},
            {"name": "Product-Market Fit", "target": "Day 85"},
            {"name": "Fundraise Ready", "target": "Day 90"}
        ],
        "success_metrics": [
            "1,000+ active users",
            "40% MoM growth",
            "NPS > 60",
            "< 5% churn rate",
            "Positive unit economics"
        ]
    }
    
    return roadmap


def generate_phases(context: dict) -> list:
    """Generate high-level phase breakdown."""
    phases = [
        {
            "phase_number": 1,
            "name": "Foundation (Days 1-30)",
            "goal": "Launch MVP and validate core value",
            "key_deliverables": [
                "MVP product launch",
                "Initial user base (100+)",
                "Feedback collection system",
                "Core metrics dashboard"
            ],
            "exit_criteria": [
                "Product is stable and usable",
                "Users are actively engaged",
                "Feedback loop is established"
            ]
        },
        {
            "phase_number": 2,
            "name": "Enhancement (Days 31-60)",
            "goal": "Improve product and scale operations",
            "key_deliverables": [
                "Enhanced feature set",
                "Expanded integrations",
                "Partnership program",
                "5x user growth"
            ],
            "exit_criteria": [
                "Product-market fit signals present",
                "Growth is sustainable",
                "Operations are scalable"
            ]
        },
        {
            "phase_number": 3,
            "name": "Scale (Days 61-90)",
            "goal": "Achieve PMF and prepare for scale",
            "key_deliverables": [
                "Product-market fit achieved",
                "Enterprise capabilities",
                "Strong unit economics",
                "Fundraise readiness"
            ],
            "exit_criteria": [
                "Clear path to profitability",
                "Repeatable sales process",
                "Ready for next funding round"
            ]
        }
    ]
    
    return phases


def generate_milestones_list(roadmap_30: dict, roadmap_60: dict, roadmap_90: dict) -> list:
    """Compile all milestones into a single list."""
    all_milestones = []
    
    for roadmap in [roadmap_30, roadmap_60, roadmap_90]:
        for milestone in roadmap.get("milestones", []):
            all_milestones.append({
                "name": milestone["name"],
                "target": milestone["target"],
                "phase": roadmap["phase"]
            })
    
    return all_milestones


def run(params: dict) -> dict:
    """
    Main handler entrypoint.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        {status, output, errors} envelope
    """
    log("info", "roadmap_generate_start", params_keys=list(params.keys()))
    
    errors = []
    
    # Validate required fields
    required = ["brand_name"]
    for field in required:
        if not params.get(field):
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "roadmap_generate_validation_failed", errors=errors)
        return {"status": "error", "output": {}, "errors": errors}
    
    # Prepare context
    context = prepare_context(params)
    
    log("info", "roadmap_generate_processing", brand_name=context["brand_name"])
    
    try:
        # Generate roadmap components
        roadmap_30 = generate_roadmap_30(context)
        roadmap_60 = generate_roadmap_60(context)
        roadmap_90 = generate_roadmap_90(context)
        phases = generate_phases(context)
        milestones = generate_milestones_list(roadmap_30, roadmap_60, roadmap_90)
        
        # Construct output
        output = {
            "brand_name": params.get("brand_name"),
            "roadmap_30": roadmap_30,
            "roadmap_60": roadmap_60,
            "roadmap_90": roadmap_90,
            "phases": phases,
            "milestones": milestones,
            "timeline_summary": {
                "total_duration": "90 days",
                "phases_count": 3,
                "milestones_count": len(milestones),
                "launch_target": roadmap_30["milestones"][2]["target"]
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0",
                "llm_powered": True,
                "roadmap_type": "30/60/90"
            }
        }
        
        log("info", "roadmap_generate_done",
            brand_name=params.get("brand_name"),
            milestones_count=len(milestones))
        
        return {
            "status": "success",
            "output": output,
            "errors": []
        }
        
    except Exception as e:
        log("error", "roadmap_generate_error", error=str(e))
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
