import math
import pytest
from sentiment_lab.engine import analyze, classify


@pytest.mark.parametrize("score, label", [(0.05, "positive"), (-0.05, "negative"), (0.04999, "neutral"), (-0.04999, "neutral"), (0, "neutral")])
def test_threshold_boundaries(score, label):
    assert classify(score) == label


@pytest.mark.parametrize("text", ["", "  ", None, "x" * 5001])
def test_invalid_input_is_rejected(text):
    with pytest.raises(ValueError):
        analyze(text)


def test_nonfinite_score_is_rejected():
    with pytest.raises(ValueError):
        classify(math.nan)


def test_classification_uses_full_precision_not_display_rounding():
    assert classify(0.04999999999999999) == "neutral"
    assert classify(0.05) == "positive"


def test_actual_tools_preserve_hindi_and_do_not_fake_comprehension():
    text = "यह फोन बहुत अच्छा है।"
    result = analyze(text)
    assert result["text"] == text
    assert result["has_devanagari"]
    assert result["vader_compound"] == result["textblob_polarity"] == 0


def test_negation_changes_both_tools():
    for tool in ("vader", "textblob"):
        assert analyze("This is good.")[f"{tool}_label"] == "positive"
        assert analyze("This is not good.")[f"{tool}_label"] == "negative"
