import os
import csv
import time
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

# Haiku 4.5 pricing (USD per token)
INPUT_PRICE = 1.00 / 1_000_000   # $1 per million input tokens
OUTPUT_PRICE = 5.00 / 1_000_000  # $5 per million output tokens

CSV_PATH = Path(__file__).parent / "logs" / "cost_latency.csv"
MODEL = "claude-haiku-4-5-20251001"


def call_and_measure(client, prompt):
    start = time.time()
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - start

    in_tok = response.usage.input_tokens
    out_tok = response.usage.output_tokens
    cost = (in_tok * INPUT_PRICE) + (out_tok * OUTPUT_PRICE)

    return {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "latency_seconds": round(latency, 3),
        "cost_usd": round(cost, 8),
    }


def log_csv(record):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        if not file_exists:
            writer.writeheader()   # write column names only once
        writer.writerow(record)


def main():
    load_dotenv()
    client = Anthropic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()

    record = call_and_measure(client, args.prompt)
    log_csv(record)

    print(f"Latency: {record['latency_seconds']}s")
    print(f"Tokens:  {record['input_tokens']} in / {record['output_tokens']} out")
    print(f"Cost:    ${record['cost_usd']:.6f}")
    print(f"Logged to {CSV_PATH}")


if __name__ == "__main__":
    main()
