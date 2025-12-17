"""
Test KuasaTurbo Service Execution (End-to-End)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from starlette.testclient import TestClient
from kuasaturbo.api.gateway import app

client = TestClient(app)


def test_execute_content_idea_service():
    """Test content idea service execution"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "content_idea",
            "payload": {
                "topic": "AI automation",
                "audience": "SME owners",
                "platform": "tiktok"
            },
            "model": "mock"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["service_id"] == "content_idea"
    assert "output" in data
    assert "ideas" in data["output"]
    print("✓ Content idea service executed")


def test_execute_caption_builder_service():
    """Test caption builder service execution"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "caption_builder",
            "payload": {
                "post_topic": "AI tools for business",
                "tone": "playful",
                "platform": "instagram",
                "include_hashtags": True
            },
            "model": "mock"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "captions" in data["output"]
    print("✓ Caption builder service executed")


def test_execute_lead_intake_service():
    """Test lead intake service execution"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "lead_intake",
            "payload": {
                "full_name": "Ahmad Ibrahim",
                "phone": "0123456789",
                "interest": "Solar panel installation",
                "source": "facebook_ads"
            },
            "model": "mock"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "lead_summary" in data["output"]
    assert "suggested_reply" in data["output"]
    print("✓ Lead intake service executed")


def test_invalid_api_key():
    """Test request with invalid API key"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "invalid_key"},
        json={
            "service_id": "content_idea",
            "payload": {
                "topic": "AI automation",
                "audience": "SME owners",
                "platform": "tiktok"
            }
        }
    )
    
    assert response.status_code == 401
    print("✓ Invalid API key rejected")


def test_missing_required_field():
    """Test request with missing required field"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "content_idea",
            "payload": {
                "topic": "AI automation"
                # Missing: audience, platform
            }
        }
    )
    
    assert response.status_code == 400
    print("✓ Missing required field rejected")


def test_persona_override():
    """Test service execution with persona override"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "content_idea",
            "payload": {
                "topic": "AI automation",
                "audience": "SME owners",
                "platform": "tiktok"
            },
            "persona_override": "jordan_cfo_analyst.v1"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["persona_id"] == "jordan_cfo_analyst.v1"
    print("✓ Persona override working")


def test_model_override():
    """Test service execution with model override"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "content_idea",
            "payload": {
                "topic": "AI automation",
                "audience": "SME owners",
                "platform": "tiktok"
            },
            "model_override": "claude-3.7"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Model used should be reflected in metadata
    assert data["metadata"]["model"] == "claude-3.7"
    print("✓ Model override working")


def test_invalid_model_override():
    """Test service execution with invalid model override"""
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "kuasa123"},
        json={
            "service_id": "content_idea",
            "payload": {
                "topic": "AI automation",
                "audience": "SME owners",
                "platform": "tiktok"
            },
            "model_override": "invalid-model-xyz"
        }
    )
    
    assert response.status_code == 400
    print("✓ Invalid model override rejected")


if __name__ == "__main__":
    test_execute_content_idea_service()
    test_execute_caption_builder_service()
    test_execute_lead_intake_service()
    test_invalid_api_key()
    test_missing_required_field()
    test_persona_override()
    test_model_override()
    test_invalid_model_override()
    print("\n✅ All service execution tests passed")
