"""Box 3 - Score (plain code, no model). The 5-dimension rubric.
Why code, not the LLM: a score must give the same answer twice and be
explainable line by line. Function 30, Domain 20, Seniority 20, Keywords 20, AI 10."""


def score(fields, profile):
    reasons = []

    # Function (30)
    fn = (fields.get("function") or "other").lower()
    function_pts = 30 if fn in profile["target_functions"] else 0
    reasons.append(f"Function '{fn}': {function_pts}/30")

    # Domain (20)
    dom = (fields.get("domain") or "").lower()
    domain_pts = 20 if any(d in dom for d in profile["target_domains"]) else 8
    reasons.append(f"Domain '{dom}': {domain_pts}/20")

    # Seniority (20): penalise roles far below or far above 12 years
    yrs = fields.get("min_years")
    mine = profile["years_experience"]
    if yrs is None:
        seniority_pts = 12
        note = "not stated"
    elif mine - 4 <= yrs <= mine + 3:
        seniority_pts = 20
        note = f"{yrs}+ yrs asked, in range"
    elif yrs < mine - 4:
        seniority_pts = 8
        note = f"{yrs}+ yrs asked, likely under-levelled"
    else:
        seniority_pts = 5
        note = f"{yrs}+ yrs asked, stretch"
    reasons.append(f"Seniority ({note}): {seniority_pts}/20")

    # Keywords (20): share of JD skills that match my keyword list
    skills = [s.lower() for s in fields.get("required_skills") or []]
    if skills:
        hits = [s for s in skills if any(k in s or s in k for k in profile["keywords"])]
        keyword_pts = round(20 * len(hits) / len(skills))
    else:
        hits, keyword_pts = [], 0
    reasons.append(f"Keywords {len(hits)}/{len(skills)} matched: {keyword_pts}/20")

    # AI signal (10)
    ai = fields.get("ai_signal") or "none"
    ai_pts = {"core": 10, "some": 5}.get(ai, 0)
    reasons.append(f"AI signal '{ai}': {ai_pts}/10")

    total = function_pts + domain_pts + seniority_pts + keyword_pts + ai_pts
    verdict = "GO" if total >= profile["gate"] else "NO-GO"
    return {"total": total, "verdict": verdict, "reasons": reasons}
