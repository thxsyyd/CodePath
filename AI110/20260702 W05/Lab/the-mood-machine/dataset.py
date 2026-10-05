"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # Added in Part 3 to fix vocabulary gaps
    "hopeful",
    "proud",
    "best",
    "fire",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # Added in Part 3 to fix vocabulary gaps
    "exhausted",
    "harder",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)


# ---------------------------------------------------------------------
# Extended dataset — realistic language styles
# ---------------------------------------------------------------------

SAMPLE_POSTS.extend([
    # Sarcasm
    "I absolutely love getting stuck in traffic 🙄",
    "Great, another Monday",
    # Slang
    "This concert was fire, lowkey the best night ever",
    "The exam was sick tbh, way harder than expected",
    # Emoji-driven
    "Just got the offer 🎉🎉🎉",
    "Kind of a rough day 😔",
    "I'm fine 🙂",
    # Mixed emotions
    "Lowkey stressed but kind of proud of myself",
    "Exhausted from work but happy the week is over",
    # Ambiguous
    "It is what it is",
])

TRUE_LABELS.extend([
    "negative",   # sarcasm about traffic — "love" is misleading
    "negative",   # sarcastic "great"
    "positive",   # "fire" is slang for "great"
    "mixed",      # "sick" is ambiguous, "harder than expected" is negative
    "positive",   # celebration via emojis
    "negative",   # "rough day" + sad emoji
    "negative",   # "I'm fine 🙂" often masks negative feelings — debatable
    "mixed",      # stressed + proud
    "mixed",      # exhausted + happy
    "neutral",    # non-committal expression
])