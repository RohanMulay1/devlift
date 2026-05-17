"""
IBM watsonx.ai client for generating onboarding kits.
Wraps the Granite model API and handles JSON parsing.
"""

import os
import json
from typing import Dict
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference


def _get_model() -> ModelInference:
    """
    Initialize and return a ModelInference instance for Granite model.
    
    Returns:
        Configured ModelInference instance
    """
    credentials = Credentials(
        url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        api_key=os.getenv("WATSONX_API_KEY"),
    )
    
    return ModelInference(
        model_id="meta-llama/llama-3-3-70b-instruct",
        credentials=credentials,
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            "max_new_tokens": 4096,
            "temperature": 0.1,
            "top_p": 0.85,
        },
    )


def generate_onboarding_kit(prompt: str) -> Dict:
    """
    Generate an onboarding kit using IBM watsonx.ai Granite model.
    
    Args:
        prompt: Formatted prompt containing repository context
        
    Returns:
        Dictionary containing the parsed onboarding kit
        
    Raises:
        ValueError: If required keys are missing from the response
        Exception: If model call or JSON parsing fails
    """
    model = _get_model()
    
    # Generate response
    response = model.generate_text(prompt=prompt)
    
    # Clean up response
    response = response.strip()
    
    # Strip markdown code fences if present
    if response.startswith("```"):
        # Handle both ```json and ``` variants
        lines = response.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]  # Remove opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # Remove closing fence
        response = "\n".join(lines).strip()
    
    # Find the first { and parse exactly one JSON object from that point.
    # raw_decode stops at the end of the first complete object, ignoring any
    # trailing text the model may have generated after the closing brace.
    first_brace = response.find("{")
    if first_brace == -1:
        raise ValueError("No JSON object found in model response")

    try:
        kit, _ = json.JSONDecoder().raw_decode(response, first_brace)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {str(e)}")
    
    # Validate required keys
    required_keys = [
        "architecture_overview",
        "key_components",
        "complexity_hotspots",
        "suggested_first_tasks",
        "common_patterns",
        "setup_summary"
    ]
    
    missing_keys = [key for key in required_keys if key not in kit]
    if missing_keys:
        raise ValueError(f"Missing required keys in response: {', '.join(missing_keys)}")
    
    return kit

# Made with Bob
