"""
KuasaTurbo Prompt Builder

Builds AI prompts from workflow + persona + payload.
"""


def build_prompt(workflow: dict, persona: dict, payload: dict) -> dict:
    """
    Build AI prompt from workflow, persona, and user input
    
    Args:
        workflow: Workflow definition
        persona: Persona definition (simplified schema)
        payload: User input (widget fields)
    
    Returns:
        {
            "prompt": str,
            "system_context": str,
            "user_input": dict
        }
    """
    # Extract persona context (simplified schema)
    persona_name = persona['persona_name']
    persona_role = persona['role']
    tone_style = persona['tone_style']
    language = persona['language']
    traits = ', '.join(persona['traits'])
    
    # Build language instruction
    if language == "bilingual":
        language_instruction = "Use a mix of English and Bahasa Malaysia naturally."
    else:
        language_instruction = "Use primarily English."
    
    # Build system context
    system_context = f"""You are {persona_name}, a {persona_role}.

Traits: {traits}
Tone: {tone_style}
Language: {language_instruction}

Generate output that matches this persona's style and characteristics.
"""
    
    # Get workflow step (assume single-step for KuasaTurbo)
    step = workflow['steps'][0]
    prompt_template = step.get('prompt_template', '')
    
    # Replace placeholders in prompt template
    prompt = prompt_template
    for key, value in payload.items():
        placeholder = f"{{{{{key}}}}}"
        prompt = prompt.replace(placeholder, str(value))
    
    # Build full prompt
    full_prompt = f"""{system_context}

Task: {workflow['description']}

User Input:
{prompt}

Generate the output according to the workflow requirements."""
    
    return {
        "prompt": full_prompt,
        "system_context": system_context,
        "user_input": payload
    }
