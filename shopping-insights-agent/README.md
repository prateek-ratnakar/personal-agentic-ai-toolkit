# shopping-insights-agent

Personal Claude-powered agent that turns raw purchase history into buying insights: spend patterns by category, price-drop timing, repeat-purchase cadence, and "should I buy now or wait" recommendations.

## Architecture

```
purchase exports (CSV/email parse)
        |
   normalizer  ->  canonical purchase ledger (JSON)
        |
   Claude analysis pass (tool use: category tagging, cadence detection)
        |
   insight generator  ->  monthly insight brief (markdown)
```

- **Normalizer** deduplicates and canonicalizes merchant names before any LLM call - grounding first.
- **Analysis pass** uses structured JSON output with a fixed schema so results are diff-able month over month.
- **Insight brief** is a rendered artifact, not chat output: every claim links back to ledger rows.

## Why it exists
Built to answer one question honestly - "where does the money actually go, and when is the right time to buy" - without handing my data to a third-party app.

See [`docs/prompt-patterns.md`](./docs/prompt-patterns.md) for the schema-constrained prompting approach.
