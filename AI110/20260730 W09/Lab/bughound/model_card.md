# BugHound Mini Model Card (Reflection)

Completed after running BugHound in both Heuristic and Gemini modes.

---

## 1) What is this system?

**Name:** BugHound
**Purpose:** Analyze a Python snippet, propose a fix, and run reliability checks
before suggesting whether the fix should be auto-applied.

**Intended users:** Students learning agentic workflows and AI reliability concepts.

---

## 2) How does it work?

BugHound runs a small agentic loop, visible in the Agent Trace:

- **PLAN** — decide to do a quick scan + fix proposal.
- **ANALYZE** — detect issues. If a Gemini client is available it uses the LLM
  analyzer; if the client is missing, the API errors, or the model returns
  non-JSON, it falls back to a heuristic analyzer.
- **ACT** — propose a fix. Same heuristic-vs-Gemini split; empty or failed LLM
  output falls back to the heuristic fixer.
- **TEST** — `assess_risk` scores the change from 0–100 and assigns a level.
- **REFLECT** — if the risk level is "low" the fix is eligible for auto-apply;
  otherwise it defers to human review.

**Heuristics** are three fixed rules: flag `print(` (Low), bare `except:` (High),
and `TODO` (Medium). **Gemini** reads the code semantically and can find logic
problems the rules cannot. Both paths feed the same risk assessor.

---

## 3) Inputs and outputs

**Inputs I tried:**

- `print_spam.py` — a small function using `print` and returning a value.
- `mixed_issues.py` — a function with a TODO, a print, a bare `except`, and a
  silent divide-by-zero returning 0.
- `cleanish.py` — clean code that already uses logging (no issues).
- A comments-only input (`# this is just a comment`) as a "weird" case.

**Outputs:**

- **Issues:** categorized as type + severity (Low/Medium/High) + message.
- **Fixes:** either heuristic replacements (print → logging, bare except →
  `except Exception`) or a full Gemini rewrite.
- **Risk report:** a score, a level, a list of reasons, and an auto-fix decision.
  Example: `mixed_issues.py` in Gemini mode scored 25 (HIGH), auto-fix = NO.

---

## 4) Reliability and safety rules

**Rule A — "Return statements may have been removed" (−30).**
- Checks whether `return` existed in the original but is gone from the fix.
- Matters because silently dropping a return changes what the function produces,
  a serious correctness bug.
- False positive: a refactor that legitimately replaces `return x` with a `raise`
  would be flagged even though removing the return was intentional.
- False negative: it only checks the substring `return`, so a fix that keeps one
  return but deletes a different, important one still passes.

**Rule B — Over-editing signal (−25) [added in Part 3].**
- Flags a fix when many lines changed (>6 changed lines AND >1.5× the original
  size), indicating the model rewrote far more than necessary.
- Matters because large rewrites are hard to review and more likely to alter
  behavior, exactly the "minimal diff" concern from the fixer prompt.
- False positive: a small file where a legitimate fix naturally touches most
  lines could trip it (this is why I added the absolute >6 threshold).
- False negative: a subtle one-line change that silently alters behavior (like
  `return 0` → `raise`) is small, so this rule won't catch it.

---

## 5) Observed failure modes

**Failure 1 — Fix that felt risky (over-editing / behavior change).**
In Gemini mode on `mixed_issues.py`, the model changed `except: return 0` into
`except ZeroDivisionError: raise ValueError(...)`. The fix is arguably good
engineering, but it silently changes the function's contract: calling
`compute(5, 0)` used to return 0 and now raises. The fixer prompt says "preserve
behavior," but the model didn't. The risk assessor correctly scored this HIGH
and refused to auto-apply.

**Failure 2 — False confidence on non-analyzable input.**
A comments-only input (`# this is just a comment`) produced "No issues," a score
of 100, and Auto-fix = YES. Nothing was actually analyzed, yet the system
reported maximum confidence and approved auto-apply — a false-confidence failure.
I added a guardrail so empty/comments-only input now returns HIGH risk and
defers to a human.

---

## 6) Heuristic vs Gemini comparison

- **Gemini caught what heuristics couldn't:** on `mixed_issues.py` it flagged a
  silent divide-by-zero returning 0 (a Correctness issue) and explained *why* a
  bare except is dangerous (it swallows KeyboardInterrupt/SystemExit). Heuristics
  can only string-match `print`, `except:`, and `TODO`.
- **Heuristics were consistent:** the three rules fire reliably and never cost
  API quota, which makes them a dependable fallback.
- **Fixes differed:** heuristics do mechanical replacements; Gemini restructures
  code and sometimes over-edits.
- **Did the risk scorer match intuition?** Mostly yes — it flagged the risky
  divide-by-zero rewrite. But my first over-editing threshold was too strict and
  flagged a harmless print→logging swap, so "agreeing with intuition" required
  tuning the thresholds.

---

## 7) Human-in-the-loop decision

BugHound should refuse to auto-fix when a change alters control flow or a
function's return/error contract — for example, turning a value-returning path
into a raised exception.

- **Trigger:** detect when the original code returns a value on a path that the
  fix converts into a `raise`, or when return values disappear.
- **Where:** in `risk_assessor`, since it already owns the auto-fix decision and
  runs outside the agent's own loop (external verification).
- **Message:** "This fix changes how the function returns or handles errors.
  Auto-apply is blocked; please review before merging."

---

## 8) Improvement idea

Add a lightweight "behavior-change" guardrail: compare the count of `return`
statements and the presence of `raise` between original and fixed code, and if
the fix trades a `return` for a `raise` (or removes returns), lower the score and
require review. It's a few lines in `risk_assessor` plus one test, but it
directly targets the most dangerous failure I saw — a fix that looks clean but
quietly changes what the function does.
