"""Offline check of the confidence layer using real retrieval scores.

Does NOT call Gemini. It runs retrieval on the sample queries and prints the
confidence decision for each, so we can see HIGH / MEDIUM / LOW behavior.
"""

from docubot import DocuBot
from confidence import assess_confidence
from dataset import SAMPLE_QUERIES


def main():
    bot = DocuBot()  # no llm_client needed for retrieval + confidence

    for query in SAMPLE_QUERIES:
        scored = bot.retrieve_with_scores(query, top_k=3, min_score=1)
        report = assess_confidence(scored)
        top = scored[0][0] if scored else 0
        print(f"{report.level:6s} score={report.score:<4} "
              f"answer={report.should_answer!s:5s} caveat={report.needs_caveat!s:5s} "
              f"top={top}  | {query}")


if __name__ == "__main__":
    main()
