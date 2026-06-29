# Day 8 — Tokenization

## What I built
token_counter.py — uses tiktoken to show the actual token PIECES and IDs
that text splits into, across revealing examples.

## The core idea
Models don't read letters or words — they read TOKENS (chunks of text, each a number).
Whatever is inside a token is invisible to the model as separate parts.

## What the examples revealed
- "strawberry" → ['str','aw','berry']: the model can't count the r's because it
  never sees individual letters — only chunks. (We see the whole bun; the model
  sees the whole token.)
- "Hello" (9906) vs "hello" (15339): casing = completely different tokens/IDs
- "antidisestablishmentarianism" → 6 tokens: rare/long words shatter into many pieces
- "  spaces   matter": spaces are real tokens and attach to words; extra spaces cost tokens
- "123456789" → ['123','456','789']: numbers chunk in 3s → why LLMs are weak at arithmetic
- 🍓 → 3 tokens: a single emoji can cost more than a word

## Why this matters
Tokenization explains a dozen "why is the AI dumb at this" cases: letter-counting,
arithmetic, casing sensitivity, why non-English/emoji text costs more, why the
context window is measured in tokens not words.

## Remaining confusions
- (anything still fuzzy?)
