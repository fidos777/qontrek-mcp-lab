#!/usr/bin/env python3
"""
L6 Workflow Packager
Combines workflow outputs into a single Workflow Transfer Object (WTO).
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class WorkflowPackager:
    """Packages workflow outputs into standardized WTO format."""
    
    WTO_VERSION = "1.0.0"
    
    def __init__(self):
        """Initialize packager."""
        self.wto_id = str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
        self.workflows_executed = []
        self.total_skills = 0
        
    def create_wto(
        self,
        brand_context: Optional[Dict] = None,
        creative_outputs: Optional[Dict] = None,
        business_outputs: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Workflow Transfer Object from workflow outputs.
        
        Args:
            brand_context: Brand information
            creative_outputs: Creative workflow outputs (slogan, landing_page, etc.)
            business_outputs: Business workflow outputs (architecture, prd, etc.)
            metadata: Additional metadata
            
        Returns:
            Complete WTO dictionary
        """
        wto = {
            "wto_id": self.wto_id,
            "wto_version": self.WTO_VERSION,
            "created_at": self.created_at,
            "brand": brand_context or {},
            "creative": creative_outputs or {},
            "business": business_outputs or {},
            "metadata": self._build_metadata(metadata)
        }
        
        return wto
    
    def add_workflow_output(
        self,
        wto: Dict,
        category: str,
        output_type: str,
        workflow_id: str,
        workflow_output: Dict
    ) -> Dict:
        """
        Add a workflow output to an existing WTO.
        
        Args:
            wto: Existing WTO dictionary
            category: 'creative' or 'business'
            output_type: Type of output (e.g., 'slogan', 'landing_page')
            workflow_id: Workflow identifier
            workflow_output: Workflow execution result
            
        Returns:
            Updated WTO dictionary
        """
        if category not in wto:
            wto[category] = {}
        
        wto[category][output_type] = {
            "workflow_id": workflow_id,
            "executed_at": datetime.now().isoformat(),
            "status": workflow_output.get("status", "unknown"),
            "output": workflow_output.get("outputs", {})
        }
        
        # Update metadata
        if workflow_id not in wto["metadata"]["workflows_executed"]:
            wto["metadata"]["workflows_executed"].append(workflow_id)
            wto["metadata"]["total_workflows_executed"] += 1
        
        # Count skills
        if "outputs" in workflow_output:
            wto["metadata"]["total_skills_executed"] += len(workflow_output["outputs"])
        
        return wto
    
    def package_creative_funnel(self, workflow_output: Dict, brand_context: Dict) -> Dict:
        """
        Package creative_funnel workflow output into WTO.
        
        Args:
            workflow_output: Output from kreator.creative_funnel.v1
            brand_context: Brand information
            
        Returns:
            WTO with creative outputs
        """
        wto = self.create_wto(brand_context=brand_context)
        
        # Extract outputs from workflow
        outputs = workflow_output.get("outputs", {})
        
        # Map to WTO structure
        if "slogan" in outputs:
            wto["creative"]["slogan"] = {
                "workflow_id": "kreator.creative_funnel.v1",
                "executed_at": datetime.now().isoformat(),
                "status": outputs["slogan"].get("status"),
                "output": outputs["slogan"].get("output")
            }
        
        if "landing" in outputs:
            wto["creative"]["landing_page"] = {
                "workflow_id": "kreator.creative_funnel.v1",
                "executed_at": datetime.now().isoformat(),
                "status": outputs["landing"].get("status"),
                "output": outputs["landing"].get("output")
            }
        
        if "socialpack" in outputs:
            wto["creative"]["social_pack"] = {
                "workflow_id": "kreator.creative_funnel.v1",
                "executed_at": datetime.now().isoformat(),
                "status": outputs["socialpack"].get("status"),
                "output": outputs["socialpack"].get("output")
            }
        
        # Update metadata
        wto["metadata"]["workflows_executed"].append("kreator.creative_funnel.v1")
        wto["metadata"]["total_workflows_executed"] = 1
        wto["metadata"]["total_skills_executed"] = len(outputs)
        
        return wto
    
    def merge_wtos(self, wto1: Dict, wto2: Dict) -> Dict:
        """
        Merge two WTOs into one.
        
        Args:
            wto1: First WTO
            wto2: Second WTO
            
        Returns:
            Merged WTO
        """
        merged = wto1.copy()
        
        # Merge creative outputs
        if "creative" in wto2:
            if "creative" not in merged:
                merged["creative"] = {}
            merged["creative"].update(wto2["creative"])
        
        # Merge business outputs
        if "business" in wto2:
            if "business" not in merged:
                merged["business"] = {}
            merged["business"].update(wto2["business"])
        
        # Merge metadata
        if "metadata" in wto2:
            merged["metadata"]["workflows_executed"].extend(
                wto2["metadata"].get("workflows_executed", [])
            )
            merged["metadata"]["total_workflows_executed"] += wto2["metadata"].get(
                "total_workflows_executed", 0
            )
            merged["metadata"]["total_skills_executed"] += wto2["metadata"].get(
                "total_skills_executed", 0
            )
        
        return merged
    
    def save_wto(self, wto: Dict, output_path: str) -> str:
        """
        Save WTO to JSON file.
        
        Args:
            wto: WTO dictionary
            output_path: File path to save to
            
        Returns:
            Path to saved file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(wto, f, indent=2)
        
        return str(output_file)
    
    def load_wto(self, input_path: str) -> Dict:
        """
        Load WTO from JSON file.
        
        Args:
            input_path: File path to load from
            
        Returns:
            WTO dictionary
        """
        with open(input_path, 'r') as f:
            return json.load(f)
    
    def validate_wto(self, wto: Dict) -> tuple[bool, List[str]]:
        """
        Validate WTO structure.
        
        Args:
            wto: WTO dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        required_fields = ["wto_id", "wto_version", "created_at"]
        for field in required_fields:
            if field not in wto:
                errors.append(f"Missing required field: {field}")
        
        # Check version format
        if "wto_version" in wto:
            version = wto["wto_version"]
            parts = version.split(".")
            if len(parts) != 3 or not all(p.isdigit() for p in parts):
                errors.append(f"Invalid version format: {version}")
        
        # Check categories
        valid_categories = ["brand", "creative", "business", "metadata"]
        for category in wto.keys():
            if category not in valid_categories and category not in required_fields:
                errors.append(f"Unknown category: {category}")
        
        return (len(errors) == 0, errors)
    
    def _build_metadata(self, custom_metadata: Optional[Dict] = None) -> Dict:
        """Build metadata section."""
        metadata = {
            "total_workflows_executed": 0,
            "total_skills_executed": 0,
            "execution_time_ms": 0,
            "workflows_executed": [],
            "tags": [],
            "custom_fields": custom_metadata or {}
        }
        return metadata


def package_workflow_output(
    workflow_id: str,
    workflow_output: Dict,
    brand_context: Optional[Dict] = None
) -> Dict:
    """
    Convenience function to package a single workflow output.
    
    Args:
        workflow_id: Workflow identifier
        workflow_output: Workflow execution result
        brand_context: Optional brand context
        
    Returns:
        WTO dictionary
    """
    packager = WorkflowPackager()
    
    if workflow_id == "kreator.creative_funnel.v1":
        return packager.package_creative_funnel(workflow_output, brand_context or {})
    
    # Generic packaging for other workflows
    wto = packager.create_wto(brand_context=brand_context)
    
    # Determine category from workflow_id
    if "kreator" in workflow_id or "creative" in workflow_id:
        category = "creative"
    elif "business" in workflow_id or "arkitek" in workflow_id:
        category = "business"
    else:
        category = "creative"  # default
    
    # Add workflow output
    output_type = workflow_id.split(".")[-2] if "." in workflow_id else workflow_id
    wto = packager.add_workflow_output(
        wto, category, output_type, workflow_id, workflow_output
    )
    
    return wto


# Example usage
if __name__ == "__main__":
    # Example: Package a creative funnel output
    packager = WorkflowPackager()
    
    brand = {
        "brand_name": "FlowMind",
        "industry": "SaaS",
        "target_audience": "Remote workers",
        "brand_values": ["efficiency", "simplicity"]
    }
    
    workflow_result = {
        "workflow": "kreator.creative_funnel.v1",
        "status": "success",
        "outputs": {
            "slogan": {
                "status": "success",
                "output": {"slogans": [{"text": "Work Smarter"}]}
            }
        }
    }
    
    wto = packager.package_creative_funnel(workflow_result, brand)
    print(json.dumps(wto, indent=2))
