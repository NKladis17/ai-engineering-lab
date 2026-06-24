import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

LOG_PATH = Path(__file__).parent / "structured_logs.jsonl"

# --- The contract: what a valid answer MUST look like ---
class StructuredAnswer(BaseModel):
    summary: str = Field(description="A concise 1-2 sentence answer.")
    key_points: List[str] = Field(description="3-5 important bullet points.")
    confidence: float = Field(ge=0, le=1, description="Confidence from 0 to 1.")
    possible_errors: List[str] = Field(description="Ways the answer might be wrong.")

SYSTEM_PROMPT = """
You are a structured-output assistant.

Return ONLY valid JSON.
Do not include markdown.
Do not include backticks.
Do not include explanations outside the JSON.

The JSON must match this exact schema:
{
  "summary": "string",
  "key_points": ["string", "string", "string"],
  "confidence": 0.0,
  "possible_errors": ["string"]
}
"""

def call_model(prompt, model, max_tokens=800):
    client = Anthropic()
    start = time.time()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - start
    return {
        "raw_text": message.content[0].text,
        "latency_seconds": round(latency, 3),
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "model": message.model,
    }

def parse_and_validate(raw_text):
    cleaned = raw_text.strip()
    # Defend against markdown code fences the model adds despite instructions
    if cleaned.startswith("```"):
        # drop the first line (```json or ```) and the closing ```
        lines = cleaned.split("\n")
        lines = lines[1:]                      # remove opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]                 # remove closing fence
        cleaned = "\n".join(lines).strip()

    data = json.loads(cleaned)          # can fail = not valid JSON
    return StructuredAnswer(**data)     # can fail = wrong shape

def log_result(record):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"))
    args = parser.parse_args()

    result = call_model(args.prompt, args.model)

    parsed = None
    validation_passed = False
    error_message = None

    try:
        parsed = parse_and_validate(result["raw_text"])
        validation_passed = True
    except json.JSONDecodeError as e:
        error_message = f"JSON decode error: {e}"
    except ValidationError as e:
        error_message = f"Pydantic validation error: {e}"

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": args.prompt,
        "model": result["model"],
        "raw_text": result["raw_text"],
        "parsed": parsed.model_dump() if parsed else None,
        "validation_passed": validation_passed,
        "error": error_message,
        "latency_seconds": result["latency_seconds"],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
    }
    log_result(record)

    if validation_passed:
        print("\nVALID STRUCTURED OUTPUT ✅")
        print(json.dumps(parsed.model_dump(), indent=2))
    else:
        print("\nVALIDATION FAILED ❌")
        print(error_message)
        print("\nRAW TEXT:")
        print(result["raw_text"])

if __name__ == "__main__":
    main()
