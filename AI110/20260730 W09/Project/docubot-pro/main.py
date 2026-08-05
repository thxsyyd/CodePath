"""
CLI runner for DocuBot Pro.

Demonstrates the full upgraded pipeline end to end:
    retrieve -> assess confidence -> decide (answer / caveat / refuse) -> generate

Every query prints a step-by-step decision trace and appends it to logs/trace.log
so the agent's behavior can be reviewed after the fact.

Modes:
    1) Confidence RAG   - the upgraded, guardrailed pipeline (recommended)
    2) Plain RAG        - base project behavior, no confidence gating
    3) Retrieval only   - no LLM, raw snippets
    q) Quit
"""

from dotenv import load_dotenv
load_dotenv()

from docubot import DocuBot
from llm_client import GeminiClient
from dataset import SAMPLE_QUERIES
from trace_log import TraceLogger


LOG_PATH = "logs/trace.log"


def try_create_llm_client():
    """Try to create a GeminiClient. Returns (client, has_llm)."""
    try:
        client = GeminiClient()
        return client, True
    except RuntimeError as exc:
        print("Warning: LLM features are disabled.")
        print(f"Reason: {exc}")
        print("You can still run retrieval only mode.\n")
        return None, False


def choose_mode(has_llm):
    print("\nChoose a mode:")
    print("  1) Confidence RAG (upgraded pipeline with guardrail)"
          + ("" if has_llm else "  [needs GEMINI_API_KEY]"))
    print("  2) Plain RAG (base behavior, no guardrail)"
          + ("" if has_llm else "  [needs GEMINI_API_KEY]"))
    print("  3) Retrieval only (no LLM)")
    print("  q) Quit")
    return input("Enter choice: ").strip().lower()


def get_query_or_use_samples():
    print("\nPress Enter to run built-in sample queries.")
    custom = input("Or type a single custom query: ").strip()
    if custom:
        return [custom]
    return SAMPLE_QUERIES


def run_confidence_rag(bot, has_llm):
    if not has_llm or bot.llm_client is None:
        print("\nConfidence RAG needs GEMINI_API_KEY.\n")
        return

    queries = get_query_or_use_samples()
    print("\nRunning Confidence RAG (with guardrail + trace logging)...\n")

    for query in queries:
        logger = TraceLogger(query)
        result = bot.answer_with_confidence(query, logger=logger)

        print("=" * 64)
        print(f"Q: {query}")
        print(f"Confidence: {result['confidence']} (score {result['score']})  "
              f"Answered: {result['answered']}")
        print(f"Sources: {result['sources'] or 'none'}")
        print("-" * 64)
        print(result["answer"])
        print()
        logger.print_trace()
        logger.append_to_file(LOG_PATH)
        print()


def run_plain_rag(bot, has_llm):
    if not has_llm or bot.llm_client is None:
        print("\nPlain RAG needs GEMINI_API_KEY.\n")
        return

    queries = get_query_or_use_samples()
    print("\nRunning Plain RAG (base behavior, no guardrail)...\n")

    for query in queries:
        print("=" * 64)
        print(f"Q: {query}")
        print("-" * 64)
        print(bot.answer_rag(query))
        print()


def run_retrieval_only(bot):
    queries = get_query_or_use_samples()
    print("\nRunning Retrieval only (no LLM)...\n")

    for query in queries:
        print("=" * 64)
        print(f"Q: {query}")
        print("-" * 64)
        print(bot.answer_retrieval_only(query))
        print()


def main():
    print("DocuBot Pro")
    print("===========")

    llm_client, has_llm = try_create_llm_client()
    bot = DocuBot(llm_client=llm_client)

    while True:
        choice = choose_mode(has_llm)
        if choice == "q":
            print("\nGoodbye.")
            break
        elif choice == "1":
            run_confidence_rag(bot, has_llm)
        elif choice == "2":
            run_plain_rag(bot, has_llm)
        elif choice == "3":
            run_retrieval_only(bot)
        else:
            print("\nUnknown choice. Please pick 1, 2, 3, or q.")


if __name__ == "__main__":
    main()
