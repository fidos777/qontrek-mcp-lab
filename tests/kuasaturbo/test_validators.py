"""
Test KuasaTurbo Request Validators
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.api.validators import validate_service_request


def test_valid_service_request():
    """Test validation with valid service and payload"""
    result = validate_service_request(
        service_id="content_idea",
        payload={
            "topic": "AI automation",
            "audience": "SME owners",
            "platform": "tiktok"
        }
    )
    assert result["valid"] == True
    assert len(result["errors"]) == 0
    assert "service" in result
    print("✓ Valid service request accepted")


def test_missing_service():
    """Test validation with non-existent service"""
    result = validate_service_request(
        service_id="nonexistent_service",
        payload={}
    )
    assert result["valid"] == False
    assert len(result["errors"]) > 0
    assert "not found" in result["errors"][0].lower()
    print("✓ Missing service rejected")


def test_missing_required_field():
    """Test validation with missing required field"""
    result = validate_service_request(
        service_id="content_idea",
        payload={
            "topic": "AI automation"
            # Missing required fields: audience, platform
        }
    )
    assert result["valid"] == False
    assert len(result["errors"]) > 0
    print("✓ Missing required field rejected")


def test_invalid_persona_override():
    """Test validation with invalid persona override"""
    result = validate_service_request(
        service_id="content_idea",
        payload={
            "topic": "AI automation",
            "audience": "SME owners",
            "platform": "tiktok"
        },
        persona_override="nonexistent_persona.v1"
    )
    assert result["valid"] == False
    assert len(result["errors"]) > 0
    print("✓ Invalid persona override rejected")


if __name__ == "__main__":
    test_valid_service_request()
    test_missing_service()
    test_missing_required_field()
    test_invalid_persona_override()
    print("\n✅ All validator tests passed")
