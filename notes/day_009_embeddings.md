# Day 9 — Embeddings

## What I built
embedding_similarity.ipynb — turns text into vectors via OpenAI's
text-embedding-3-small, then measures similarity with cosine similarity.

## The core idea
An embedding turns text into a list of numbers (a vector) — "hello" became 1536 numbers.
Those numbers are a LOCATION in "idea space." Similar meanings land close together.

## What the experiment proved
- "I love my dog" vs "My puppy is wonderful" → 0.615 (HIGH) despite ZERO shared words
- "I love my dog" vs "The stock market crashed" → 0.051 (LOW), correctly unrelated
- A thing vs itself → 1.000

## Keyword search vs embeddings
Keyword search matches surface words, so dog ≠ puppy = "unrelated."
Embeddings match meaning-as-location, so dog and puppy sit close → similar.

## Cosine similarity
Measures how closely two vectors point the same direction: 1 = identical, 0 = unrelated.

## Why this matters
This is the engine under semantic search, recommendations, and RAG (Day 43+):
find relevant things by MEANING, not word overlap.

## Debugging win
Relative path "01_llm_api_logger/.env" failed to load the key from a notebook in
a different folder. Fixed with an absolute path (Path.home()/...). Printed state at
each step to find where reality diverged from expectation.

## Remaining confusions
- (anything still fuzzy?)
