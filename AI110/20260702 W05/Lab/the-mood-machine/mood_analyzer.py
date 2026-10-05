# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""


from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens.

        Steps:
          1. Lowercase and strip whitespace
          2. Add spaces around known emojis so they split into separate tokens
          3. Split on whitespace
          4. Strip punctuation from each token (but keep emojis intact)
        """

        # Known emojis (must match the ones used in score_text)
        known_emojis = {"🙂", "🙄", "😊", "😔", "😭", "🎉", "💀", "😂", "🥲", "😞"}

        cleaned = text.strip().lower()

        # Step 2: pad emojis with spaces so they become their own tokens
        for emoji in known_emojis:
            cleaned = cleaned.replace(emoji, f" {emoji} ")

        # Step 3: split on whitespace
        raw_tokens = cleaned.split()

        # Step 4: strip punctuation from each token, but keep emojis untouched
        punctuation = ".,!?;:\"'()[]{}"
        tokens = []
        for token in raw_tokens:
            if token in known_emojis:
                tokens.append(token)  # don't strip emojis
            else:
                tokens.append(token.strip(punctuation))

        # Remove any empty strings that might have appeared
        tokens = [t for t in tokens if t]
        return tokens
    
    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> Tuple[int, int]:
        """
        Compute mood scores for the given text.

        Returns a tuple (positive_score, negative_score):
          - positive_score: sum of positive signal strengths
          - negative_score: sum of negative signal strengths (as a positive number)

        Features:
          - Negation: "not happy" flips "happy" from positive to negative.
          - Emojis: known positive/negative emojis contribute to the scores.
          - Counting: repeated words/emojis are counted multiple times.
        """
        # Emoji word lists (must match the ones used in preprocess)
        positive_emojis = {"🎉", "😊", "🙂", "😂", "🥲"}
        negative_emojis = {"😔", "😭", "😞", "🙄", "💀"}

        # Negation words that flip the next sentiment token
        negation_words = {"not", "never", "no", "isn't", "aren't", "wasn't", "weren't"}

        tokens = self.preprocess(text)

        positive_score = 0
        negative_score = 0
        negate_next = False # flag: 下一个情绪词要不要反转？

        for token in tokens:
            # Check if this token is a negation word
            if token in negation_words:
                negate_next = True
                continue

            # Determine if this token is a positive or negative signal
            is_positive = token in self.positive_words or token in positive_emojis
            is_negative = token in self.negative_words or token in negative_emojis

            if is_positive:
                if negate_next:
                    negative_score += 1  # "not happy" counts as negative
                else:
                    positive_score += 1
                negate_next = False
            elif is_negative:
                if negate_next:
                    positive_score += 1  # "not bad" counts as positive
                else:
                    negative_score += 1
                negate_next = False
            else:
                # Non-sentiment token: reset negation flag so it doesn't linger too far
                negate_next = False

        return (positive_score, negative_score)

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn positive/negative scores into a mood label.

        Rules:
          - Both positive and negative signals present  -> "mixed"
          - Positive dominates                          -> "positive"
          - Negative dominates                          -> "negative"
          - No signals at all                           -> "neutral"
        """
        positive_score, negative_score = self.score_text(text)

        # Both sides fired: conflict → mixed
        if positive_score > 0 and negative_score > 0:
            return "mixed"

        # Only positive fired
        if positive_score > negative_score:
            return "positive"

        # Only negative fired
        if negative_score > positive_score:
            return "negative"

        # Both are zero
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        Shows:
          - All tokens after preprocessing
          - Which tokens counted as positive/negative
          - The final (positive, negative) scores
          - The predicted label
        """
        # Same emoji/negation setup as score_text
        positive_emojis = {"🎉", "😊", "🙂", "😂", "🥲"}
        negative_emojis = {"😔", "😭", "😞", "🙄", "💀"}
        negation_words = {"not", "never", "no", "isn't", "aren't", "wasn't", "weren't"}

        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        negate_next = False

        for token in tokens:
            if token in negation_words:
                negate_next = True
                continue

            is_positive = token in self.positive_words or token in positive_emojis
            is_negative = token in self.negative_words or token in negative_emojis

            if is_positive:
                if negate_next:
                    negative_hits.append(f"NOT+{token}")
                else:
                    positive_hits.append(token)
                negate_next = False
            elif is_negative:
                if negate_next:
                    positive_hits.append(f"NOT+{token}")
                else:
                    negative_hits.append(token)
                negate_next = False
            else:
                negate_next = False

        pos_score, neg_score = self.score_text(text)
        label = self.predict_label(text)

        return (
            f"Label: {label} | "
            f"Positive={pos_score} {positive_hits or '[]'}, "
            f"Negative={neg_score} {negative_hits or '[]'}"
        )
