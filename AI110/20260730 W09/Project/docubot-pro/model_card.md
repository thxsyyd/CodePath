# Model Card: DocuBot Pro

A responsible-AI reflection on DocuBot Pro, a confidence-gated RAG documentation
assistant built for CodePath AI110 as an Applied AI System.

---

## 1. System overview

**What it does.** DocuBot Pro answers developer questions about a project's own
Markdown documentation. It retrieves relevant paragraphs, scores how trustworthy
that retrieval is, and then either answers, answers with a caveat, or refuses and
defers to a human.

**Base project.** It extends DocuBot, an earlier RAG assistant that could
retrieve snippets and ask Gemini to answer from them, but had no awareness of its
own retrieval quality. DocuBot Pro adds a confidence layer, a refusal guardrail,
decision-trace logging, and an offline evaluation harness.

**Intended users.** Developers looking up facts in a documentation set, and
learners studying how reliability is engineered around an LLM.

## 2. How it works

For each question, the pipeline runs: retrieve paragraph chunks by keyword →
assess confidence from retrieval signals (top score, number of hits, and the gap
between the top two chunks) → decide (HIGH answers, MEDIUM answers with a caveat,
LOW refuses) → generate with Gemini only when the guardrail allows it. Because
the confidence check runs before generation, low-confidence questions are refused
without an API call.

The key design choice is that confidence is **rule-based and explainable**. Every
decision can be traced to concrete retrieval signals rather than a hidden second
model call, which makes the behavior auditable — the whole point of the trace log.

## 3. Data

The corpus is four Markdown files (authentication, API reference, database, and
setup) describing a small fictional web application. There is deliberately no
content about some topics (for example, payment processing), which lets us test
whether the system refuses questions it cannot support. The docs are small and
English-only, so the system's knowledge is narrow by design.

## 4. Reliability features and evaluation

- **Refusal guardrail.** LOW-confidence questions are refused and escalated to a
  human instead of answered from weak evidence.
- **Confidence caveats.** MEDIUM-confidence answers carry an explicit
  "please verify" warning.
- **Trace logging.** Every query's RETRIEVE → ASSESS → DECIDE → RESPOND steps are
  recorded to `logs/trace.log` for after-the-fact review.
- **Evaluation harness.** `evaluation.py` checks the answer/refuse decision
  against eight labeled cases — four answerable and four should-refuse (off-topic,
  empty, gibberish, and a topic absent from the docs). Current result: **8/8 pass**.

Evaluation is offline and deterministic (it never calls Gemini), so it is fast,
free, and reproducible for anyone reviewing the project.

## 5. Limitations and biases

- **Keyword retrieval has no sense of meaning.** A question phrased differently
  from the docs ("list users" vs "returns all users") can score low and be
  refused even though the answer exists. During testing, several genuinely
  answerable questions (the `/api/projects` return value, the users-table fields)
  scored just as low as the unanswerable payment question and were refused. This
  is a **false-negative** failure: the system is conservative and would rather
  refuse than guess.
- **The confidence thresholds are heuristic.** They were tuned against this small
  corpus; a different or larger document set would likely need re-tuning, and no
  single threshold cleanly separates "answerable" from "unanswerable."
- **Small, narrow corpus.** Four English documents about one fictional app. The
  system should not be treated as knowledgeable outside that scope.

## 6. Responsible use

- Treat answers as pointers, not final truth — DocuBot Pro cites its source files
  precisely so a reader can confirm the claim in the original doc.
- Read a refusal as "verify manually," not as "the answer does not exist." Because
  retrieval is conservative, a refusal can be a false negative.
- Do not remove the guardrail to force answers on low-confidence questions; that
  reintroduces exactly the hallucination risk the upgrade was built to prevent.

## 7. Reflection

**How AI collaboration helped.** I used an AI assistant to reason through the
confidence design — which retrieval signals to use, and how to turn them into a
HIGH/MEDIUM/LOW policy — and to scaffold the trace logger and evaluation harness.
That sped up the parts that were mechanical once the design was clear.

**Where I had to double-check the AI.** I did not trust the behavior until I ran
it. Reading the actual traces and the evaluation report is what revealed the most
important finding: the guardrail refuses some genuinely answerable questions
because keyword retrieval scores them as low as truly unanswerable ones. That
false-negative pattern is not obvious from the code — only from the output. It is
a direct echo of the "trust the log, not the vibe" idea: the trace told me what
the system actually did, which was more conservative than it looked on paper.

**One good improvement suggestion I would keep:** replacing keyword scoring with
embedding-based semantic retrieval, so questions are matched by meaning rather
than exact words. This directly targets the false-negative problem above and is
the single change most likely to raise real answer coverage without weakening the
guardrail.

**One suggestion I would push back on:** making the guardrail more permissive
(lowering the confidence threshold) to answer more questions. It would improve
the surface metric — fewer refusals — but at the cost of answering from weak
evidence, which is exactly the failure this system exists to avoid. Fewer
refusals is not the goal; trustworthy answers are.
