import json
import os
from typing import Any, Dict
from litellm import completion
# See https://docs.litellm.ai/docs/ for reference.

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

# Name of the environment variable that should contain your Groq / LLM API key.
API_KEY_ENV_VAR = "GROQ_API_KEY"



def _validate_itinerary_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic schema validation for the itinerary JSON.

    Ensures all required fields are present and of expected types.
    """
    required_fields = ["destination", "price_range", "ideal_visit_times", "top_attractions"]

    if not isinstance(data, dict):
        raise ValueError("LLM response is not a JSON object.")

    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f"LLM response missing required fields: {', '.join(missing)}")

    if not isinstance(data["destination"], str):
        raise ValueError("Field 'destination' must be a string.")

    if not isinstance(data["price_range"], str):
        raise ValueError("Field 'price_range' must be a string.")

    if not isinstance(data["ideal_visit_times"], list):
        raise ValueError("Field 'ideal_visit_times' must be a list.")

    if not isinstance(data["top_attractions"], list):
        raise ValueError("Field 'top_attractions' must be a list.")

    return data


def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    destination = destination.strip()
    if not destination:
        raise ValueError("Destination must be a non-empty string.")

    api_key = _load_api_key()

    system_prompt = (
        "You are a helpful travel assistant. "
        "Only respond with a single JSON object that matches this schema:\n"
        "{\n"
        '  "destination": string,\n'
        '  "price_range": string,\n'
        '  "ideal_visit_times": string[],\n'
        '  "top_attractions": string[]\n'
        "}\n"
        "Do not include any extra keys or text outside the JSON."
    )

    user_prompt = (
        f"Create a concise travel itinerary overview for {destination}. "
        "Fill in the JSON fields with appropriate values."
    )

    # See https://docs.litellm.ai/docs/ for reference.
    response = completion(
        model=MODEL,
        api_key=api_key,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    # LiteLLM returns an OpenAI-style response object.
    message = response.choices[0].message
    content = message.get("content") if isinstance(message, dict) else getattr(message, "content", "")

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM did not return valid JSON: {exc}") from exc

    return _validate_itinerary_schema(parsed)
