"""
KuasaTurbo AI Client

Mock/Simulation mode for AI generation with multi-model routing.
All models run in MOCK MODE (no external API calls).
"""

from typing import Dict, Any
import json
from kuasaturbo.services.model_router import get_provider


def generate_output(
    prompt: str,
    workflow: dict,
    persona: dict,
    model: str = "mock"
) -> Dict[str, Any]:
    """
    Generate AI output (mock mode with routing)
    
    Args:
        prompt: Full prompt with system context
        workflow: Workflow definition
        persona: Persona definition
        model: Model identifier (routed model)
    
    Returns:
        Structured output matching workflow output_schema
    """
    # Get provider for the model
    provider = get_provider(model)
    
    print(f"[AI Client] Using model: {model} (provider: {provider})")
    
    # Get expected output schema from workflow
    output_schema = workflow.get('output_schema', {})
    workflow_id = workflow.get('id', 'unknown')
    
    # Route to appropriate generator based on provider
    if provider == "internal":
        # Use internal mock generator
        return _generate_mock_output(workflow_id, output_schema, persona, model)
    elif provider in ["openai", "anthropic", "google", "groq"]:
        # Simulate external provider (still mock mode, no API calls)
        print(f"[AI Client] Simulating {provider} response (mock mode)")
        return _generate_mock_output(workflow_id, output_schema, persona, model)
    else:
        # Unknown provider, fall back to mock
        print(f"[AI Client] Unknown provider '{provider}', using mock mode")
        return _generate_mock_output(workflow_id, output_schema, persona, model)


def _generate_mock_output(workflow_id: str, output_schema: dict, persona: dict, model: str = "mock") -> Dict[str, Any]:
    """
    Generate realistic mock output based on workflow type
    
    Args:
        workflow_id: Workflow identifier
        output_schema: Expected output structure
        persona: Persona for tone/style reference (simplified schema)
    
    Returns:
        Mock output matching schema
    """
    persona_name = persona['persona_name']
    
    # Content Idea Workflow
    if 'content_idea' in workflow_id:
        return {
            "ideas": [
                "10 cara AI boleh automate bisnes SME - jom tengok!",
                "Rahsia scale bisnes tanpa tambah staff - AI power!",
                "From manual to magic: AI transformation story",
                "Boss SME wajib tahu - AI tools yang senang guna",
                "Automation hacks untuk bisnes kecil - game changer!",
                "AI bukan untuk tech company je - SME pun boleh!",
                "Save 10 jam seminggu dengan AI - here's how",
                "Budget kecil, impact besar - AI tools for SMEs",
                "Real talk: AI implementation untuk bisnes Malaysia",
                "Future-proof your SME dengan AI automation"
            ]
        }
    
    # Caption Builder Workflow
    elif 'caption_builder' in workflow_id:
        return {
            "captions": [
                {
                    "hook": "Korang rasa AI ni mahal? Think again! 💡",
                    "body": "SME owners, listen up! AI automation bukan untuk big corp je. Even with small budget, you can automate repetitive tasks and focus on growing your business. The future is NOW! 🚀",
                    "cta": "Drop 'INTERESTED' if nak tahu more!",
                    "hashtags": "#AIForSME #AutomationMalaysia #SmartBusiness"
                },
                {
                    "hook": "Tired of doing the same tasks every day? 😴",
                    "body": "Let AI handle the boring stuff while you focus on what matters - growing your empire! Automation is the secret weapon of successful SMEs. Time to level up! 💪",
                    "cta": "Comment 'YES' untuk free consultation!",
                    "hashtags": "#BusinessAutomation #SMEMalaysia #ProductivityHacks"
                },
                {
                    "hook": "Real talk: AI saved me 10 hours per week ⏰",
                    "body": "As an SME owner, every hour counts. AI automation transformed how I run my business - from manual chaos to smooth operations. If I can do it, you can too! 🎯",
                    "cta": "Share this with a business owner who needs this!",
                    "hashtags": "#EntrepreneurLife #AITransformation #BusinessGrowth"
                }
            ]
        }
    
    # Invoice Generator Workflow
    elif 'invoice_gen' in workflow_id:
        return {
            "invoice_text": "INVOICE\n\nBill To: [Client Name]\nService: [Service Description]\nAmount: RM [Amount]\nDue Date: [Due Date]\n\nPayment Details:\nBank: [Your Bank]\nAccount: [Your Account]\n\nThank you for your business!",
            "payment_note": "Payment is due by [Due Date]. Please include invoice number in payment reference."
        }
    
    # Lead Intake Workflow
    elif 'lead_intake' in workflow_id:
        return {
            "lead_summary": f"New lead captured successfully. {persona_name} will follow up with personalized consultation.",
            "suggested_reply": "Hi [Name]! Thanks for your interest. I'm excited to learn more about your needs. When would be a good time for a quick chat? Looking forward to helping you! 😊"
        }
    
    # Trade-In Evaluation Workflow
    elif 'tradein_eval' in workflow_id:
        return {
            "evaluation_note": "Vehicle details recorded. Based on initial info, this looks like a solid trade-in candidate. Recommend in-person inspection for accurate valuation.",
            "customer_reply": "Thanks for the details! Your [Vehicle Make] [Vehicle Model] looks interesting. Let's schedule an inspection to give you the best trade-in value. When can you come by? 🚗",
            "next_steps": [
                "Schedule inspection appointment",
                "Prepare vehicle documents",
                "Review current market value",
                "Present trade-in offer"
            ]
        }
    
    # Loan Check Workflow
    elif 'loancheck' in workflow_id:
        return {
            "assessment_narrative": "Based on the information provided, preliminary assessment shows potential eligibility. Monthly income appears sufficient for the requested loan amount. Recommend proceeding with full application and document verification.",
            "document_checklist": [
                "Latest 3 months payslips",
                "Bank statements (6 months)",
                "IC copy (front & back)",
                "Latest EA/BE form",
                "Existing loan statements (if any)"
            ],
            "disclaimers": [
                "This is an indicative assessment only",
                "Final approval subject to bank's credit evaluation",
                "Interest rates and terms may vary",
                "Additional documents may be required"
            ]
        }
    
    # Attendance Workflow
    elif 'attendance' in workflow_id:
        return {
            "attendance_summary": "Attendance recorded successfully. Employee status updated in local system.",
            "manager_note": "Attendance logged for [Employee Name] (ID: [Employee ID]). Action: [Action]. All records up to date. 📋"
        }
    
    # Menu Update Workflow
    elif 'menu_update' in workflow_id:
        return {
            "menu_description": "Delicious [Item Name] - a perfect blend of flavors that will make your taste buds dance! Freshly prepared with quality ingredients. Available now at [Category] section. 🍽️",
            "promo_caption": "NEW on the menu! 🎉 Try our amazing [Item Name] - you won't regret it! Perfect for [occasion]. Come taste the difference today! Limited time offer at RM [Price]. Tag someone who needs to try this! 😋 #FoodieHeaven #NewMenu #MustTry"
        }
    
    # Default fallback
    else:
        return {
            "result": f"Mock output generated by {persona_name}",
            "message": "This is a simulated response. Real AI integration coming soon!",
            "workflow_id": workflow_id
        }


def get_supported_models() -> list:
    """
    Get list of supported models
    
    Returns:
        List of model identifiers
    """
    return [
        "mock",
        # Future models:
        # "gpt-4",
        # "gpt-3.5-turbo",
        # "claude-3-opus",
        # "claude-3-sonnet",
        # "gemini-pro"
    ]


def validate_model(model: str) -> bool:
    """
    Check if model is supported
    
    Args:
        model: Model identifier
    
    Returns:
        True if supported, False otherwise
    """
    return model in get_supported_models()
