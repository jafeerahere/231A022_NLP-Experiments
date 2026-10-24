"""Two independent English sentiment tools; no translation or custom lexicon."""
from functools import lru_cache
import math
import re

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

LABELS = ("negative", "neutral", "positive")
THRESHOLD = 0.05
MAX_TEXT_LENGTH = 5000


def classify(score: float, threshold: float = THRESHOLD) -> str:
    """Inclusive +/- boundaries. TextBlob's cutoff is a project choice."""
    if not math.isfinite(score) or not 0 < threshold <= 1:
        raise ValueError("Use a finite score and a threshold in (0, 1].")
    if score >= threshold:
        return "positive"
    if score <= -threshold:
        return "negative"
    return "neutral"


@lru_cache(maxsize=1)
def vader() -> SentimentIntensityAnalyzer:
    return SentimentIntensityAnalyzer()


def validate_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Enter non-empty text.")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Use at most {MAX_TEXT_LENGTH:,} characters per input.")
    return text.strip()


def analyze(text: str) -> dict:
    text = validate_text(text)
    vs = vader().polarity_scores(text)
    blob = TextBlob(text).sentiment_assessments
    return {
        "text": text,
        "vader_label": classify(vs["compound"]),
        "vader_compound": vs["compound"],
        "vader_positive": vs["pos"],
        "vader_neutral": vs["neu"],
        "vader_negative": vs["neg"],
        "textblob_label": classify(blob.polarity),
        "textblob_polarity": float(blob.polarity),
        "textblob_subjectivity": float(blob.subjectivity),
        "textblob_assessments": [
            {"tokens": list(words), "polarity": float(p), "subjectivity": float(s)}
            for words, p, s, _ in blob.assessments
        ],
        "tools_agree": classify(vs["compound"]) == classify(blob.polarity),
        "has_devanagari": bool(re.search(r"[\u0900-\u097f]", text)),
    }
