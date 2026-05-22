"""
IBM watsonx.ai client for generating onboarding kits.
Falls back to Groq (Llama 3.3 70B) if watsonx is unavailable.
"""

import os
import json
from typing import Dict


def _parse_kit(response: str) -> Dict:
    response = response.strip()
    if response.startswith("```"):
        lines = response.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response = "\n".join(lines).strip()

    first_brace = response.find("{")
    if first_brace == -1:
        raise ValueError("No JSON object found in model response")

    try:
        kit, _ = json.JSONDecoder().raw_decode(response, first_brace)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {str(e)}")

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


def _generate_with_watsonx(prompt: str) -> str:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    credentials = Credentials(
        url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        api_key=os.getenv("WATSONX_API_KEY"),
    )
    model = ModelInference(
        model_id="meta-llama/llama-3-3-70b-instruct",
        credentials=credentials,
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            "max_new_tokens": 4096,
            "temperature": 0.1,
            "top_p": 0.85,
        },
    )
    return model.generate_text(prompt=prompt)


def _generate_with_groq(prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.1,
    )
    return completion.choices[0].message.content


def generate_onboarding_kit(prompt: str) -> Dict:
    """
    Generate an onboarding kit using IBM watsonx.ai, falling back to Groq if unavailable.
    """
    watsonx_key = os.getenv("WATSONX_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if watsonx_key:
        try:
            response = _generate_with_watsonx(prompt)
            return _parse_kit(response)
        except Exception as e:
            if not groq_key:
                raise
            print(f"[watsonx fallback] watsonx failed: {e} — retrying with Groq")

    if groq_key:
        response = _generate_with_groq(prompt)
        return _parse_kit(response)

    raise RuntimeError("No AI provider available — set WATSONX_API_KEY or GROQ_API_KEY")

# Made with Bob
