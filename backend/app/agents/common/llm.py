"""LiteLLM wrapper for configurable LLM access."""
import litellm
from app.config import get_settings

settings = get_settings()

# Configure LiteLLM
litellm.set_verbose = False


async def call_llm(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> str:
    model = model or settings.LITELLM_MODEL
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=120,
            num_retries=2,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}") from e


async def call_llm_json(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
) -> dict:
    """Call LLM with JSON response format."""
    import json

    model = model or settings.LITELLM_MODEL
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            timeout=120,
            num_retries=2,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"LLM returned invalid JSON: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}") from e
