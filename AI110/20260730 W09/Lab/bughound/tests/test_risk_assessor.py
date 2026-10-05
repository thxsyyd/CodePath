from reliability.risk_assessor import assess_risk


def test_no_fix_is_high_risk():
    risk = assess_risk(
        original_code="print('hi')\n",
        fixed_code="",
        issues=[{"type": "Code Quality", "severity": "Low", "msg": "print"}],
    )
    assert risk["level"] == "high"
    assert risk["should_autofix"] is False
    assert risk["score"] == 0


def test_low_risk_when_minimal_change_and_low_severity():
    original = "import logging\n\ndef add(a, b):\n    return a + b\n"
    fixed = "import logging\n\ndef add(a, b):\n    return a + b\n"
    risk = assess_risk(
        original_code=original,
        fixed_code=fixed,
        issues=[{"type": "Code Quality", "severity": "Low", "msg": "minor"}],
    )
    assert risk["level"] in ("low", "medium")  # depends on scoring rules
    assert 0 <= risk["score"] <= 100


def test_high_severity_issue_drives_score_down():
    original = "def f():\n    try:\n        return 1\n    except:\n        return 0\n"
    fixed = "def f():\n    try:\n        return 1\n    except Exception as e:\n        return 0\n"
    risk = assess_risk(
        original_code=original,
        fixed_code=fixed,
        issues=[{"type": "Reliability", "severity": "High", "msg": "bare except"}],
    )
    assert risk["score"] <= 60
    assert risk["level"] in ("medium", "high")


def test_missing_return_is_penalized():
    original = "def f(x):\n    return x + 1\n"
    fixed = "def f(x):\n    x + 1\n"
    risk = assess_risk(
        original_code=original,
        fixed_code=fixed,
        issues=[],
    )
    assert risk["score"] < 100
    assert any("Return" in r or "return" in r for r in risk["reasons"])


def test_comments_only_input_is_not_autofixed():
    # A file with no real code (comments + blank lines only) should never be
    # auto-fixed; there is nothing meaningful to assess, so defer to a human.
    original = "# this is just a comment\n\n# another note\n"
    fixed = original
    risk = assess_risk(original_code=original, fixed_code=fixed, issues=[])
    assert risk["should_autofix"] is False
    assert risk["level"] == "high"
    assert any("analyzable" in r.lower() or "no analyzable code" in r.lower()
               for r in risk["reasons"])


def test_real_code_still_assessed_normally():
    # Sanity check: the empty-code guardrail must NOT trip on real code.
    original = "import logging\n\ndef add(a, b):\n    return a + b\n"
    fixed = original
    risk = assess_risk(original_code=original, fixed_code=fixed, issues=[])
    # Real code with no issues should score well and remain eligible to autofix.
    assert risk["score"] > 0
    assert "No analyzable code found" not in " ".join(risk["reasons"])
