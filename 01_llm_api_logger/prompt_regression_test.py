import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
MODEL = "claude-haiku-4-5-20251001"

# Wall #1 + #2: fixed test cases, each with its own correctness rule (required keyword)
TEST_CASES = [
    {"question": "What unit does an LLM process text in?", "must_contain": "token"},
    {"question": "What technique retrieves documents to answer questions?", "must_contain": "rag"},
    {"question": "What setting controls randomness in model output?", "must_contain": "temperature"},
    {"question": "What do you call it when a model invents false facts?", "must_contain": "hallucinat"},
    {"question": "What is the name for adapting a model on custom data?", "must_contain": "fine-tun"},
]

# Wall #3: the two prompts are the ONLY thing that changes
PROMPT_A = "You are a helpful assistant."
PROMPT_B = "You are a precise AI expert. Answer in one short sentence using exact technical terms."


def run_case(system_prompt, question):
    response = client.messages.create(
        model=MODEL,
        max_tokens=100,
        temperature=0,                      # Wall #3: temp 0 removes randomness
        system=system_prompt,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


# Wall #4: one automatic, identical scoring rule for both prompts
def score(answer, must_contain):
    has_keyword = must_contain.lower() in answer.lower()
    is_concise = len(answer.split()) <= 25      # B's instruction: "one short sentence"
    return has_keyword and is_concise


# Wall #5: loop over every case for one prompt, tally the passes
def evaluate(name, system_prompt):
    passed = 0
    print(f"\n===== {name} =====")
    for case in TEST_CASES:
        answer = run_case(system_prompt, case["question"])
        ok = score(answer, case["must_contain"])
        passed += ok
        mark = "✅" if ok else "❌"
        word_count = len(answer.split())
        print(f"{mark} (need '{case['must_contain']}', {word_count} words) → {answer.strip()[:70]}")
    print(f"SCORE: {passed}/{len(TEST_CASES)}")
    return passed


def main():
    a = evaluate("PROMPT A (vague)", PROMPT_A)
    b = evaluate("PROMPT B (specific)", PROMPT_B)
    print("\n========== RESULT ==========")
    print(f"Prompt A: {a}/{len(TEST_CASES)}")
    print(f"Prompt B: {b}/{len(TEST_CASES)}")


if __name__ == "__main__":
    main()
