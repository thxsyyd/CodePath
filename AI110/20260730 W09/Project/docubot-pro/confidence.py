"""
Confidence layer for DocuBot Pro.

After retrieval, but before answering, this module scores how trustworthy the
retrieved evidence is and decides what the system should do:

    HIGH   -> answer normally
    MEDIUM -> answer, but attach a "please verify" caveat
    LOW    -> refuse to answer (guardrail); defer to a human

The score is intentionally rule-based and explainable: every decision can be
traced back to the retrieval signals below, rather than a hidden model call.

Signals used (all derived from keyword retrieval scores):
  - top_score:   the highest chunk score (strength of the best match)
  - hit_count:   how many chunks cleared the retrieval threshold
  - score_gap:   how far the top chunk beats the runner-up (is there a clear winner?)
"""

from dataclasses import dataclass
from typing import List, Tuple


# Thresholds (tuned against the sample docs; documented in the model card).
HIGH_MIN_TOP_SCORE = 3      # a strong single match scores at least this
MEDIUM_MIN_TOP_SCORE = 2    # a usable-but-weak match

LOW_CONFIDENCE_LABEL = "LOW"
MEDIUM_CONFIDENCE_LABEL = "MEDIUM"
HIGH_CONFIDENCE_LABEL = "HIGH"


@dataclass
class ConfidenceReport:
    """The result of assessing a single query's retrieval quality."""
    level: str                 # HIGH / MEDIUM / LOW
    score: float               # normalized 0.0 - 1.0
    should_answer: bool        # False = guardrail refuses
    needs_caveat: bool         # True = answer but warn the user
    reasons: List[str]         # human-readable explanation of the decision
    top_score: int
    hit_count: int
    score_gap: int


def assess_confidence(
    scored_chunks: List[Tuple[int, str, str]],
) -> ConfidenceReport:
    """
    Assess retrieval confidence from scored chunks.

    scored_chunks: list of (score, filename, chunk_text), highest first,
                   as returned by DocuBot.retrieve_with_scores().

    Returns a ConfidenceReport describing the level and the decision.
    """
    reasons: List[str] = []

    # Case 0: nothing was retrieved at all -> lowest confidence, refuse.
    if not scored_chunks:
        return ConfidenceReport(
            level=LOW_CONFIDENCE_LABEL,
            score=0.0,
            should_answer=False,
            needs_caveat=False,
            reasons=["No relevant chunks were retrieved."],
            top_score=0,
            hit_count=0,
            score_gap=0,
        )

    top_score = scored_chunks[0][0]
    hit_count = len(scored_chunks)
    runner_up = scored_chunks[1][0] if len(scored_chunks) > 1 else 0
    score_gap = top_score - runner_up

    # Decide the level from the strongest match, then refine with other signals.
    if top_score >= HIGH_MIN_TOP_SCORE:
        level = HIGH_CONFIDENCE_LABEL
        reasons.append(f"Strong top match (score {top_score}).")
    elif top_score >= MEDIUM_MIN_TOP_SCORE:
        level = MEDIUM_CONFIDENCE_LABEL
        reasons.append(f"Moderate top match (score {top_score}).")
    else:
        level = LOW_CONFIDENCE_LABEL
        reasons.append(f"Weak top match (score {top_score}).")

    # Multiple supporting chunks slightly increase trust.
    if hit_count >= 2:
        reasons.append(f"{hit_count} supporting chunks retrieved.")
    else:
        reasons.append("Only one chunk cleared the retrieval threshold.")

    # A clear gap between #1 and #2 means the top match stands out.
    if score_gap >= 2:
        reasons.append(f"Top chunk clearly outranks the next (gap {score_gap}).")

    # Normalize to a 0-1 score for display. Cap top_score contribution at 6.
    normalized = min(top_score / 6.0, 1.0)

    # Decision policy:
    #   HIGH   -> answer, no caveat
    #   MEDIUM -> answer, with caveat
    #   LOW    -> refuse (guardrail)
    if level == HIGH_CONFIDENCE_LABEL:
        should_answer, needs_caveat = True, False
    elif level == MEDIUM_CONFIDENCE_LABEL:
        should_answer, needs_caveat = True, True
        reasons.append("Answer will be returned with a verification caveat.")
    else:
        should_answer, needs_caveat = False, False
        reasons.append("Confidence too low; refusing and deferring to a human.")

    return ConfidenceReport(
        level=level,
        score=round(normalized, 2),
        should_answer=should_answer,
        needs_caveat=needs_caveat,
        reasons=reasons,
        top_score=top_score,
        hit_count=hit_count,
        score_gap=score_gap,
    )
