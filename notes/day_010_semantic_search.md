# Day 10 — Semantic Search

## What I built
semantic_search.py — a working search engine that finds documents by MEANING.
Two phases: INDEX (embed all docs once at startup) + SEARCH (embed the query,
compare to all doc vectors, return the closest by cosine similarity).

## Why the two-phase split
Embedding documents is the expensive part → do it once upfront (indexing).
Searching is just cheap comparisons against pre-computed vectors → do per query.
This is how real vector databases work.

## What it proved
- "cheap flights" → "Affordable airfare..." at 0.547 (ZERO shared words)
- "staying healthy" → "Regular exercise improves cardiovascular health" (0.420)
- "fast animals" → cheetah line (0.434)
- Scores are a CONFIDENCE signal, not just a ranking — useful for thresholds in RAG

## How embeddings work (the deeper why)
- The embedding model is a neural net trained by a fill-in-the-blank game on huge text.
- To win that game it had to place words used in similar contexts at similar coordinates.
- So meaning-as-location EMERGED. "You know a word by the company it keeps."
- Cosine similarity is just a ruler measuring distance; the meaning lives in the coordinates.

## Why this matters
This IS the retrieval engine under RAG (Day 43): embed the question, find the
closest stored documents by meaning. I built the heart of it by hand.

## Remaining confusions
- (anything still fuzzy?)
