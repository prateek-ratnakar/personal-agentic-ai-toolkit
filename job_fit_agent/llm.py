"""Thin wrapper around the Claude API. The only file that talks to a model."""
import json
import os

EXTRACT_MODEL = os.environ.get("EXTRACT_MODEL", "claude-haiku-4-5-20251001")  # cheap, fast
TAILOR_MODEL = os.environ.get("TAILOR_MODEL", "claude-sonnet-5")               # better writing


def call_claude(model, system, user, max_tokens=1200):
    """Send one message and return (text, usage). Raises a clear error if no key is set."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Run with --offline, or set the key first "
            "(see README, step 6)."
        )
    import anthropic  # imported here so --offline works without the package

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(block.text for block in msg.content if block.type == "text")
    usage = {"input_tokens": msg.usage.input_tokens, "output_tokens": msg.usage.output_tokens}
    return text, usage


def parse_json(text):
    """Models sometimes wrap JSON in code fences. Strip them before parsing."""
    cleaned = text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)
