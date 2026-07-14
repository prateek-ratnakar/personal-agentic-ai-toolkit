# job-search-agent

Multi-user agentic system built for friends running senior-level job searches. Given a JD, it scores fit, tailors a one-page resume from a locked achievement bank, and prepares an apply-ready package.

## Pipeline

```
JD (text/URL)
   |
1. PARSE      -> role, seniority band, must-haves, keywords
2. SCORE      -> 5-dimension rubric: Function 30 / Domain 20 / Seniority 20 / Keywords 20 / AI-signal 10
                 gate at 85% for cold applications; go / borderline / no-go verdict with named gaps and bridges
3. TAILOR     -> RAG over the user's achievement bank; bullet selection + reordering only,
                 figures locked - the agent may rephrase, never invent
4. RENDER     -> resume-pipeline module: HTML template -> one-page PDF at 94-97% fill, ATS-verified
5. PACKAGE    -> resume + cover letter + gap disclosure notes, ready for one-click apply
```

## Key design decisions
- **Achievement bank as source of truth.** Each user maintains a human-verified markdown bank of figures and bullets. Hallucinated metrics are a firing offense for the agent: the tailor step is retrieval + selection, with a post-generation diff that flags any number not present in the bank.
- **Scored, not vibed.** Every verdict ships with the dimension-level scores, the gaps as bullets, and the bridge actions - so the human can overrule with full information.
- **Honesty gates.** Missing certifications or tooling experience are surfaced for explicit disclosure, never papered over.

## Multi-user
Per-user config: achievement bank path, comp floor, target tracks, resume base templates. The rubric weights are shared; the gates are personal.
