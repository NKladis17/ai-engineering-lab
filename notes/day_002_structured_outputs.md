# Day 2 — Structured Outputs

## What I built
A structured_logger.py that forces the model to return JSON matching a Pydantic schema (summary, key_points, confidence, possible_errors), validates it, and logs both raw and parsed output with pass/fail status.

## Why raw text is not enough
Raw text is for humans. Code can't reliably extract fields from a paragraph. To build a system on model output, the output needs a predictable shape. When you need the model to feed data into a pipeline—feeding an agent, populating a database, triggering logic—you need guarantees about what fields exist and what types they hold.

## What JSON validation does
Two guards: `json.loads()` checks the text is parseable JSON; Pydantic checks it matches the required schema. Either can fail, and failure is caught, not ignored. If the model returns Markdown or wrapped the JSON in code fences, the first guard catches it. If the JSON is valid but missing a key field or has the wrong type, the second guard catches it.

## What Pydantic checks
Field names, types (summary=str, key_points=list of str), and constraints (confidence must be 0–1). Pydantic won't let you construct a StructuredAnswer with malformed data—it raises ValidationError before the object even exists.

## How validation failed
Call 1 failed because the model wrapped JSON in markdown backticks despite being told not to—a JSON decode error. The weak-prompt test ("Answer helpfully") failed because the model returned a Markdown article, not JSON at all. Same model, both "good" answers, both rejected for breaking the contract.

## What I learned about controlling model output
The model is probabilistic and violates instructions even when told clearly. So you don't trust it—you validate and defend (I added fence-stripping). "Nice answer" ≠ "valid machine-readable output."

## Remaining confusions
How much do system prompt specificity vs. max_tokens vs. model choice actually improve compliance? Would instruction-tuned models do better?
