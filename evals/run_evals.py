"""Eval harness. Compares the agent's GO/NO-GO with your own past decisions and real outcomes.

Add one row per past JD to evals/eval_set.csv:
  jd_file      path to the JD text you saved in evals/jds/
  my_decision  GO or NO-GO (what you decided at the time)
  outcome      interview, rejected, or no_response

Usage:
  python evals/run_evals.py              one pass over the set
  python evals/run_evals.py --repeat 3   run extraction 3 times per JD to measure variance
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from job_fit_agent import score  # noqa: E402
from job_fit_agent.extract import extract  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, default=1)
    args = ap.parse_args()
    profile = json.load(open("data/profile.json"))
    rows = list(csv.DictReader(open("evals/eval_set.csv")))

    agree = false_go = rejected_total = unstable = 0
    tokens = 0
    out = []
    for r in rows:
        jd = open(r["jd_file"], encoding="utf-8").read()
        verdicts, totals = [], []
        for _ in range(args.repeat):
            fields, usage = extract(jd)
            tokens += usage["input_tokens"] + usage["output_tokens"]
            s = score.score(fields, profile)
            verdicts.append(s["verdict"])
            totals.append(s["total"])
        verdict = max(set(verdicts), key=verdicts.count)
        if len(set(verdicts)) > 1:
            unstable += 1
        if verdict == r["my_decision"]:
            agree += 1
        if r["outcome"] == "rejected":
            rejected_total += 1
            if verdict == "GO":
                false_go += 1
        out.append([r["jd_file"], r["my_decision"], r["outcome"], verdict, min(totals), max(totals)])

    n = len(rows)
    print(f"JDs evaluated:            {n}")
    print(f"Agreement with you:       {agree}/{n}")
    print(f"False GO on rejections:   {false_go}/{rejected_total}")
    print(f"Unstable across repeats:  {unstable}/{n} (runs per JD: {args.repeat})")
    print(f"Total tokens:             {tokens}")
    with open("evals/results_latest.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["jd_file", "my_decision", "outcome", "agent_verdict", "min_score", "max_score"])
        w.writerows(out)
    print("Row detail saved to evals/results_latest.csv")


if __name__ == "__main__":
    main()
