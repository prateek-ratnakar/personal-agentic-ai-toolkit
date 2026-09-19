"""Box 5 - Grounding check (plain code). Every number in the draft must exist in the bank.
This is the launch gate: an ungrounded number blocks the output instead of reaching a human."""
import re

NUMBER = re.compile(r"\$?\d+(?:[.,]\d+)*(?:%|M|K|x)?")


def numbers_in(text):
    found = set()
    for n in NUMBER.findall(text):
        n = n.replace(",", "")
        if n.strip("$%MKx"):
            found.add(n)
    return found


def check(draft, bank_text):
    bank_numbers = numbers_in(bank_text)
    draft_numbers = numbers_in(draft)
    ungrounded = sorted(n for n in draft_numbers if n not in bank_numbers)
    return {"passed": not ungrounded, "ungrounded": ungrounded}
