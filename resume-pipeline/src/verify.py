"""Build verification for one-page resume PDFs.

A build is unfinished until every check passes. See README for rationale.
"""
import re, subprocess, sys

def tag_balance(html_path):
    s = open(html_path).read()
    problems = []
    for tag in ("div", "ul", "li", "span", "p"):
        opens = len(re.findall(rf"<{tag}[\s>]", s))
        closes = s.count(f"</{tag}>")
        if opens != closes:
            problems.append(f"{tag}: {opens} open vs {closes} close")
    return problems

def non_ascii(html_path):
    return [i + 1 for i, ln in enumerate(open(html_path))
            if any(ord(c) > 127 for c in ln)]

def end_anchor(pdf_path, anchor):
    txt = subprocess.run(["pdftotext", pdf_path, "-"],
                         capture_output=True, text=True).stdout
    return anchor in txt

def page_count(pdf_path):
    out = subprocess.run(["pdfinfo", pdf_path],
                         capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))

if __name__ == "__main__":
    html, pdf, anchor = sys.argv[1], sys.argv[2], sys.argv[3]
    assert not tag_balance(html), tag_balance(html)
    assert not non_ascii(html), f"non-ascii lines: {non_ascii(html)}"
    assert page_count(pdf) == 1, "not one page"
    assert end_anchor(pdf, anchor), "END ANCHOR MISSING - silent truncation"
    print("all checks passed")
