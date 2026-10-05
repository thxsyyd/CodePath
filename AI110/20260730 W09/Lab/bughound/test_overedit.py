"""Offline sanity check for the over-editing risk signal.

Feeds fake original/fixed code pairs directly into assess_risk to confirm
that large rewrites are penalized. No Gemini calls.
"""

from reliability.risk_assessor import assess_risk


def show(label, original, fixed, issues):
    result = assess_risk(original_code=original, fixed_code=fixed, issues=issues)
    print(f"=== {label} ===")
    print(f"  score={result['score']}  level={result['level']}  autofix={result['should_autofix']}")
    for r in result["reasons"]:
        print(f"    - {r}")
    print()


def main():
    # Case 1: small, targeted fix (should NOT trigger over-editing)
    original_small = 'def greet(name):\n    print("hi", name)\n    return True'
    fixed_small = 'import logging\n\ndef greet(name):\n    logging.info("hi", name)\n    return True'
    show("Small fix (logging swap)", original_small, fixed_small,
         [{"type": "Code Quality", "severity": "Low", "msg": "print"}])

    # Case 2: massive rewrite (SHOULD trigger over-editing)
    original_big = 'def compute(x, y):\n    print("computing")\n    try:\n        return x / y\n    except:\n        return 0'
    fixed_big = 'import logging\n\ndef compute(x, y):\n    """Compute x divided by y."""\n    logging.info("starting")\n    if y == 0:\n        raise ValueError("no")\n    result = x / y\n    logging.info("done")\n    return result'
    show("Big rewrite (over-edit)", original_big, fixed_big,
         [{"type": "Reliability", "severity": "High", "msg": "bare except"}])


if __name__ == "__main__":
    main()
