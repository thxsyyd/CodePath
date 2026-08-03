"""Offline sanity check for the severity validation guardrail.

Does NOT call Gemini — it feeds fake 'LLM output' directly into the
agent's normalization logic to confirm malformed severities are handled.
"""

from bughound_agent import BugHoundAgent


def main():
    agent = BugHoundAgent(client=None)  # no client needed; offline

    # 1. Test _validate_severity directly with good and bad values
    print("=== _validate_severity ===")
    cases = ["Low", "medium", "HIGH", " high ", "Critical", "urgent", "Hgih", "", "42"]
    for raw in cases:
        result = agent._validate_severity(raw)
        print(f"  {raw!r:12s} -> {result!r}")

    # 2. Test _normalize_issues with a simulated malformed LLM response
    print("\n=== _normalize_issues (simulated bad LLM output) ===")
    fake_llm_issues = [
        {"type": "Reliability", "severity": "High", "msg": "bare except"},
        {"type": "Security", "severity": "Critical", "msg": "sql injection"},  # illegal!
        {"type": "Style", "severity": "low", "msg": "long line"},
        {"type": "Mystery", "msg": "no severity field at all"},               # missing!
    ]
    normalized = agent._normalize_issues(fake_llm_issues)
    for issue in normalized:
        print(f"  type={issue['type']:12s} severity={issue['severity']:8s} msg={issue['msg']}")

    print("\nExpected: 'Critical' -> 'High', missing severity -> 'High'")


if __name__ == "__main__":
    main()
