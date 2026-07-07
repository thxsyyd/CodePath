# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  
Both. I built and refined the rule-based model, then compared it side-by-side with the ML model trained on the same dataset.

**Intended purpose:**  
What is this model trying to do?  
This is a demonstration project that classifies short English social media posts into four mood categories: positive, negative, neutral, or mixed. It could serve as an educational baseline for understanding how simple sentiment classifiers work, or as a starting point for downstream applications such as AI chatbots that need to gauge user emotion during conversations. It is not designed for production use — the training dataset is very small (only ~16 posts), and both models have significant limitations that are documented below.

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  
For the ML version, describe how training works at a high level (no math needed).

Rule-based version (mood_analyzer.py) follows a three-step prediction pipeline:

Representation (preprocess()): lowercases the text, isolates emojis, and strips punctuation to produce a list of tokens.
Scoring (score_text()): loops through tokens, matches against hand-curated positive/negative word lists and emoji sets, with special handling for negation words ("not", "never") that flip the next sentiment token. Returns a (positive_score, negative_score) tuple.
Decision rule (predict_label()): maps the score tuple to a label — "mixed" if both sides fire, "positive"/"negative" if one dominates, "neutral" if neither fires.

ML version (ml_experiments.py) uses classical machine learning:

CountVectorizer converts each post into a bag-of-words vector — a numeric list where each dimension counts how often a word appears in that post.
LogisticRegression learns weights for each word by looking at the training examples and their labels. During prediction, it multiplies the weights by word counts and picks the highest-scoring category.

Unlike the rule-based model, no explicit rules are written — the model derives its own patterns from the labeled data.


## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.
The dataset lives in `dataset.py` as two aligned lists: `SAMPLE_POSTS` and `TRUE_LABELS`. The starter provided 6 posts. I extended it to **16 posts** by adding 10 new examples that deliberately reflect messy, realistic language — sarcasm, slang, emoji-driven expression, mixed emotions, and ambiguous statements.

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.

I labeled each new post based on my personal reading of its emotional intent, not just the literal words. Several were genuinely difficult and could reasonably be labeled differently by another person:

- `"I'm fine 🙂"` — labeled `negative`, since this phrase is commonly used to mask negative feelings. Another labeler could reasonably choose `positive` based on the surface reading. This example illustrates how "true labels" are really *human judgments*, not universal truths.
- `"The exam was sick tbh, way harder than expected"` — labeled `mixed`, because "sick" is ambiguous slang (could mean cool or hard) and "harder than expected" is negative. Reasonable labelers might disagree.
- `"It is what it is"` — labeled `neutral`, though this phrase often carries an undertone of resignation that leans negative.

**Important characteristics of your dataset:**  

- Contains slang: "fire", "lowkey", "sick", "tbh"
- Contains emojis: 🎉, 😔, 🙂, 🙄
- Contains sarcasm: "I absolutely love getting stuck in traffic 🙄", "Great, another Monday"
- Contains mixed emotions: "Lowkey stressed but kind of proud of myself"
- Contains ambiguous language: "It is what it is", "I'm fine 🙂"
- Short-form (typical social media post length)

**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

- **Size**: 16 examples is far too small for a machine learning model to generalize well. Real-world sentiment datasets typically have thousands to millions of labeled examples.
- **Label imbalance**: Roughly 5 positive, 6 negative, 3 mixed, 2 neutral — the "mixed" and "neutral" classes are especially underrepresented.
- **Labeler bias**: All labels reflect a single person's (my) judgment. There is no inter-annotator agreement to check consistency.
- **Language and cultural narrowness**: Only English, with slang and cultural references (e.g., "Monday" as universally undesirable) that assume a Western, urban, casual context. The model would likely misinterpret language from other cultures or dialects.
- **No neutral variety**: Only two neutral examples ("This is fine" and "It is what it is") — the model has very little to learn from about what "neutral" actually looks like.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
The rule-based model in `mood_analyzer.py` implements a three-stage prediction pipeline:

1. **Preprocessing** (`preprocess()`):
   - Lowercases the text
   - Isolates known emojis (🙂, 🙄, 😊, 😔, 😭, 🎉, 💀, 😂, 🥲, 😞) by padding them with spaces so they become their own tokens
   - Splits on whitespace
   - Strips punctuation from each token, but leaves emojis and internal apostrophes intact

2. **Scoring** (`score_text()`):
   - Iterates over tokens and tracks two separate scores: `positive_score` and `negative_score`
   - Positive signal (+1 to positive_score): matches against `POSITIVE_WORDS` list or positive emoji set (🎉, 😊, 🙂, 😂, 🥲)
   - Negative signal (+1 to negative_score): matches against `NEGATIVE_WORDS` list or negative emoji set (😔, 😭, 😞, 🙄, 💀)
   - **Negation handling**: negation words ("not", "never", "no", "isn't", "aren't", "wasn't", "weren't") flip the sentiment of the next matching token. E.g., "not happy" contributes to `negative_score`, not `positive_score`.
   - **Counting**: repeated words or emojis contribute multiple times (e.g., 🎉🎉🎉 → +3 to positive_score)
   - Returns the tuple `(positive_score, negative_score)`

3. **Label prediction** (`predict_label()`):
   - Both scores > 0 → `mixed`
   - Positive dominates → `positive`
   - Negative dominates → `negative`
   - Both scores = 0 → `neutral`

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

- **Fully interpretable**: For every prediction, I can point to the exact tokens that fired and explain the decision (`explain()` method makes this visible).
- **Handles explicit negation** better than the ML model — "not bad" is correctly flipped to positive.
- **Predictable behavior on unseen data**: if a word is in the vocabulary, its contribution is always the same. No hidden weights.
- **Emoji-aware**: correctly picks up 🎉 as positive and 😔 as negative, since I explicitly encoded them.

**Weaknesses of this approach:**  
Where does it fail?  

- **Vocabulary gaps** are the dominant failure mode. Any word not in `POSITIVE_WORDS`/`NEGATIVE_WORDS` is invisible to the model. Fixing this requires manually expanding the word lists forever — a losing battle.
- **Cannot detect sarcasm.** Sentences like "Great, another Monday" or "I absolutely love getting stuck in traffic 🙄" contain positive keywords the model has no way to reinterpret in context. The rule-based system reads them literally.
- **Slang ambiguity**: words like "sick" can mean "cool" (positive) or "difficult/unpleasant" (negative) depending on context. A single word list cannot capture both.
- **No context window**: the model treats each token independently (except for the one-token negation flip). It cannot understand phrases like "kind of proud" or "not really that bad".

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Bag-of-words representation using `CountVectorizer` from scikit-learn. Each post is converted into a numeric vector whose length equals the total vocabulary of the training set. Each dimension counts how many times a specific word appears in that post. Word order is discarded.

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.
The model is trained on the same `SAMPLE_POSTS` and `TRUE_LABELS` in `dataset.py` that the rule-based model uses for evaluation (16 examples).

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

The model is a `LogisticRegression` classifier that learns per-word weights toward each of the four mood classes. During training, it adjusts these weights so its predictions best match the provided labels. Because I evaluated it on the **same data** used for training, its reported accuracy of 100% is *training accuracy*, not true generalization ability. When I tested it on new, unseen sentences interactively, its accuracy dropped sharply — a classic sign of overfitting on a tiny dataset.

**Strengths and weaknesses:**
Strengths might include learning patterns automatically.  

Strengths:
- **No manual rule writing required.** The model discovers patterns from the data automatically.
- **Handles sarcasm-in-training-set**: because "Great, another Monday" was labeled negative, the model learned that "another Monday" is a negative signal — something the rule-based model cannot do.
- **Learned that "sick + harder" pattern maps to mixed**, correctly classifying one of the exam sentences.
- Requires only relabeling and retraining to improve — no coding changes.

Weaknesses:
- **Severely overfit to 16 examples.** On unseen inputs like "I feel amazing today" (obviously positive), the model predicted `negative` — because "amazing" appears only once in training data and other words dominated the weights.
- **No negation understanding.** Predicted "Not bad honestly" as `negative`, because it treats "not" and "bad" as independent features.
- **Bag-of-words discards word order.** "I love this class" and "This class loves I" would be identical to the model.
- **Black-box in a small way**: while you can inspect the weights, they're not as clearly interpretable as a hand-written rule.
- **Fragile with new vocabulary**: any word not seen during training is completely ignored (contributes zero).

## 5. Evaluation

**How you evaluated the model:**  
Both models were evaluated by running them against `SAMPLE_POSTS` and comparing predictions to `TRUE_LABELS`. Accuracy was measured as (correct predictions / total predictions).

- **Rule-based model**: 12 out of 16 correct → **75% accuracy** on the labeled dataset (after Part 3 vocabulary expansion; started at 50% before adding words like "hopeful", "proud", "fire", "exhausted").
- **ML model**: 16 out of 16 correct → **100% training accuracy**. However, on unseen sentences during interactive testing, actual accuracy dropped to roughly 60%, revealing overfitting.

**Examples of correct predictions:**

- "I love this class so much" — Both models correctly labeled positive. Rule-based matched the word `love`; ML learned that `love` correlates with positive.
- "Feeling tired but kind of hopeful" — Rule-based correctly labeled `mixed` after `hopeful` was added to the vocabulary in Part 3, allowing both positive and negative signals to fire.
- "Just got the offer 🎉🎉🎉" — Rule-based correctly labeled positive by counting three emoji hits (+3 to positive_score).

**Examples of incorrect predictions:**

- **Sarcasm (rule-based fails, ML gets it right by memorization):**
  - "Great, another Monday" — Rule-based predicted `positive` (matched "great"), true label is `negative`. ML got this right only because it had seen this exact pattern during training.
  - "I absolutely love getting stuck in traffic 🙄" — Rule-based predicted `mixed` (love +1, 🙄 -1), true label is `negative`. ML memorized it correctly.

- **Ambiguous slang (both models struggle):**
  - "The exam was sick tbh, way harder than expected" — Rule-based predicted `negative` (only `harder` matched), true label is `mixed`. ML happened to memorize this one.

- **ML overfitting on new data (rule-based more robust):**
  - "Not bad honestly" — ML predicted `negative` because it doesn't understand negation. Rule-based (if given this input) would correctly return `positive` thanks to explicit negation handling.
  - "I feel amazing today" — ML predicted `negative`, despite this being obviously positive. The word "amazing" was underrepresented in training data and other features dominated.

**Failure comparison:**  
The two models fail differently. Rule-based fails on **things it wasn't told about** (words not in vocabulary, sarcasm patterns not encoded). ML fails on **things it hasn't seen enough examples of** (any pattern not well-represented in the 16-sample training set). Neither failure mode is inherently worse — they reflect fundamentally different ways of building a classifier.

## 6. Limitations

Describe the most important limitations.  

- **Dataset is very small (16 examples).** No amount of clever modeling can overcome this. Both models are essentially toy demos.
- **Both models fail on sarcasm in principle.** The rule-based model cannot understand that "love" and 🙄 combined signal irony. The ML model can only learn sarcasm patterns it has explicitly seen in training data — it cannot generalize the *concept* of sarcasm.
- **The models cannot handle context or word order.** "I don't love this" and "I love, don't this" would score the same under bag-of-words.
- **The models cannot handle intensity.** "Slightly annoyed" and "absolutely furious" both contribute equally under simple word matching.
- **The models cannot handle mixed dialects or non-English text.** Feeding in Chinese or Spanish sentences would produce essentially random labels since none of those words appear in the vocabulary.
- **Labels are subjective.** My personal reading of "I'm fine 🙂" as negative shapes the entire system's understanding of that phrase. A different labeler would produce a different model.
- **Neutral and mixed classes are underrepresented**, so the model is especially weak at recognizing them.

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
- **Misclassifying distress signals.** If deployed to screen social media posts for mental health concerns, a message like "I'm fine 🙂" being classified as positive could cause the system to miss someone genuinely struggling. Conversely, sarcastic negative posts being flagged as distress would generate false alarms and dilute human reviewers' attention.
- **Cultural and linguistic bias.** The vocabulary lists reflect a Western, English-speaking, casual internet register. Slang and emoji usage vary widely across age groups, regions, and communities. The model would systematically misinterpret language from non-Western English speakers, older generations, or non-native speakers — potentially penalizing them or excluding them from services.
- **Privacy.** Any real deployment would involve analyzing users' personal messages. This raises consent, surveillance, and data-retention concerns that are outside the scope of the model itself but would be central to any real use.
- **Automation bias.** Users (and developers deploying this) may over-trust the output because it produces confident-looking labels. But "positive" and "negative" are dramatic oversimplifications of human emotional expression — treating them as ground truth risks reducing complex human states to binary flags.
- **Feedback loops in AI products.** If an AI chatbot uses this classifier to decide how to respond emotionally, systematic misclassification (e.g., calling sarcasm "positive") would train users to communicate less naturally to be "understood" by the bot — the tool would reshape human behavior in ways the designers didn't intend.

## 8. Ideas for Improvement

List ways to improve either model.  
- **Grow the dataset significantly.** Move from 16 examples to at least several hundred, with balanced representation across positive/negative/neutral/mixed and diverse language styles.
- **Use TF-IDF instead of raw word counts** so common words like "the" and "was" don't dominate the feature space.
- **Add n-gram features** (word pairs and triplets) so the ML model can capture phrases like "not bad" or "kind of" as atomic units.
- **Introduce a real train/test split** to measure true generalization accuracy instead of training accuracy. With 16 examples this isn't practical, but with a larger dataset it becomes essential.
- **Cross-validation** to get a more stable estimate of model performance.
- **Move beyond bag-of-words** to a small neural model or pre-trained language model (e.g., a sentence-transformer). These handle word order and semantic similarity in ways bag-of-words cannot.
- **Improve the rule-based scorer**:
  - Handle longer negation windows (currently only affects the immediately following token)
  - Add intensifiers ("very", "extremely", "kind of") that scale nearby sentiment
  - Add explicit sarcasm markers (positive words + 🙄 or /s)
- **Solicit multiple annotators** for each post and measure agreement. Where labelers disagree, that's real signal about how subjective the task is.
- **Add uncertainty estimates.** Rather than returning a single label, the model could return a confidence score, so downstream systems know when to fall back to human review.