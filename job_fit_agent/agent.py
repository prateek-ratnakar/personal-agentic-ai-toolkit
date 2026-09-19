"""Run the full pipeline on one JD file.

Usage:
  python -m job_fit_agent.agent examples/sample_jd.txt --offline   (no API key needed)
  python -m job_fit_agent.agent path/to/jd.txt                     (live, uses Claude)
"""
import argparse
import json
import os
import time

from . import grounding, score
from .gate import ask_and_log


def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def bank_path():
    return "data/my_bank.md" if os.path.exists("data/my_bank.md") else "data/bank_example.md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jd_file")
    ap.add_argument("--offline", action="store_true", help="use saved model outputs from examples/")
    ap.add_argument("--no-gate", action="store_true", help="skip the approval prompt")
    args = ap.parse_args()

    jd = load(args.jd_file)
    bank = load(bank_path())
    profile = json.loads(load("data/profile.json"))
    t0 = time.time()

    # Box 2 - Extract
    if args.offline:
        fields = json.loads(load("examples/sample_extract.json"))
    else:
        from .extract import extract
        fields, usage = extract(jd)
        print(f"[extract] tokens in/out: {usage['input_tokens']}/{usage['output_tokens']}")
    print("\n== Extracted fields ==")
    print(json.dumps(fields, indent=2))

    # Box 3 - Score
    result = score.score(fields, profile)
    print("\n== Score ==")
    for r in result["reasons"]:
        print(" ", r)
    print(f"  TOTAL {result['total']}/100 -> {result['verdict']} (gate {profile['gate']})")

    # Box 4 - Tailor
    if args.offline:
        draft = load("examples/sample_draft.txt")
    else:
        from .tailor import tailor
        draft, usage = tailor(jd, bank)
        print(f"[tailor] tokens in/out: {usage['input_tokens']}/{usage['output_tokens']}")
    print("\n== Draft bullets ==")
    print(draft)

    # Box 5 - Grounding check
    g = grounding.check(draft, bank)
    print("\n== Grounding check ==")
    if g["passed"]:
        print("  PASS - every number traces to the bank")
    else:
        print(f"  BLOCKED - numbers not in the bank: {', '.join(g['ungrounded'])}")
        print("  The draft does not reach you until these are removed or added to the bank.")

    print(f"\n[latency] {time.time() - t0:.1f}s")

    # Box 6 - Human gate
    if not args.no_gate:
        ask_and_log(fields.get("title") or "untitled", result)


if __name__ == "__main__":
    main()
