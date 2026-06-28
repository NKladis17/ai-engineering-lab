import subprocess

prompts = [
    "Explain what an API is.",
    "What is a token in an LLM?",
    "Define latency in one sentence.",
    "What is JSON?",
    "Explain embeddings simply.",
    "What does a vector database do?",
    "Summarize what RAG is.",
    "What is fine-tuning?",
    "Explain temperature in LLMs.",
    "What is an AI agent?",
    "Define overfitting.",
    "What is gradient descent?",
    "Explain attention in transformers.",
    "What is a context window?",
    "Define a system prompt.",
    "What is prompt injection?",
    "Explain what an eval is.",
    "What is a hallucination in AI?",
    "Define inference in ML.",
    "What is quantization?",
]

for i, p in enumerate(prompts, 1):
    print(f"\n--- Call {i}/{len(prompts)} ---")
    subprocess.run([
        "python3",
        "01_llm_api_logger/cost_latency_logger.py",
        "--prompt", p,
    ])
