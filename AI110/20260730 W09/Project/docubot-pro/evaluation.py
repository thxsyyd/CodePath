"""
Evaluation harness for DocuBot Pro.

Runs the confidence layer against a set of labeled test cases and reports how
often the system's decision (answer vs refuse) matches what we expect. This is
an OFFLINE reliability check: it never calls Gemini, so it is fast, free, and
fully reproducible. It exercises retrieval + confidence, which is where the
answer/refuse decision is actually made.

Each case declares:
    query           - the input question
    expect_answered - True if the system SHOULD answer, False if it should refuse
    note            - why we expect that (for the report)

Run:
    python evaluation.py
"""

from docubot import DocuBot
from confidence import assess_confidence


# Labeled test cases. "expect_answered" is the ground truth for the guardrail.
TEST_CASES = [
    {
        "query": "Where is the auth token generated?",
        "expect_answered": True,
        "note": "AUTH.md clearly documents generate_access_token",
    },
    {
        "query": "What environment variables are required for authentication?",
        "expect_answered": True,
        "note": "AUTH.md / SETUP.md list AUTH_SECRET_KEY",
    },
    {
        "query": "How do I connect to the database?",
        "expect_answered": True,
        "note": "DATABASE.md documents DATABASE_URL",
    },
    {
        "query": "How does a client refresh an access token?",
        "expect_answered": True,
        "note": "AUTH.md / API_REFERENCE.md document /api/refresh",
    },
    {
        "query": "Is there any mention of payment processing?",
        "expect_answered": False,
        "note": "No payment content exists in the docs -> should refuse",
    },
    {
        "query": "What is the weather in Seattle today?",
        "expect_answered": False,
        "note": "Unrelated to the docs -> should refuse",
    },
    {
        "query": "",
        "expect_answered": False,
        "note": "Empty input -> should refuse",
    },
    {
        "query": "asdfghjkl qwerty zxcvbnm",
        "expect_answered": False,
        "note": "Gibberish -> should refuse",
    },
]


def evaluate():
    bot = DocuBot()  # retrieval + confidence only; no LLM needed

    passed = 0
    rows = []

    for case in TEST_CASES:
        query = case["query"]
        expected = case["expect_answered"]

        scored = bot.retrieve_with_scores(query, top_k=3, min_score=1)
        report = assess_confidence(scored)
        actual = report.should_answer

        ok = (actual == expected)
        if ok:
            passed += 1

        rows.append({
            "query": query if query else "(empty)",
            "expected": "ANSWER" if expected else "REFUSE",
            "actual": "ANSWER" if actual else "REFUSE",
            "confidence": report.level,
            "result": "PASS" if ok else "FAIL",
        })

    return passed, rows


def print_report(passed, rows):
    total = len(rows)
    print("DocuBot Pro — Evaluation Report")
    print("=" * 72)
    print(f"{'Query':<48}{'Expect':<8}{'Got':<8}{'Result'}")
    print("-" * 72)
    for r in rows:
        q = r["query"]
        if len(q) > 46:
            q = q[:45] + "…"
        print(f"{q:<48}{r['expected']:<8}{r['actual']:<8}{r['result']}")
    print("-" * 72)
    print(f"Passed {passed}/{total} "
          f"({round(100 * passed / total)}%). "
          f"Guardrail decisions checked offline (no API calls).")


if __name__ == "__main__":
    passed, rows = evaluate()
    print_report(passed, rows)
