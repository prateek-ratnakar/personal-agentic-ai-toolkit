"""Box 4 - Tailor (LLM). Picks and adapts bullets, using ONLY the achievement bank."""
from .llm import TAILOR_MODEL, call_claude

SYSTEM = """You tailor resume bullets for one job description.
Rules:
1. Use ONLY facts and numbers that appear in the ACHIEVEMENT BANK. Never invent,
   round, or combine numbers.
2. Return exactly 4 bullets, one per line, each starting with "- ".
3. Lead each bullet with the outcome, then how. Plain ASCII only.
4. If the bank has nothing relevant for a requirement, skip it rather than stretch."""


def tailor(jd_text, bank_text):
    user = f"ACHIEVEMENT BANK:\n{bank_text}\n\nJOB DESCRIPTION:\n{jd_text}"
    return call_claude(TAILOR_MODEL, SYSTEM, user, max_tokens=700)
