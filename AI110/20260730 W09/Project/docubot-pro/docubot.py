"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a keyword index and paragraph-level chunks
- Retrieving relevant snippets for a query
- Supporting retrieval-only answers
- Supporting grounded RAG answers when paired with a Gemini client
"""

import os
import glob


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

        If no chunk scores >= min_score, returns an empty list so the caller
        can respond with "I do not know."
        """
        scored = []
        for filename, chunk_id, chunk_text in self.chunks:
            score = self.score_document(query, chunk_text)
            if score >= min_score:
                scored.append((score, filename, chunk_text))

        scored.sort(reverse=True)

        results = []
        for score, filename, chunk_text in scored[:top_k]:
            results.append((filename, chunk_text))
        return results

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
        RAG mode: retrieve snippets, then ask Gemini to answer using only them.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        Used for the naive 'generation only' baseline.
        """
        return "\n\n".join(text for _, text in self.documents)
