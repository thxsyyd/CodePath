"""
Core DocuBot Pro class.

Responsibilities:
- Load documents from the docs/ folder
- Build a keyword index and paragraph-level chunks
- Retrieve relevant snippets for a query
- Support retrieval-only answers
- Support grounded RAG answers when paired with a Gemini client
- Run a confidence-gated RAG pipeline that decides whether to answer,
  answer-with-caveat, or refuse (the reliability upgrade over the base project)
"""

import os
import glob

from confidence import assess_confidence
from trace_log import TraceLogger


class DocuBot:
    # Common English words that carry little meaning for keyword matching.
    # Skipping them stops noisy words like "the" or "is" from inflating scores.
    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "do", "does",
        "for", "from", "how", "i", "in", "is", "it", "of", "on", "or",
        "that", "the", "there", "these", "this", "to", "was", "what",
        "when", "where", "which", "who", "why", "with", "you", "your",
        "any", "mention", "me", "my", "can", "will", "would", "should",
    }

    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        self.documents = self.load_documents()  # List of (filename, text)

        # Build a keyword index and paragraph-level chunks
        self.index = self.build_index(self.documents)
        self.chunks = self.build_chunks(self.documents)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
    # Chunking
    # -----------------------------------------------------------

    def build_chunks(self, documents):
        """
        Split each document into paragraph-level chunks.
        Returns a list of (filename, chunk_id, chunk_text) tuples.
        Empty paragraphs are skipped.
        """
        chunks = []
        for filename, text in documents:
            paragraphs = text.split("\n\n")
            for i, para in enumerate(paragraphs):
                para = para.strip()
                if para:
                    chunks.append((filename, i, para))
        return chunks

    # -----------------------------------------------------------
    # Index Construction
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.
        """
        index = {}
        for filename, text in documents:
            words = text.lower().split()
            for word in words:
                if word not in index:
                    index[word] = []
                if filename not in index[word]:
                    index[word].append(filename)
        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
        Return a simple relevance score for how well the text matches the query.

        - Convert query into lowercase words
        - Skip common stop words so they don't inflate scores
        - Count how many meaningful query words appear in the text
        """
        query_words = query.lower().split()
        text_lower = text.lower()

        score = 0
        for word in query_words:
            clean_word = word.strip("?.,!:;()<>/")
            if not clean_word or clean_word in self.STOP_WORDS:
                continue
            score += text_lower.count(clean_word)

        return score

    def retrieve(self, query, top_k=3, min_score=1):
        """
        Retrieve the top_k most relevant paragraph chunks whose score is at
        least min_score. Returns a list of (filename, chunk_text) tuples.
        """
        scored = self.retrieve_with_scores(query, top_k=top_k, min_score=min_score)
        return [(filename, chunk_text) for _, filename, chunk_text in scored]

    def retrieve_with_scores(self, query, top_k=3, min_score=1):
        """
        Like retrieve(), but also returns the numeric score for each chunk.
        Returns a list of (score, filename, chunk_text) tuples, highest first.
        Used by the confidence layer so it can reason about match strength.
        """
        scored = []
        for filename, chunk_id, chunk_text in self.chunks:
            score = self.score_document(query, chunk_text)
            if score >= min_score:
                scored.append((score, filename, chunk_text))

        scored.sort(reverse=True)
        return scored[:top_k]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=5):
        """
        Retrieval-only mode: returns raw snippets and filenames, no LLM.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Plain RAG mode (base project behavior): retrieve snippets, then ask
        Gemini to answer using only them. No confidence gating.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Confidence-gated RAG (the reliability upgrade)
    # -----------------------------------------------------------

    def answer_with_confidence(self, query, top_k=3, min_score=1, logger=None):
        """
        The upgraded pipeline. Steps:
            1. RETRIEVE   - get scored chunks
            2. ASSESS     - score confidence from retrieval signals
            3. DECIDE     - answer / answer-with-caveat / refuse (guardrail)
            4. GENERATE   - only call the LLM when the guardrail allows it

        Returns a dict:
            {
              "answer": str,
              "confidence": "HIGH" | "MEDIUM" | "LOW",
              "score": float,
              "answered": bool,
              "reasons": [str, ...],
              "sources": [filename, ...],
            }

        If a TraceLogger is passed, each step is recorded for later review.
        """
        log = logger or TraceLogger(query)

        # 1. RETRIEVE
        scored = self.retrieve_with_scores(query, top_k=top_k, min_score=min_score)
        sources = [filename for _, filename, _ in scored]
        log.step("RETRIEVE", f"{len(scored)} chunk(s) above min_score={min_score}; "
                             f"sources={sources or 'none'}")

        # 2. ASSESS confidence
        report = assess_confidence(scored)
        log.step("ASSESS", f"confidence={report.level} (score={report.score}); "
                           + "; ".join(report.reasons))

        # 3. DECIDE - guardrail
        if not report.should_answer:
            log.step("DECIDE", "Guardrail: confidence too low -> refuse and defer to human.")
            answer = (
                "I'm not confident enough to answer this from the documentation. "
                "Please verify with a human or rephrase the question."
            )
            log.step("RESPOND", "Refused (low confidence).")
            return {
                "answer": answer,
                "confidence": report.level,
                "score": report.score,
                "answered": False,
                "reasons": report.reasons,
                "sources": sources,
            }

        # 4. GENERATE via the LLM (only reached when the guardrail allows it)
        if self.llm_client is None:
            raise RuntimeError(
                "Confidence RAG requires an LLM client. Provide a GeminiClient instance."
            )

        log.step("DECIDE", f"Confidence sufficient ({report.level}) -> generate answer.")
        snippets = [(filename, chunk_text) for _, filename, chunk_text in scored]
        answer = self.llm_client.answer_from_snippets(query, snippets)

        # Attach a caveat for medium-confidence answers.
        if report.needs_caveat:
            answer = (
                "[Medium confidence - please verify]\n" + answer
            )
            log.step("RESPOND", "Answered with a verification caveat (medium confidence).")
        else:
            log.step("RESPOND", "Answered normally (high confidence).")

        return {
            "answer": answer,
            "confidence": report.level,
            "score": report.score,
            "answered": True,
            "reasons": report.reasons,
            "sources": sources,
        }

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        Used for the naive 'generation only' baseline.
        """
        return "\n\n".join(text for _, text in self.documents)
