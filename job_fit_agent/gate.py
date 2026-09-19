"""Box 6 - Human gate. The agent recommends; a person decides. It never applies anywhere."""
import csv
import datetime
import os


def ask_and_log(title, result, log_path="data/decisions.csv"):
    print(f"\nAgent says {result['verdict']} ({result['total']}/100) for: {title}")
    answer = input("Your decision - apply? (y/n): ").strip().lower()
    decision = "GO" if answer == "y" else "NO-GO"
    new_file = not os.path.exists(log_path)
    with open(log_path, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["date", "title", "agent_score", "agent_verdict", "my_decision"])
        w.writerow([datetime.date.today().isoformat(), title, result["total"], result["verdict"], decision])
    print(f"Logged: you said {decision}. Disagreements are the eval signal.")
    return decision
