import tiktoken

# A tokenizer turns text into the numbered chunks a model actually reads.
# cl100k_base is the tokenizer used by GPT-4-class models (concept is the same across LLMs).
enc = tiktoken.get_encoding("cl100k_base")


def show_tokens(text):
    token_ids = enc.encode(text)               # text -> list of token ID numbers
    chunks = [enc.decode([tid]) for tid in token_ids]  # each ID -> its text piece
    print(f"\nTEXT: {text!r}")
    print(f"TOKEN COUNT: {len(token_ids)}")
    print(f"PIECES: {chunks}")
    print(f"IDS:    {token_ids}")


# A set of revealing examples
examples = [
    "Hello world",
    "tokenization",
    "antidisestablishmentarianism",
    "strawberry",
    "  spaces   matter",
    "Hello",
    "hello",
    "ChatGPT is great!!!",
    "123456789",
    "🍓 emoji",
]

for ex in examples:
    show_tokens(ex)
