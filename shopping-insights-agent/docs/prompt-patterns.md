# Prompt patterns

## Schema-constrained analysis
The analysis prompt supplies (1) the canonical ledger slice, (2) a strict JSON schema, (3) three worked examples. The system prompt forbids inferring purchases not present in the ledger - the same "grounding before generation" rule used across the toolkit.

## Cadence detection
Rather than asking the model to "find patterns," the orchestrator computes inter-purchase intervals deterministically and asks the model only to label and explain them - LLM for judgment, code for arithmetic.
