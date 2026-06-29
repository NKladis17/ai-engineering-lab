# AI Engineering Lab

A hands-on lab building toward **LLM Systems & Evaluation Engineering**.
Each project explores how LLM systems work by building, breaking, measuring, and explaining them.

## Projects

### 01 — LLM API Logger
A small system built around the core skill of calling and measuring LLM APIs.

- **`llm_api_logger.py`** — calls an LLM, logs prompt/response/latency/tokens to JSONL, takes a `--prompt` CLI argument
- **`structured_outputs/`** — forces JSON output validated against a Pydantic schema; catches and logs malformed responses (defensive fence-stripping for markdown the model adds despite instructions)
- **`temperature_experiment.ipynb`** — same prompt run at temperature 0 vs 1, showing deterministic vs varied output
- **`cost_latency_logger.py`** — computes real USD cost per call from token counts; logs to CSV
- **`prompt_regression_test.py`** — scores two prompt versions against fixed test cases (keyword accuracy + brevity), producing a defensible pass/fail tally

## Key ideas demonstrated
- LLM output is probabilistic and must be validated, not trusted
- Cost and latency are driven by output token count
- "Better" requires measurement: fixed test cases, a single controlled variable, and automatic scoring

## Stack
Python, Anthropic API, Pydantic, Jupyter

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`
3. Run any script, e.g. `python 01_llm_api_logger/llm_api_logger.py --prompt "Hello"`
