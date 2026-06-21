import os
import json
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "llm_calls.jsonl")

def load_config():
    """Load API key and model from environment."""
    load_dotenv()
    model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
    return {"client": Anthropic(), "model": model}

def call_model(client, model, prompt):
    """Send the prompt to the model and time the round trip."""
    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - start
    return {
        "timestamp": datetime.now().isoformat(),
        "model": response.model,
        "prompt": prompt,
        "response": response.content[0].text,
        "latency_seconds": round(latency, 2),
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

def log_call(data):
    """Append one call as a single JSON line."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(data) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, help="The prompt to send")
    args = parser.parse_args()

    config = load_config()
    result = call_model(config["client"], config["model"], args.prompt)
    log_call(result)

    print("--- ANSWER ---")
    print(result["response"])
    print("\n--- STATS ---")
    print(f"Model:   {result['model']}")
    print(f"Latency: {result['latency_seconds']}s")
    print(f"Tokens:  {result['input_tokens']} in / {result['output_tokens']} out")
    print(f"\nLogged to {LOG_PATH}")

if __name__ == "__main__":
    main()
