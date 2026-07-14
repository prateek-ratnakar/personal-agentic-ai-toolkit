# personal-agentic-ai-toolkit

Personal, non-employer agentic AI projects built end-to-end with Claude and Gemini APIs - designed, prompted, and shipped by one person with no engineering team. Each module is a working system I run for myself or a small user group, published here as sanitized architecture, prompt patterns, and orchestration code.

**Author:** Prateek Ratnakar | [LinkedIn](https://www.linkedin.com/in/prateekratnakar) | prateek.ratnakar@gmail.com

## Modules

| Module | What it does | Stack |
|---|---|---|
| [`shopping-insights-agent`](./shopping-insights-agent) | Personal agent that analyzes purchase history and price signals to surface buying insights and timing recommendations | Claude API, tool use, structured JSON outputs |
| [`job-search-agent`](./job-search-agent) | Multi-user agent for friends: matches JDs against a candidate achievement bank, scores fit on a 5-dimension rubric, tailors a one-page resume, and prepares a one-click apply package | Claude API, RAG over achievement bank, HTML-to-PDF pipeline |
| [`resume-pipeline`](./resume-pipeline) | Deterministic resume build-and-verify pipeline: HTML templates, binary-search line-height fitting to 94-97% page fill, ATS checks (tag balance, non-ASCII scan, truncation anchor grep) | Python, wkhtmltopdf, pdftotext/pdfinfo |

## Design principles

1. **Agent as operator, not oracle.** Every agent produces an auditable artifact (a scored table, a rendered PDF, a decision log) rather than free text.
2. **Grounding before generation.** Job matching and resume tailoring run RAG over a locked, human-verified achievement bank - the agent may select and rephrase, never invent a figure.
3. **Verification is part of the product.** The resume pipeline treats a build as unfinished until programmatic checks pass: page count, fill percentage, tag balance, ASCII cleanliness, end-anchor presence.
4. **Cheap to run, boring to operate.** Plain Python orchestration, no framework lock-in; every module runs from a single entry point.

## Status

Active personal use. Sanitized: no employer data, no proprietary prompts, no third-party personal data.
