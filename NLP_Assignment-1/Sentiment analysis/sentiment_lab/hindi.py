"""Local Hindi/Hinglish lexicon adapter with explicit, inspectable rules."""
from functools import lru_cache
import json
import math
from pathlib import Path
import re
import unicodedata
from .engine import classify, vader, validate_text

NEGATORS = {"नहीं", "नही", "मत", "ना", "nahi", "nahin", "nhi", "mat", "na", "not", "never", "no"}
INTENSIFIERS = {"बहुत", "बेहद", "काफी", "अत्यंत", "bahut", "bohot", "bohut", "bahot", "kaafi", "very", "really"}
BOUNDARIES = {".", "!", "?", "।", ",", ";", ":", "लेकिन", "पर", "मगर", "और", "but", "lekin", "magar", "aur", "and"}
TOKEN_PATTERN = re.compile(r"[\u0900-\u097f]+|[a-z]+|[.!?।,;:]", re.IGNORECASE)


@lru_cache(maxsize=1)
def lexicon() -> dict[str, float]:
    path = Path(__file__).resolve().parents[1] / "data/hindi_lexicon.json"
    return {unicodedata.normalize("NFC", key): value for key, value in json.loads(path.read_text(encoding="utf-8")).items()}


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(unicodedata.normalize("NFC", text).casefold())


def looks_hindi(text: str) -> bool:
    """A routing heuristic, overridable by the user; not language identification."""
    return bool(re.search(r"[\u0900-\u097f]", text)) or any(t in lexicon() for t in tokenize(text))


def analyze_hindi(text: str) -> dict:
    text = validate_text(text)
    tokens = tokenize(text)
    words = lexicon()
    matches = []
    for i, token in enumerate(tokens):
        base = words.get(token)
        source = "Hindi lexicon"
        if base is None:
            base = vader().lexicon.get(token)
            source = "English lexicon"
        if base is None or token in NEGATORS or token in BOUNDARIES:
            continue
        before, after = [], []
        for j in range(i - 1, max(-1, i - 4), -1):
            if tokens[j] in BOUNDARIES or tokens[j] in words or tokens[j] in vader().lexicon:
                break
            before.append(tokens[j])
        for j in range(i + 1, min(len(tokens), i + 4)):
            if tokens[j] in BOUNDARIES or tokens[j] in words or tokens[j] in vader().lexicon:
                break
            after.append(tokens[j])
        negators = [t for t in before if t in NEGATORS] + [t for t in after if t in NEGATORS - {"not", "never", "no"}]
        negated = len(negators) % 2 == 1
        intensified = any(t in INTENSIFIERS for t in before[:2])
        adjusted = float(base) * (1.5 if intensified else 1.0) * (-0.74 if negated else 1.0)
        matches.append({"token": token, "base_valence": float(base), "valence": adjusted,
                        "negated": negated, "intensified": intensified, "source": source})
    total = sum(m["valence"] for m in matches)
    score = total / math.sqrt(total * total + 15) if total else 0.0
    return {"text": text, "method": "Hindi lexicon + negation", "label": classify(score),
            "score": score, "matches": matches, "matched_terms": len(matches)}
