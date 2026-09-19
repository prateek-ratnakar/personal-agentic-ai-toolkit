"""Box 2 - Extract (LLM). Turns messy JD text into fixed fields.
Why an LLM here: JDs are free text in a hundred formats. Why fixed fields:
the next step is plain code and needs the same shape every time."""
from .llm import EXTRACT_MODEL, call_claude, parse_json

SYSTEM = """You read job descriptions and return ONLY a JSON object, no other text.
Fields:
- title: string, the role title as written
- function: one of "program management", "technical program management",
  "product management", "ai product management", "strategy and operations",
  "founders office", "chief of staff", "engineering", "sales", "other"
- domain: short lowercase phrase for the industry, e.g. "fintech", "e-commerce", "healthcare"
- min_years: integer minimum years of experience asked for, or null if not stated
- level_words: list of seniority words in the title or text, e.g. ["senior", "principal", "director"]
- required_skills: list of up to 15 short lowercase skill phrases the JD requires
- ai_signal: one of "core" (AI is the job), "some" (AI mentioned as a tool), "none"
If a field is not in the text, use null or an empty list. Never guess a number."""


def extract(jd_text):
    text, usage = call_claude(EXTRACT_MODEL, SYSTEM, jd_text, max_tokens=800)
    return parse_json(text), usage
